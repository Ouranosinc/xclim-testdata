"""
Simple script to construct xclim's ERA5/daily_surface_cancities_1990-1993.nc test dataset.

This dataset has the goal to provide a real example of every variable supported by xclim
in the atmos realm. When a variable is not given by ERA5, either an approximated version
is computed or it is ensured that needed base variables are given here. For example, the
`snw` variable doesn't need to be in the dataset, it is simply computed with swe * 1000.

Some of those extra variables are computed here but not included in the final output.

Author: Pascal Bourgault, 2021
Revised: Trevor James Smith, 2022
"""
import datetime as dt
import logging
import sys
from pathlib import Path

import xarray as xr
import xclim as xc
from dask import compute
from dask.distributed import Client
from xclim.core import formatting
from xclim.core.units import convert_units_to

logging.basicConfig(level=logging.INFO)

if len(sys.argv) == 2:
    base_path = Path(sys.argv[-1])
else:
    base_path = Path().cwd()

# Base Path for converted ERA5
NAMpath = base_path.joinpath(
    "datasets/reconstruction/ECMWF/ERA5/NAM/{time}"
)
glob_files = "{variable}_{time}_ecmwf_era5-single-levels_NAM_199{y}*.zarr"

# Protect dask's threading
if __name__ == "__main__":
    logging.info("Starting the construction of ERA5 daily_cancities dataset")
    logging.info(f"Will use data found in {NAMpath.parent.as_posix()}")
    # Uses the threads, but not that much memory
    c = Client(
        n_workers=6, threads_per_worker=6, dashboard_address=8786, memory_limit="5GB"
    )

    gather = dict()
    gather["1hr"] = []
    gather["day"] = []

    for freq, files in gather.items():
        logging.info(f"Gathering {freq} files.")
        for variable_folder in Path(NAMpath.as_posix().format(time=freq)).iterdir():
            variable = variable_folder.name
            fpath = Path(NAMpath.as_posix().format(time=freq)).joinpath(variable)
            if fpath.exists():
                logging.info(f"Found {freq} folders for {variable}.")
                for y in range(4):
                    files.extend(list(fpath.glob((glob_files.format(time=freq, variable=variable, y=y)))))

    raw_hrly_nam = xr.open_mfdataset(
        gather["1hr"],
        chunks={"time": 2928, "latitude": 25, "longitude": 50},
        engine="zarr"
    )
    raw_dly_nam = xr.open_mfdataset(
        gather["day"],
        chunks={"time": 2928, "latitude": 25, "longitude": 50},
        engine="zarr"
    )

    location = xr.DataArray(
        ["Halifax", "Montréal", "Iqaluit", "Saskatoon", "Victoria"],
        dims=("location",),
        name="location",
        attrs={"long_name": "City"},
    )
    lon = xr.DataArray(
        [-63.5, -73.5, -68.5, -106.75, -123.25],
        dims=("location",),
        coords={"location": location},
        attrs={
            "standard_name": "longitude",
            "units": "degree_east",
            "long_name": "longitude",
        },
    )
    lat = xr.DataArray(
        [44.5, 45.5, 63.75, 52.0, 48.5],
        dims=("location",),
        coords={"location": location},
        attrs={
            "standard_name": "latitude",
            "units": "degree_north",
            "long_name": "latitude",
        },
    )

    hrly = raw_hrly_nam.sel(lon=lon, lat=lat, method="nearest")
    dly = raw_dly_nam.sel(lon=lon, lat=lat, method="nearest")

    dly.lon.attrs.update(lon.attrs)
    dly.lat.attrs.update(lat.attrs)
    # Some of those names are not exact (i.e. tp is not pr), but who cares
    try:
        hrly = hrly.rename(
            t2m="tas",
            tp="pr",
            d2m="tdps",
            sd="swe",
            sf="prsn",
            sp="ps",
            msl="psl",
            u10="uas",
            v10="vas",
            pev="evspsblpot",
            msdwswrf="rsds",
            msdwlwrf="rlds",
        )
    except ValueError:
        pass

    # Variables computation
    # Loosely regrouped by thematics

    if "tas" not in dly.data_vars:
        tas = hrly.tas.resample(time="D").mean()
    else:
        tas = dly.tas

    if "tasmin" not in dly.data_vars:
        tasmin = hrly.tas.resample(time="D").min()
    else:
        tasmin = dly.tasmin

    if "tasmax" not in dly.data_vars:
        tasmax = hrly.tas.resample(time="D").max()
    else:
        tasmax = dly.tasmax

    tas.attrs.update(
        standard_name="air_temperature",
        long_name="Mean daily surface temperature",
        units="K",
        cell_methods="time: mean within days",
    )
    tasmin.attrs.update(
        standard_name="air_temperature",
        long_name="Minimum daily surface temperature",
        units="K",
        cell_methods="time: minimum within days",
    )
    tasmax.attrs.update(
        standard_name="air_temperature",
        long_name="Mean daily surface temperature",
        units="K",
        cell_methods="time: maximum within days",
    )

    if "pr" not in dly.data_vars:
        # Total precip in m to flux in kg m-2 s-1 : daily_sum [m/day] * 1000 kg/m³ / 86400 s/day
        pr = hrly.pr.resample(time="D").sum() * 1000 / 86400
    else:
        pr = dly.pr

    pr.attrs.update(
        standard_name="precipitation_flux",
        long_name="Mean daily precipitation flux",
        units="kg m-2 s-1",
        cell_methods="time: mean within days",
        description="Total precipitation thickness converted to mass flux using a water density of 1000 kg/m³.",
    )

    if "evspsblpot" not in dly.data_vars:
        # Total Potential Evapotranspiration in m to flux in kg m-2 s-1, daily sum [m/d] * 1000 kg/m³ / 86400 s/d
        evspsblpot = hrly.evspsblpot.resample(time="D").sum() * 1000 / 86400
    else:
        evspsblpot = dly.evspsblpot

    evspsblpot.attrs.update(
        standard_name="water_potential_evaporation_flux",
        long_name="Mean daily potential evaporation flux",
        units="kg m-2 s-1",
        cell_methods="time: mean within days",
        description="Total potential evaporation thickness converted to mass flux using a water density of 1000 kg/m³.",
    )

    if "prsn" not in dly.data_vars:
        # Total snow precip in m of water equivalent to flux in kg m-2 s-1 : daily_sum [m/day] * 1000 kg/m³ / 86400 s/day
        prsn = hrly.prsn.resample(time="D").sum() * 1000 / 86400
    else:
        prsn = dly.prsn

    snw = hrly.snw.resample(time="D").mean() if "snw" not in dly.data_vars else dly.snw
    snr = hrly.snr.resample(time="D").mean() if "snr" not in dly.data_vars else dly.snr
    if "snd" not in dly.data_vars:
        if "snd" in hrly.data_vars:
            snd = hrly.snd.resample(time="D").mean()
        else:
            snd = snw / snr
    else:
        snd = dly.snd

    prsn.attrs.update(
        standard_name="solid_precipitation_flux",
        long_name="Mean daily solid precipitation",
        units="kg m-2 s-1",
        cell_methods="time: mean within days",
        description="Total solid precipitation thickness of water equivalent "
        "converted to mass flux using a water density of 1000 kg/m³.",
    )
    snw.attrs.update(
        standard_name="surface_snow_amount",
        long_name="Surface snow amount",
        units="kg m-2",
        cell_methods="time: mean within days",
        description="Snow thickness in m of liquid water equivalent "
        "converted to snow amount using a water density of 1000 kg/m³.",
    )
    snd.attrs.update(
        standard_name="surface_snow_thickness",
        long_name="Snow depth",
        units="m",
        cell_methods="time: mean within days",
        description="Snow thickness in m of liquid water equivalent converted "
        "to snow thickness using a water density of 1000 kg/m³ "
        "and a snow density of 300 kg/m³.",
    )

    if "uas" not in dly.data_vars:
        uas = hrly.uas.resample(time="D").mean()
    else:
        uas = dly.uas

    if "vas" not in dly.data_vars:
        vas = hrly.vas.resample(time="D").mean()
    else:
        vas = dly.vas

    windmag, _ = xc.atmos.wind_speed_from_vector(uas=hrly.uas, vas=hrly.vas)
    sfcWind = windmag.resample(time="D").mean()
    wsgsmax = windmag.resample(time="D").max()

    _, sfcWindfromdir = xc.atmos.wind_speed_from_vector(uas=uas, vas=vas)

    uas.attrs.update(
        standard_name="eastward_wind",
        long_name="Eastward wind component (10 m)",
        units="m s-1",
        cell_methods="time: mean within days",
    )
    vas.attrs.update(
        standard_name="northward_wind",
        long_name="Northward wind component (10 m)",
        units="m s-1",
        cell_methods="time: mean within days",
    )
    sfcWind.attrs.update(
        standard_name="wind_speed",
        long_name="Daily mean surface wind speed (10 m)",
        units="m s-1",
        cell_methods="time: mean within days",
    )
    sfcWindfromdir.attrs.update(
        standard_name="wind_speed_from_direction",
        long_name="Daily mean surface wind direction (10 m)",
        units="degree",
        cell_methods="time: mean within days",
    )
    wsgsmax.attrs.update(
        standard_name="wind_speed_of_gust",
        long_name="Daily maximum surface wind speed (10 m)",
        units="m s-1",
        cell_methods="time: maximum within days",
    )

    if "ps" not in dly.data_vars:
        ps = hrly.ps.resample(time="D").mean()
    else:
        ps = dly.ps

    if "psl" not in dly.data_vars:
        if "psl" not in hrly.data_vars:
            psl = ps.copy()
        else:
            psl = hrly.psl.resample(time="D").mean()
    else:
        psl = dly.psl

    ps.attrs.update(
        standard_name="surface_air_pressure",
        long_name="Daily mean surface air pressure",
        cell_methods="time: mean within days",
        units="Pa",
    )
    psl.attrs.update(
        standard_name="air_pressure_at_sea_level",
        long_name="Daily mean sea-level air pressure",
        cell_methods="time: mean within days",
        units="Pa",
        description="Copy of surface air pressure.",
    )

    if "tdps" not in dly.data_vars:
        tdps = hrly.tdps.resample(time="D").mean()
    else:
        tdps = dly.tdps

    tdps.attrs.update(
        standard_name="dew_point_temperature",
        long_name="Daily mean surface dew point temperature",
        units="K",
        cell_methods="time: mean within days",
    )

    hurs = (
        convert_units_to(
            xc.atmos.relative_humidity_from_dewpoint(tas=tas, tdps=tdps), "1"
        )
        .resample(time="D")
        .mean(keep_attrs=True)
    )
    hurs.attrs.update(
        long_name="Daily mean surface relative humidity",
        cell_methods="time: mean within days",
        units="1",
    )

    huss = xc.atmos.specific_humidity(tas=tas, hurs=hurs, ps=ps)
    huss.attrs.update(
        long_name="Daily mean surface specific humidity",
        cell_methods="time: mean within days",
        units="1",
    )

    # sund = convert_units_to(
    #     xc.core.units.to_agg_units(
    #         (hrly.rsds > 120).resample(time="D").sum(), hrly.rsds, "count"
    #     ),
    #     "s",
    # )
    # sund.attrs.update(
    #     standard_name="duration_of_sunshine",
    #     long_name="Daily duration of sunshine",
    #     cell_methods="time: sum within days",
    # )

    logging.info("Preparing dataset")
    ds = xr.Dataset(
        coords={k: v for k, v in dly.coords.items() if k != "time"},
        attrs={
            "Conventions": "CF-1.9",
            "history": formatting.update_history(
                "Spatial extraction, daily aggregation and intermediate computation of raw ERA5 data.",
                raw_dly_nam,
            ),
            "title": "xclim test dataset from ERA5",
            "source": "reanalysis",
            "comment": f"Contains modified Copernicus Climate ChangeService information {dt.date.today().year}",
            "institution": "ECMWF",
            "doi": "doi:10.24381/cds.adbb2d47",
            "description": (
                "Test dataset for xclim including all officially supported atmos variables that ERA5 can provide. "
                "Intended for testing only, some intermediate variables are only rough approximations, "
                "but they should have data in the right range and sequence. Approximated variables are flagged "
                "as such in their description."
            ),
        },
    )

    # Here we choose which variables to include
    ds = ds.assign(
        evspsblpot=evspsblpot,
        hurs=hurs,
        huss=huss,
        pr=pr,
        prsn=prsn,
        ps=ps,
        psl=psl,
        sfcWind=sfcWind,
        snd=snd,
        snw=snw,
        # sund=sund,  # not available
        tas=tas,
        tasmax=tasmax,
        tasmin=tasmin,
        tdps=tdps,
        uas=uas,
        vas=vas,
        wsgsmax=wsgsmax,
    )

    # Needed due to bad metadata in some variable coordinates
    for coord in ds.coords:
        if "_precision" in ds[coord].attrs:
            del ds[coord].attrs["_precision"]

    # Save it with a fancy save_mfdataset : enables parallel IO. But we merge it anyway at the end.
    base_path = "daily_surface_cancities_1990-1993_{var}.nc"
    objs = []
    paths = []
    for nam, var in ds.data_vars.items():
        objs.append(var.to_dataset())
        paths.append(base_path.format(var=nam))
    delayed = xr.save_mfdataset(objs, paths, compute=False)
    compute(delayed)

    dss = xr.open_mfdataset("daily_surface_cancities_1990-1993_*.nc")
    dss = dss.transpose("location", "time")
    dss.attrs.update(ds.attrs)
    encoding = {"time": {"dtype": "int32"}}
    for var in dss.data_vars.keys():
        encoding[var] = {"dtype": "float32"}
    dss.to_netcdf("daily_surface_cancities_1990-1993.nc", encoding=encoding)
