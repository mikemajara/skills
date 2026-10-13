#!/usr/bin/env python3
"""Check final signed comment text from stdin without posting or changing it."""

import argparse
import json
import sys


def measure(text, units):
    if units == "utf16":
        return len(text.encode("utf-16-le")) // 2
    if units == "utf8":
        return len(text.encode("utf-8"))
    if units == "codepoints":
        return len(text)
    raise ValueError(f"Unsupported counting unit: {units}")


def positive_int(value):
    limit = int(value)
    if limit < 1:
        raise argparse.ArgumentTypeError("limit must be positive")
    return limit


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=positive_int, default=3500)
    parser.add_argument(
        "--units", choices=("utf16", "utf8", "codepoints"), default="utf16"
    )
    args = parser.parse_args(argv)
    length = measure(sys.stdin.read(), args.units)
    fits = length <= args.limit
    print(json.dumps({
        "fits": fits,
        "length": length,
        "limit": args.limit,
        "units": args.units,
    }))
    return 0 if fits else 1


if __name__ == "__main__":
    sys.exit(main())
