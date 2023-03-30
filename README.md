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
When updating a dataset in `xclim-testdata` using a development branch and Pull Request, once changes have been merged
to the `main` branch, you should tag a new version of `xclim-testdata`. The version tag of `xclim-testdata` is loosely tied
to that of `xclim`, and should represent the `xclim` version (**stable**, i.e. version string not ending in `-dev`)
that is compatible with `xclim-testdata`.

> **Warning** 
> In the event that multiple Pull Requests occur for `xclim-testdata` between two stable versions 
> (e.g. one for `xclim @ 1.2.3-dev` and another for `xclim @ 1.2.5-dev`),
> the `xclim-tesdata` tag (e.g. `xclim-testdata @ 1.3.0`) should be replaced with the commit reflecting the most recent changes.
