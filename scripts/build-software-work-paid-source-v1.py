#!/usr/bin/env python3
"""Build the exact deterministic USTAR source archive for Gate D Item 13."""

import argparse
import hashlib
import io
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "test-vectors/software-work-paid-source-v1"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    output = Path(args.output)
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w", format=tarfile.USTAR_FORMAT) as archive:
        for path in sorted(SOURCE.iterdir(), key=lambda item: item.name):
            body = path.read_bytes()
            info = tarfile.TarInfo(path.name)
            info.size = len(body)
            info.mode = 0o444
            info.mtime = 0
            info.uid = info.gid = 0
            info.uname = info.gname = ""
            archive.addfile(info, io.BytesIO(body))
    encoded = buffer.getvalue()
    output.write_bytes(encoded)
    print("sha256:" + hashlib.sha256(encoded).hexdigest())


if __name__ == "__main__":
    main()
