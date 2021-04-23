#!/usr/bin/env python
import hashlib
from pathlib import Path


def file_md5_checksum(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        hash_md5.update(f.read())
    return hash_md5.hexdigest()


def main():
    files = Path().cwd().rglob('*.nc')
    for ncf in files:
        outf = f'{ncf.as_posix()}.md5'
        with open(outf, 'w') as f:
            f.write(file_md5_checksum(ncf))


if __name__ == '__main__':
    main()
