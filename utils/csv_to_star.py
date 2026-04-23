#!/usr/bin/env python3

import argparse
import os

import pandas as pd
import starfile


def main():
    parser = argparse.ArgumentParser(
        description="Convert a CSV file into a RELION STAR file using the starfile package."
    )
    parser.add_argument("input_csv", help="Path to the input .csv file")
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Path to the output .star file. Defaults to the CSV filename with a .star suffix.",
    )
    parser.add_argument(
        "-b",
        "--block-name",
        default="global",
        help="STAR data block name to use. Defaults to 'global' to match the example in utils.",
    )
    args = parser.parse_args()

    input_csv = os.path.abspath(args.input_csv)
    output_star = (
        os.path.abspath(args.output)
        if args.output
        else os.path.splitext(input_csv)[0] + ".star"
    )

    df = pd.read_csv(input_csv)

    if df.empty:
        raise ValueError("The input CSV has no rows.")

    starfile.write({args.block_name: df}, output_star, overwrite=True)
    print(f"Wrote {output_star}")


if __name__ == "__main__":
    main()
