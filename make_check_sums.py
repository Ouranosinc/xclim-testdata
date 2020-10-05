#!/usr/bin/env python

from pathlib import Path

from xarray.tutorial import file_md5_checksum


def main():
    files = Path().cwd().rglob('*.nc')
    for ncf in files:
        outf = f'{ncf.as_posix()}.md5'
        with open(outf, 'w') as f:
            f.write(file_md5_checksum(ncf))

if __name__ == '__main__':
    main()
