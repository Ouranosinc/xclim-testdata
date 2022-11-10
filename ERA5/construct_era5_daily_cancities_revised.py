"""
Simple script to construct xclim's ERA5/daily_surface_cancities_1990-1993.nc test dataset.

This dataset has the goal to provide a real example of every variable supported by xclim
in the atmos realm. When a variable is not given by ERA5, either an approximated version
is computed or it is ensured that needed base variables are given here. For example, the
`snw` variable doesn't need to be in the dataset, it is simply computed with swe * 1000.

Some of those extra variables are computed here but not included in the final output.

Author: Pascal Bourgault, 2021
"""
import sys

import xarray as xr
import xclim as xc
from dask import compute
from dask.distributed import Client
from xclim.core.units import convert_units_to

if len(sys.argv) == 2:
    base_path = sys.argv[-1]

# Base Path for converted ERA5
NAMpath = base_path + "/datasets/reconstruction/ECMWF/ERA5/NAM/day/*/*_day_ecmwf_era5-single-levels_NAM_199[0123].zarr"

# Protect dask's threading
if __name__ == "__main__":
    print("Starting the construction of ERA5 daily_cancities dataset")
    print(f"Will use data found in {NAMpath}")
    # Uses the threads, but not that much memory
    c = Client(
        n_workers=6, threads_per_worker=6, dashboard_address=8786, memory_limit="5GB"
    )

    raw_nam = xr.open_mfdataset(
        NAMpath, chunks={"time": 2928, "latitude": 25, "longitude": 50}
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

    hrly = raw_nam.sel(longitude=lon, latitude=lat, method="nearest").rename(
        longitude="lon", latitude="lat"
    )

    hrly.lon.attrs.update(lon.attrs)
    hrly.lat.attrs.update(lat.attrs)
    # Some of those names are not exact (i.e. tp is not pr), but who cares
    hrly = hrly.rename(
        t2m="tas",
        tp="pr",
        d2m="dtas",
        sd="swe",
        sf="prsn",
        sp="ps",
        u10="uas",
        v10="vas",
        pev="evpot",
        msdwswrf="rsds",
        msdwlwrf="rlds",
    )

    # Variables computation
    # Loosely regrouped by thematics

    tas = hrly.tas.resample(time="D").mean()
    tasmin = hrly.tas.resample(time="D").min()
    tasmax = hrly.tas.resample(time="D").max()

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

    # Total precip in m to flux in kg m-2 s-1 : daily_sum [m/day] * 1000 kg/m³ / 86400 s/day
    pr = hrly.pr.resample(time="D").sum() * 1000 / 86400

    pr.attrs.update(
        standard_name="precipitation_flux",
        long_name="Mean daily precipitation flux",
        units="kg m-2 s-1",
        cell_methods="time: mean within days",
        description="Total precipitation thickness converted to mass flux using a water density of 1000 kg/m³.",
    )

    # Total Potential Evapotranspiration in m to flux in kg m-2 s-1, daily sum [m/d] * 1000 kg/m³ / 86400 s/d
    evspsblpot = hrly.evpot.resample(time="D").sum() * 1000 / 86400

    evspsblpot.attrs.update(
        standard_name="water_potential_evaporation_flux",
        long_name="Mean daily potential evaporation flux",
        units="kg m-2 s-1",
        cell_methods="time: mean within days",
        description="Total potential evaporation thickness converted to mass flux using a water density of 1000 kg/m³.",
    )

    # Total snow precip in m of water equivalent to flux in kg m-2 s-1 : daily_sum [m/day] * 1000 kg/m³ / 86400 s/day
    prsn = hrly.prsn.resample(time="D").sum() * 1000 / 86400

    swe = hrly.swe.resample(time="D").mean()

    snw = swe * 1000

    # Liquid water equivalent snow thickness [m] to snow thickness in [m] : lwe [m] * 1000 kg/m³ / 300 kg/m³
    snd = snw / 300

    prsn.attrs.update(
        standard_name="solid_precipitation_flux",
        long_name="Mean daily solid precipitation",
        units="kg m-2 s-1",
        cell_methods="time: mean within days",
        description="Total solid precipitation thickness of water equivalent converted to mass flux using a water density of 1000 kg/m³.",
    )
    swe.attrs.update(
        standard_name="lwe_thickness_of_surface_snow_amount",
        long_name="Liquid water equivalent of surface snow amount",
        units="m",
        cell_methods="time: mean within days",
    )
    snw.attrs.update(
        standard_name="surface_snow_amount",
        long_name="Surface snow amount",
        units="kg m-2",
        cell_methods="time: mean within days",
        description="Snow thickness in m of liquid water equivalent converted to snow amount using a water density of 1000 kg/m³.",
    )
    snd.attrs.update(
        standard_name="surface_snow_thickness",
        long_name="Snow depth",
        units="m",
        cell_methods="time: mean within days",
        description="Snow thickness in m of liquid water equivalent converted to snow thickness using a water density of 1000 kg/m³ and a snow density of 300 kg/m³.",
    )

    uas = hrly.uas.resample(time="D").mean()
    vas = hrly.vas.resample(time="D").mean()

    windmag = xc.atmos.wind_speed_from_vector(uas=hrly.uas, vas=hrly.vas)[0]
    sfcWind = windmag.resample(time="D").mean()
    wsgsmax = windmag.resample(time="D").max()

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

    ps = hrly.ps.resample(time="D").mean()
    psl = ps.copy()
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

    dtas = hrly.dtas.resample(time="D").mean()
    dtas.attrs.update(
        standard_name="dew_point_temperature",
        long_name="Daily mean surface dew point temperature",
        units="K",
        cell_methods="time: mean within days",
    )

    rh = (
        convert_units_to(
            xc.atmos.relative_humidity_from_dewpoint(tas=hrly.tas, dtas=hrly.dtas), "1"
        )
        .resample(time="D")
        .mean(keep_attrs=True)
    )
    rh.attrs.update(
        long_name="Daily mean surface relative humidity",
        cell_methods="time: mean within days",
        units="1",
    )

    huss = xc.atmos.specific_humidity(tas=tas, rh=rh, ps=ps)
    huss.attrs.update(
        long_name="Daily mean surface specific humidity",
        cell_methods="time: mean withinh days",
        units="1",
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

    # Final dataset
    ds = xr.Dataset(
        coords={k: v for k, v in hrly.coords.items() if k != "time"},
        attrs={
            "Conventions": "CF-1.8",
            "history": xc.core.formatting.update_history(
                "Spatial extraction, daily aggregation and intermediate computation of raw ERA5 data.",
                raw_nam,
            ),
            "title": "xclim test dataset from ERA5",
            "source": "reanalysis",
            "comment": "Contains modified Copernicus Climate ChangeService information 2020",
            "institution": "ECMWF",
            "references": "doi:10.24381/cds.adbb2d47",
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
        tas=tas,
        tasmax=tasmax,
        tasmin=tasmin,
        pr=pr,
        evspsblpot=evspsblpot,
        prsn=prsn,
        swe=swe,  # snw=snw, snd=snd,
        uas=uas,
        vas=vas,
        wsgsmax=wsgsmax,  # sfcWind=sfcWind,
        tdps=dtas,
        ps=ps,
        hurs=rh,  # psl=psl, huss=huss,
        sund=sund,
        dtas=dtas,
        rh=rh,  # Retro-compatibility with xclim <= 0.26
    )

    # Save it with a fancy save_mfdataset : enables parallel IO. But we merge it anyway at the end.
    base_path = "daily_surface_cancities_1990-1993_{var}.nc"
    objs = []
    paths = []
    for nam, var in ds.data_vars.items():
        objs.append(var.to_dataset())
        paths.append(base_path.format(var=nam))
    delayed = xr.save_mfdataset(objs, paths, compute=False)
    # Isn't save_mfdataset supposed to do this?
    compute(delayed)

    dss = xr.open_mfdataset("daily_surface_cancities_1990-1993_*.nc")
    dss = dss.transpose("location", "time")
    dss.attrs.update(ds.attrs)
    encoding = {"time": {"dtype": "int32"}}
    for var in dss.data_vars.keys():
        encoding[var] = {"dtype": "float32"}
    dss.to_netcdf("daily_surface_cancities_1990-1993.nc", encoding=encoding)
