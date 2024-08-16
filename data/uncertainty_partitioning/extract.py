import pandas as pd
import xarray as xr
import numpy as np
from pathlib import Path

def load_test_data(var="tas", region="pnw"):
    """Load data from https://github.com/thenaomig/regionalVariance.

    Accessed 2022-12-16 (399b4b8)
    """
    scens = ("historical", "rcp26", "rcp45", "rcp60", "rcp85")
    path = Path("/tmp/regionalVariance/timeSeries")
    fn_pat = "timeSeries_{var}_{region}_Monthly_{scen}.csv"
    def read(var, region, scen):
        fn = fn_pat.format(var=var, region=region, scen=scen)
        df = pd.read_csv(path / fn, index_col=0, header=[0, 1], parse_dates=True)
        da = df.stack([0, 1]).to_xarray().astype(np.float32)
        da.name = var
        return da

    index = pd.Index(scens, name="scen")
    out = xr.concat([read(var, region, scen) for scen in scens], dim=index).resample(time="Y").mean()
    out.attrs["source"] = "https://github.com/thenaomig/regionalVariance"
    out.attrs["original_filenames"] = ", ".join([fn_pat.format(var=var, region=region, scen=scen) for scen in scens])
    out.attrs["date_accessed"] = "2022-12-20"
    return out


def save_test_data(path="~/src/xclim-testdata/uncertainty_partitioning/"):
    """Save to netCDF."""

    for var in ["pr", "tas"]:
        for region in ["global", "pnw"]:
            da = load_test_data(var, region)
            da.to_netcdf(Path(path) / f"cmip5_{var}_{region}_mon.nc",
                         encoding={var: {"zlib": True, "complevel": 8}})
            da.close()
