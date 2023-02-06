"""
Simple script to construct xclim's ERA5/daily_surface_cancities_1990-1993.nc test dataset.

This dataset has the goal to provide a real example of every variable supported by xclim
in the atmos realm. When a variable is not given by ERA5, either an approximated version
is computed or it is ensured that needed base variables are given here. For example, the
`snw` variable doesn't need to be in the dataset, it is simply computed with swe * 1000.

Some of those extra variables are computed here but not included in the final output.

Requires xclim==0.40 and data converted with miranda>=0.3.0

Author: Pascal Bourgault, 2021
Revised: Trevor James Smith, 2023
"""
import datetime as dt
import logging
import sys
from pathlib import Path

import xarray as xr
import xclim as xc
from dask import compute
from dask.distributed import Client
from numpy import arctan2, cos, sin
from xclim.core import formatting
from xclim.core.units import convert_units_to

logging.basicConfig(level=logging.INFO)

if len(sys.argv) == 2:
    base_path = Path(sys.argv[-1])
else:
    base_path = Path().cwd()

# Base Path for converted ERA5
NAMpath = base_path.joinpath("datasets/reconstruction/ECMWF/ERA5/NAM/{time}")
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
                    files.extend(
                        list(
                            fpath.glob(
                                (glob_files.format(time=freq, variable=variable, y=y))
                            )
                        )
                    )

    raw_hrly_nam = xr.open_mfdataset(
        gather["1hr"],
        chunks={"time": 2928, "latitude": 25, "longitude": 50},
        engine="zarr",
    )
    raw_dly_nam = xr.open_mfdataset(
        gather["day"],
        chunks={"time": 2928, "latitude": 25, "longitude": 50},
        engine="zarr",
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
        # Total precip flux in kg m-2 s-1
        pr = hrly.pr.resample(time="D").mean()
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
        # Total Potential Evapotranspiration flux in kg m-2 s-1
        evspsblpot = hrly.evspsblpot.resample(time="D").mean()
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
        # Total Solid Precipitation flux in kg m-2 s-1
        prsn = hrly.prsn.resample(time="D").mean()
    else:
        prsn = dly.prsn

    snw = hrly.snw.resample(time="D").mean() if "snw" not in dly.data_vars else dly.snw
    swe = snw / 1000
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
    )
    snw.attrs.update(
        standard_name="surface_snow_amount",
        long_name="Surface snow amount",
        units="kg m-2",
        cell_methods="time: mean within days",
    )
    snd.attrs.update(
        standard_name="surface_snow_thickness",
        long_name="Snow depth",
        units="m",
        cell_methods="time: mean within days",
    )
    swe.attrs.update(
        standard_name="lwe_thickness_of_surface_snow_amount",
        long_name="Liquid water equivalent of surface snow amount",
        units="m",
        cell_methods="time: mean within days",
    )

    uas, vas = None, None
    if (
        "uas" not in dly.data_vars
        or "vas" not in dly.data_vars
        or "sfcWind" not in dly.data_vars
        or "wsgsmax" not in dly.data_vars
    ):
        windmag_interim, _ = xc.atmos.wind_speed_from_vector(uas=hrly.uas, vas=hrly.vas)
        sfcWind = windmag_interim.resample(time="D").mean()
        wsgsmax = windmag_interim.resample(time="D").max()
        theta = arctan2(hrly.vas, hrly.uas)

        uas = cos(theta) * sfcWind
        vas = sin(theta) * sfcWind
    else:
        uas = dly.uas
        vas = dly.vas
        sfcWind = dly.sfcWind
        wsgsmax = dly.wsgsmax

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
    wsgsmax.attrs.update(
        standard_name="wind_speed_of_gust",
        long_name="Daily maximum surface wind speed (10 m)",
        units="m s-1",
        cell_methods="time: maximum within days",
    )

    _, sfcWindfromdir = xc.atmos.wind_speed_from_vector(uas=uas, vas=vas)

    sfcWindfromdir.attrs.update(
        standard_name="wind_speed_from_direction",
        long_name="Daily mean surface wind direction (10 m)",
        units="degree",
        cell_methods="time: mean within days",
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

    if "rlds" not in dly.data_vars:
        rlds = hrly.rlds.tdps.resample(time="D").mean()
    else:
        rlds = dly.rlds
    rlds.attrs.update(
        standard_name="surface_downwelling_longwave_flux",
        long_name="Surface downwelling longwave flux",
        cell_methods="time: mean within days",
    )

    if "rls" not in dly.data_vars:
        rls = hrly.rls.tdps.resample(time="D").mean()
    else:
        rls = dly.rls
    rlds.attrs.update(
        standard_name="surface_net_downward_longwave_flux",
        long_name="Surface net downward longwave flux",
        cell_methods="time: mean within days",
    )

    if "rsds" not in dly.data_vars:
        rsds = hrly.rsds.tdps.resample(time="D").mean()
    else:
        rsds = dly.rsds
    rsds.attrs.update(
        standard_name="surface_downwelling_shortwave_flux",
        long_name="Surface downwelling shortwave flux",
        cell_methods="time: mean within days",
    )

    if "rss" not in dly.data_vars:
        rss = hrly.rss.tdps.resample(time="D").mean()
    else:
        rss = dly.rss
    rss.attrs.update(
        standard_name="surface_net_downward_shortwave_flux",
        long_name="Surface net downward shortwave flux",
        cell_methods="time: mean within days",
    )

    sund = convert_units_to(
        xc.core.units.to_agg_units(
            (hrly.rsds > 120).resample(time="D").sum(), hrly.rsds, "count"
        ),
        "s",
    )
    sund.attrs.update(
        standard_name="duration_of_sunshine",
        long_name="Daily duration of sunshine",
        cell_methods="time: sum within days",
    )

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
        rlds=rlds,
        rls=rls,
        rsds=rsds,
        rss=rss,
        sfcWind=sfcWind,
        snd=snd,
        snw=snw,
        sund=sund,
        swe=swe,
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
