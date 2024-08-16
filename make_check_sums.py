#!/usr/bin/env python
import hashlib
from pathlib import Path


def file_md5_checksum(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb", encoding="utf-8") as f:
        hash_md5.update(f.read())
    return hash_md5.hexdigest()


def main(dry_run=False):
    files = list(Path().cwd().joinpath("data").rglob("*.nc"))
    files.extend(Path().cwd().joinpath("data").rglob("*.csv"))

    for ncf in files:
        md5 = Path(f"{ncf}.md5")
        if not md5.exists():
            if dry_run:
                print(f"Create checksum for {ncf}")
                continue

            with open(md5, "w", encoding="utf-8") as out:
                out.write(file_md5_checksum(ncf))


if __name__ == '__main__':
    main()
