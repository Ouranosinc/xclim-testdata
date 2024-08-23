#!/usr/bin/env python
import hashlib
from pathlib import Path


def file_sha256_checksum(fname):
    hash_sha256 = hashlib.sha256()
    with open(fname, "rb") as f:
        hash_sha256.update(f.read())
    return hash_sha256.hexdigest()


def main(dry_run=False):
    data = Path().cwd().joinpath("data")
    files = []
    files.extend(data.rglob("*.nc"))
    files.extend(data.rglob("*.csv"))

    registry = Path("data/registry.txt")
    with open(registry, "w", encoding="utf-8") as out:
        for f in files:
            out.write(f"{f.relative_to(Path(__file__).parent.joinpath('data'))} sha256:{file_sha256_checksum(f)}\n")


if __name__ == '__main__':
    main()
