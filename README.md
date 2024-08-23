# xclim-testdata
NetCDF example files used for the testing suite of `xclim`

## Contributing
In order to add a new dataset to the `xclim` testing data, please ensure you perform the following:

1. Create a new branch: `git checkout -b my_new_testdata_branch`
2. Place your dataset within an appropriate subdirectory (or create a new one: `mkdir data/my_testdata_contribution`).
3. Run the registry generation script: `python make_check_sums.py`
4. Commit your changes: `git add testdata_contribution && git commit -m "added my_new_testdata"`
5. Open a Pull Request.

To modify an existing dataset, be sure to remove the existing checksum file before running the `make_check_sums.py` script.

If you wish to perform preliminary tests against the dataset using `xclim`, this can be done with the following procedure:
```python
from xclim.testing import open_dataset


ds = open_dataset(
    "testdata_contribution/my_netcdf.nc",
    github_url="https://github.com/my_username/xclim-testdata/data",
    branch="my_new_testdata_branch",
    checksum="sha256:1234567890abcdef",
)
```

> [!NOTE]
> The following options only work for branches based on `Ouranosinc/xclim-testdata`, not forks.

If you wish to run the entire `xclim` testing suite locally against your branch, this can be set via an environment variable:
```shell
$ export XCLIM_TESTDATA_BRANCH="my_new_testdata_branch"

$ pytest xclim
# or, alternatively:
$ tox
```

If you wish to run the entire `xclim` testing suite on the `Ouranosinc/xclim` GitHub Workflows (CI) against your branch,
this can be set via an environment variable default in the `.github/workflows/main.yml` workflow configuration:
```yaml
env:
  XCLIM_TESTDATA_BRANCH: my_new_testdata_branch
```

> ![WARNING]
> Be aware that modifying this variable to a value other than the latest tagged version of `xclim-testdata`
> will trigger a GitHub Workflow that will block merging of your Pull Request until changes are effected.

## Versioning
When updating a dataset in `xclim-testdata` using a development branch and Pull Request,
once changes have been merged to the `main` branch, you should tag a new version of `xclim-testdata`. 

The version tag of `xclim-testdata` should follow a [calendar versioning](https://calver.org/) scheme
(i.e. version string follows from `vYYYY.MM.DD-r#`) reflecting the date of the tag creation, with modifiers if required.

## Data Information

### CMIP(3/5/6)

* About the CMIP3 project: https://wcrp-cmip.org/cmip3/
* About the CMIP5 project: https://wcrp-cmip.org/cmip5/
* About the CMIP6 project: https://wcrp-cmip.org/cmip6/

* For raw data access: https://pcmdi.llnl.gov/mips/cmip5/data-access-getting-started.html
* Data access: https://pcmdi.llnl.gov/mips/cmip5/data-portal.html
* For information about the NASA GISS-ER model: https://data.giss.nasa.gov/modelE/cmip3/

### ECCC (AHCCD: Adjusted and Homogenized Canadian Climate Data)

* About the data: https://www.canada.ca/en/environment-climate-change/services/climate-change/canadian-centre-climate-services/display-download/technical-documentation-adjusted-climate-data.html
* Data license: https://open.canada.ca/en/open-government-licence-canada

### ERA5

* About ERA5: https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels?tab=overview
* Copernicus Data license: https://cds.climate.copernicus.eu/api/v2/terms/static/licence-to-use-copernicus-products.pdf

### NA-CORDEX (CRCM5)

* About NA-CORDEX: https://na-cordex.org/
* For more information about NA-CORDEX models: https://na-cordex.org/rcm-characteristics.html

### NASA (GFWED)

* About the GFWED project: https://data.giss.nasa.gov/impacts/gfwed/
* GFWED data access: https://portal.nccs.nasa.gov/datashare/GlobalFWI/

### NRCAN (NRCan Canada Daily Gridded 10Km and CFFDRS)

* Gridded Daily 10Km data and data access: https://cfs.nrcan.gc.ca/projects/3/4
* About the CFFDRS project: https://cwfis.cfs.nrcan.gc.ca/background/summary/fdr

### OURANOS (Generic Climate Scenarios)

* For data access and terms of use: https://www.ouranos.ca/portraits-climatiques/#/
* About the Generic Scenarios project: https://www.ouranos.ca/wp-content/uploads/FicheLoganGauvin2016_EN.pdf

### PCIC (BCCAQv2)

* About the data and data access information: https://www.pacificclimate.org/data/statistically-downscaled-climate-scenarios

### Regional Variance Dataset

* Data Repository: https://github.com/thenaomig/regionalVariance/
* Goldenson, N., Mauger, G., Leung, L. R., Bitz, C. M., & Rhines, A. (2018). Effects of Ensemble Configuration on Estimates of Regional Climate Uncertainties. Geophysical Research Letters, 45(2), 926–934. https://doi.org/10.1002/2017GL076297

### Lafferty-Sriver Uncertainty Dataset

* Data Repository: https://github.com/david0811/lafferty-sriver_2023_npjCliAtm
  * DOI: https://doi.org/10.5281/zenodo.8244794
* Lafferty, D.C. & Sriver, R.L. Downscaling and bias-correction contribute considerable uncertainty to local climate projections in CMIP6. npj Clim Atmos Sci 6, 158 (2023). https://doi.org/10.1038/s41612-023-00486-0