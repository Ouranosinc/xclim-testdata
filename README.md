# xclim-testdata
NetCDF example files used for the testing suite of `xclim`

## Contributing
In order to add a new dataset to the `xclim` testing data, please ensure you perform the following:

1. Create a new branch: `git checkout -b my_new_testdata_branch`
2. Place your dataset within an appropriate subdirectory (or create a new one, e.g. `mkdir data/my_new_data_folder`).
3. Run the sha256 checksum generation script: `python report_check_sums.py`
4. Commit your changes: `git add . && git commit -m "added my_new_testdata"`
5. Open a Pull Request.

To modify an existing dataset, be sure to remove the existing checksum file before running the `report_check_sums.py` script.

If you wish to load data from this repository using `pooch`, this can be done with the following procedure:

* To gather a single file (using the `daily_surface_cancities_1990-1993.nc` file as an example):
```python
import pooch
import xarray as xr

GITHUB_URL = "https://github.com/Ouranosinc/xclim-testdata"
BRANCH_OR_COMMIT_HASH = "main" # or a specific branch name or commit hash

test_data_path = pooch.retrieve(
    url=f"{GITHUB_URL}/raw/{BRANCH_OR_COMMIT_HASH}/data/ERA5/daily_surface_cancities_1990-1993.nc",
    known_hash="sha256:049d54ace3d229a96cc621189daa3e1a393959ab8d988221cfc7b2acd7ab94b2",
)
ds = xr.open_dataset(test_data_path)
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

> [!WARNING]
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

### COPERNICUS (ERA5)

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

* [//]: # (Code below this line is autogenerated by `report_check_sums.py`)
## Available datasets

### Files

| File | Size | Checksum |
| ---- | ---- | -------- |
| uncertainty_partitioning/seattle_avg_tas.csv | 649.4 kiB | sha256:157d6721f9925eec8268848e34548df2b1da50935f247a9b136d251ef53898d7 |
| uncertainty_partitioning/cmip5_tas_pnw_mon.nc | 231.8 kiB | sha256:eeb48765fd430186f3634e7f779b4be45ab3df73e806a4cbb743fefb13279398 |
| uncertainty_partitioning/cmip5_tas_global_mon.nc | 212.4 kiB | sha256:41ba79a43bab169a0487e3f3f66a68a699bef9355a13e26a87fdb65744555cb5 |
| uncertainty_partitioning/cmip5_pr_pnw_mon.nc | 299.9 kiB | sha256:1cdfe74f5bd5cf71cd0737c190277821ea90e4e79de5b37367bf2b82c35a66c9 |
| uncertainty_partitioning/cmip5_pr_global_mon.nc | 251.3 kiB | sha256:7e585c995e95861979fd23dd9346f78a879403ea1d1d15acaa627802b4c5f1f4 |
| sdba/nrcan_1950-2013.nc | 655.0 kiB | sha256:4ce2dcfdac09b028db0f3e348272a496d796c36d4f3c4a412ebcca11449b7237 |
| sdba/ahccd_1950-2013.nc | 654.2 kiB | sha256:7e9a1f61c1d04ca257b09857a82715f1fa3f0550d77f97b7306d4eaaf0c70239 |
| sdba/adjusted_external.nc | 443.8 kiB | sha256:ff325c88eca96844bc85863744e4e08bcdf3d257388255636427ad5e11960d2e |
| sdba/CanESM2_1950-2100.nc | 1.5 MiB | sha256:b41fe603676e70d16c747ec207eb75ec86a39b665de401dcb23b5969ab3e1b32 |
| cmip6/snw_day_CanESM5_historical_r1i1p1f1_gn_19910101-20101231.nc | 491.1 kiB | sha256:05263d68f5c7325439a170990731fcb90d1103a6c5e4f0c0fd1d3a44b92e88e0 |
| cmip6/sic_SImon_CCCma-CanESM5_ssp245_r13i1p2f1_2020.nc | 3.4 MiB | sha256:58a03aa401f80751ad60c8950f14bcf717aeb6ef289169cb5ae3081bb4689825 |
| cmip6/prsn_day_CanESM5_historical_r1i1p1f1_gn_19910101-20101231.nc | 414.6 kiB | sha256:b272ae29fd668cd8a63ed2dc7949a1fd380ec67da98561a4beb34da371439815 |
| cmip6/o3_Amon_GFDL-ESM4_historical_r1i1p1f1_gr1_185001-194912.nc | 845.0 kiB | sha256:cfff189d4986289efb2b88f418cd6d65b26b59355b67b73ca26ac8fa12a9f83f |
| cmip5/tas_Amon_HadGEM2-ES_rcp85_r1i1p1_229912-229912.nc | 9.0 kiB | sha256:3fa657483072d8a04363b8718bc9c4e63e6354617a4ab3d627b25222a4cd094c |
| cmip5/tas_Amon_HadGEM2-ES_rcp85_r1i1p1_227412-229911.nc | 20.4 kiB | sha256:ecf52dc8ac13e04d0b643fc53cc5b367b32e68a311e6718686eaa87088788f98 |
| cmip5/tas_Amon_HadGEM2-ES_rcp85_r1i1p1_224912-227411.nc | 20.4 kiB | sha256:abbe16349870c501335f7f17a5372703f82e8db84f911d29c31783bb07100e6e |
| cmip5/tas_Amon_HadGEM2-ES_rcp85_r1i1p1_222412-224911.nc | 20.4 kiB | sha256:e8d406cc7b87d0899236610e1a9ddecde8279d0d26316114496f159565fb78ba |
| cmip5/tas_Amon_HadGEM2-ES_rcp85_r1i1p1_219912-222411.nc | 20.4 kiB | sha256:21c8db59941ad5481433b69eae5c9efed534c0fc35062ab767a481be9da503b6 |
| cmip5/tas_Amon_HadGEM2-ES_rcp85_r1i1p1_217412-219911.nc | 20.4 kiB | sha256:b6378f082aa6d877fae46be9663e1fe3bf82e0d596aaf501afa6217fcc300878 |
| cmip5/tas_Amon_HadGEM2-ES_rcp85_r1i1p1_214912-217411.nc | 20.4 kiB | sha256:156577a84d82c23f65e019ba58fcdbb7677f1a1128f4745d72441896d0485a11 |
| cmip5/tas_Amon_HadGEM2-ES_rcp85_r1i1p1_212412-214911.nc | 20.4 kiB | sha256:35791a451c392d3dae69ecb789c4a952eff761dddab934389c7d0686feeb6e72 |
| cmip5/tas_Amon_HadGEM2-ES_rcp85_r1i1p1_209912-212411.nc | 20.4 kiB | sha256:54dda14b6c2d8dce8e3a2ff526ffba8cc54bf5de5ace96eec93d060256fd63b6 |
| cmip5/tas_Amon_HadGEM2-ES_rcp85_r1i1p1_208012-209912.nc | 18.1 kiB | sha256:bd7e419c8d6b60dbe700517a16453f787b147bb15cfdebf0519e882fa967f5a0 |
| cmip5/tas_Amon_HadGEM2-ES_rcp85_r1i1p1_205512-208011.nc | 20.8 kiB | sha256:8c18253f8039dfda0aba71f69e5fde367453fc8a239936ee54c6d32db184f3b9 |
| cmip5/tas_Amon_HadGEM2-ES_rcp85_r1i1p1_203012-205511.nc | 20.9 kiB | sha256:31b9a4139574012acbc9d7fdb210af8d00d45119a9b98ebcab67905262543c6d |
| cmip5/tas_Amon_HadGEM2-ES_rcp85_r1i1p1_200512-203011.nc | 20.9 kiB | sha256:3cb54d67bf89cdf542a7b93205785da3800f9a77eaa8436f4ee74af13b248b95 |
| cmip5/tas_Amon_CanESM2_rcp85_r1i1p1_200701-200712.nc | 431.9 kiB | sha256:7471770e4e654997225ab158f2b24aa0510b6f06006fb757b9ea7c0d4a47e1f2 |
| cmip3/tas.sresb1.giss_model_e_r.run1.atm.da.nc | 575.4 kiB | sha256:e709552beeeccafcfe280759edf5477ae5241c698409ca051b0899c16e92c95e |
| SpatialAnalogs/indicators.nc | 1.5 MiB | sha256:3bcbb0e4540d4badc085ac42b9d04a353e815fb55c62271eb73275b889c80a15 |
| SpatialAnalogs/dissimilarity.nc | 367.3 kiB | sha256:200ab9b7d43d41e6db917c54d35b43e3c5853e0df701e44efd5b813e47590110 |
| SpatialAnalogs/NRCAN_SECan_1981-2010.nc | 2.3 MiB | sha256:bde680ddad84106caad3a2e83a70ecdd8138578a70e875d77c2ec6d3ff868fee |
| SpatialAnalogs/CanESM2_ScenGen_Chibougamau_2041-2070.nc | 23.5 kiB | sha256:b6cfc4a963d68b6da8978acd26ffb506f33c9c264d8057badd90bf47cd9f3f3d |
| Raven/q_sim.nc | 661.9 kiB | sha256:f7a0ae73c498235e1c3e7338a184c5ca3729941b81521e606aa60b2c639f6e71 |
| NRCANdaily/nrcan_canada_daily_tasmin_1990.nc | 6.0 MiB | sha256:13d61fc54cdcb4c1617ec777ccbf59575d8fdc24754f914042301bc1b024d7f7 |
| NRCANdaily/nrcan_canada_daily_tasmax_1990.nc | 6.0 MiB | sha256:84880205b798740e37a102c7f40e595d7a4fde6e35fb737a1ef68b8dad447526 |
| NRCANdaily/nrcan_canada_daily_pr_1990.nc | 5.8 MiB | sha256:144479ec7a976cfecb6a10762d128a771356093d72caf5f075508ee86d25a1b0 |
| HadGEM2-CC_360day/tasmin_day_HadGEM2-CC_rcp85_r1i1p1_na10kgrid_qm-moving-50bins-detrend_2095.nc | 1.0 MiB | sha256:5c8fa666603fd68f614d95ac8c5a0dbdfb9f8e2e86666a270516a38526c1aa20 |
| HadGEM2-CC_360day/tasmax_day_HadGEM2-CC_rcp85_r1i1p1_na10kgrid_qm-moving-50bins-detrend_2095.nc | 1.0 MiB | sha256:aa3eb54ea69bb00330de1037a48ac13dbc5b72f346c801d97731dec8260f400c |
| HadGEM2-CC_360day/pr_day_HadGEM2-CC_rcp85_r1i1p1_na10kgrid_qm-moving-50bins-detrend_2095.nc | 1.1 MiB | sha256:c45ff4c17ba9fd92392bb08a7705789071a0bec40bde48f5a838ff12413cc33b |
| FWI/cffdrs_test_wDC.nc | 130.8 kiB | sha256:ebadcad1dd6a1a1e93c29a1143d7caefd46593ea2fbeb721015245981cce90c3 |
| FWI/cffdrs_test_fwi.nc | 23.3 kiB | sha256:147be24e080aa67f17261f61f05a5dfb381a66a23785a327e47e2303667ca3ab |
| FWI/GFWED_sample_2017.nc | 101.1 kiB | sha256:cf3bde795825663894fa7619a028d5a14fee307c623968235f25393f7afe159e |
| EnsembleStats/BCCAQv2+ANUSPLIN300_CNRM-CM5_historical+rcp45_r1i1p1_1970-2050_tg_mean_YS.nc | 296.2 kiB | sha256:623eab96d75d8cc8abd59dfba1c14cfb06fd7c0fe9ce86788d3c8b0891684df2 |
| EnsembleStats/BCCAQv2+ANUSPLIN300_CCSM4_historical+rcp45_r2i1p1_1950-2100_tg_mean_YS.nc | 532.5 kiB | sha256:ca36aafb3c63ddb6bfc8537abb854b71f719505c1145d5c81c3315eb1a13647c |
| EnsembleStats/BCCAQv2+ANUSPLIN300_CCSM4_historical+rcp45_r1i1p1_1950-2100_tg_mean_YS.nc | 532.5 kiB | sha256:9cfa9bc4e81e936eb680a55db428ccd9f0a6d366d4ae2c4a9064bfa5d71e5ca7 |
| EnsembleStats/BCCAQv2+ANUSPLIN300_BNU-ESM_historical+rcp45_r1i1p1_1950-2100_tg_mean_YS.nc | 532.5 kiB | sha256:c796276f563849c31bf388a3beb4a440eeb72062a84b4cf9760c854d1e990ca4 |
| EnsembleStats/BCCAQv2+ANUSPLIN300_ACCESS1-0_historical+rcp45_r1i1p1_1950-2100_tg_mean_YS.nc | 532.5 kiB | sha256:ca0cc893cf91db7c6dfe3df10d605684eabbea55b7e26077c10142d302e55aed |
| EnsembleReduce/TestEnsReduceCriteria.nc | 9.3 kiB | sha256:ae7a70b9d5c54ab072f1cfbfab91d430a41c5067db3c1968af57ea2122cfe8e7 |
| ERA5/daily_surface_cancities_1990-1993.nc | 769.3 kiB | sha256:049d54ace3d229a96cc621189daa3e1a393959ab8d988221cfc7b2acd7ab94b2 |
| CanESM2_365day/tasmin_day_CanESM2_rcp85_r1i1p1_na10kgrid_qm-moving-50bins-detrend_2095.nc | 1.0 MiB | sha256:5d43ec47759bf9d118942277fe8d7c632765c3a0ba02dc828b0610e1f2030a63 |
| CanESM2_365day/tasmax_day_CanESM2_rcp85_r1i1p1_na10kgrid_qm-moving-50bins-detrend_2095.nc | 1.0 MiB | sha256:0c57c56e38a9e5b0623180c3def9406e9ddabbe7b1c01b282f1a34c4a61ea357 |
| CanESM2_365day/pr_day_CanESM2_rcp85_r1i1p1_na10kgrid_qm-moving-50bins-detrend_2095.nc | 1.2 MiB | sha256:16dafec260dd74bf38f87482baa34cc35a1689facfb5557ebfc7d2c928618fc7 |
| CRCM5/tasmax_bby_198406_se.nc | 6.6 MiB | sha256:9a80cc19ed212428ef90ce0cc40790fbf0d1fc301df0abdf578da45843dae93d |
