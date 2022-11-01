# xclim-testdata
NetCDF example files used for the testing suite of Xclim

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
