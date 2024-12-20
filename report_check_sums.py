#!/usr/bin/env python
import hashlib
import math
from pathlib import Path
from typing import Union


def file_size_formatter(i: int, binary: bool = True, precision: int = 1) -> str:
    """Format byte size into an appropriate nomenclature for prettier printing.

    Notes
    -----
    Adapted from https://github.com/Ouranosinc/miranda/blob/main/miranda/storage.py
    """
    _CONVERSIONS = ["B", "k{}B", "M{}B"]

    # Determine the appropriate conversion factor
    base = 1024 if binary else 1000
    if i == 0:
        return "0 B"
    multiple = math.trunc(math.log2(i) / math.log2(base))
    value = i / math.pow(base, multiple)
    suffix = _CONVERSIONS[multiple].format("i" if binary else "")
    return f"{value:.{precision}f} {suffix}"


def file_sha256_checksum(filename: Path) -> str:
    """Return sha256 checksum for file."""
    hash_sha256 = hashlib.sha256()
    with filename.open("rb") as f:
        hash_sha256.update(f.read())
    return hash_sha256.hexdigest()


def valid(path: Path) -> bool:
    """Return True if path should be considered for the creation of sha256 checksum.

    Parameters
    ----------
    path : Path
        The path to the file.
    """

    # Exclude top-level files
    if len(path.parts) == 1:
        return False

    # Exclude hidden files
    if any([p.startswith(".") for p in path.parts]):
        return False

    # Exclude the registry
    if path.name == "registry.txt":
        return False

    if path.suffix == ".py":
        return False

    if path.is_file():
        return True


def main(dry_run: bool = False, readme: Union[str, Path] = "README.md"):
    """Create checksum files."""
    data_folder = Path(".").joinpath("data")
    files = list(filter(valid, data_folder.rglob("**/*")))

    file_checksums_tmp = dict()
    for file in files:
        if valid(file):
            file_checksums_tmp[file] = file_sha256_checksum(file)

    # Sort the dictionary by key
    file_checksums = dict(sorted(file_checksums_tmp.items()))

    # Write the checksums dictionary to the bottom of the README.md file, replacing the existing table
    readme = Path(readme)
    with readme.open() as f:
        lines = f.readlines()

    # Find the index of the existing checksum table
    start_index, end_index = None, None
    for i, line in enumerate(lines):
        if line.startswith("### Files"):
            start_index = i

    # Remove existing checksum table
    if start_index is not None:
        del lines[start_index:]

    i = None
    for i, line in enumerate(lines):
        if line.startswith("## Available datasets"):
            break
    if not i:
        raise ValueError("Could not find '## Available datasets' in README.md")

    # Insert new checksum table
    lines.insert(i + 1, "\n")
    lines.insert(i + 2, "### Files\n")
    lines.insert(i + 3, "\n")
    lines.insert(i + 4, "| File | Size | Checksum |\n")
    lines.insert(i + 5, "| ---- | ---- | -------- |\n")

    for file, checksum in file_checksums.items():
        lines.insert(
            i + 6,
            f"| {file.relative_to(data_folder).as_posix()} "
            f"| {file_size_formatter(file.stat().st_size)} "
            f"| sha256:{checksum} |\n",
        )

    # Remove trailing newline
    if lines[-1].startswith("\n"):
        del lines[-1]

    with readme.open("w", encoding="utf-8") as r:
        r.writelines(lines)
    print(f"Successfully wrote {len(file_checksums)} checksums to {readme}.")

    # Update the data registry file
    registry = Path("data/registry.txt")
    with registry.open("w", encoding="utf-8") as out:
        for file, checksum in file_checksums.items():
            out.write(f"{file.relative_to(data_folder).as_posix()} sha256:{checksum}\n")
    print(f"Successfully wrote {len(file_checksums)} checksums to {registry}.")


if __name__ == "__main__":
    main()