#!/usr/bin/env python3

import argparse
import os
import re

import pandas as pd
import starfile


def sanitize_block_name(name):
    return re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("_") or "block"


def write_csv(df, output_path):
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"Expected a pandas DataFrame, got {type(df).__name__}")
    df.to_csv(output_path, index=False)
    print(f"Wrote {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Export a RELION STAR file into CSV file(s) using the starfile package."
    )
    parser.add_argument("input_star", help="Path to the input .star file")
    parser.add_argument(
        "-o",
        "--output-dir",
        default=None,
        help="Directory for exported CSV files. Defaults to the STAR file directory.",
    )
    args = parser.parse_args()

    input_star = os.path.abspath(args.input_star)
    output_dir = os.path.abspath(args.output_dir) if args.output_dir else os.path.dirname(input_star)
    os.makedirs(output_dir, exist_ok=True)

    star_data = starfile.read(input_star)
    base_name = os.path.splitext(os.path.basename(input_star))[0]

    if isinstance(star_data, pd.DataFrame):
        output_path = os.path.join(output_dir, f"{base_name}.csv")
        write_csv(star_data, output_path)
        return

    if isinstance(star_data, dict):
        for block_name, df in star_data.items():
            safe_block_name = sanitize_block_name(block_name)
            output_path = os.path.join(output_dir, f"{base_name}_{safe_block_name}.csv")
            write_csv(df, output_path)
        return

    raise TypeError(f"Unsupported STAR content type: {type(star_data).__name__}")


if __name__ == "__main__":
    main()
