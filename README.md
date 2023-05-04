# xclim-testdata
NetCDF example files used for the testing suite of `xclim`

## Contributing
In order to add a new dataset to the `xclim` testing data, please ensure you perform the following:

1. Create a new branch: `git checkout -b my_new_testdata_branch`
2. Place your dataset within an appropriate subdirectory (or create a new one: `mkdir testdata_contribution`).
3. Run the md5 checksum generation script: `python make_check_sums.py`
4. Commit your changes: `git add testdata_contribution && git commit -m "added my_new_testdata"`
5. Open a Pull Request.

To modify an existing dataset, be sure to remove the existing checksum file before running the `make_check_sums.py` script.

If you wish to perform preliminary tests against the dataset using `xclim`, this can be done with the following procedure:
```python
from xclim.testing import open_dataset


ds = open_dataset(
    "testdata_contribution/my_netcdf.nc",
    github_url="https://github.com/my_username/raven-testdata",
    branch="my_new_testdata_branch"
)
```

> **Note**
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

> **Note**
> Be aware that modifying this variable to a value other than the latest tagged version of `xclim-testdata`
> will trigger a GitHub Workflow that will block merging of your Pull Request until changes are effected.

## Versioning
When updating a dataset in `xclim-testdata` using a development branch and Pull Request,
once changes have been merged to the `main` branch, you should tag a new version of `xclim-testdata`. 

The version tag of `xclim-testdata` should follow a [calendar versioning](https://calver.org/) scheme
(i.e. version string follows from `vYYYY.MM.DD-r#`) reflecting the date of the tag creation, with modifiers if required.
