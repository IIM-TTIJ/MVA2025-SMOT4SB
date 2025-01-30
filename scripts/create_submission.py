import argparse
import zipfile
from datetime import datetime
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Create a submission zip file")
    parser.add_argument(
        "--input-dir",
        "-i",
        type=str,
        required=True,
        help="Path to predictions directory.",
    )
    parser.add_argument(
        "--output-file",
        "-o",
        type=str,
        help="Path to output submission file. defaults to <timestamp>.zip.",
    )
    parser.add_argument("--subset", "-s", type=str)
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    if not input_dir.is_dir():
        raise ValueError(f"{input_dir} is not a directory.")

    if args.output_file is None:
        output_file = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.zip"
    else:
        output_file = args.output_file

    if args.subset is None:
        subset = input_dir.stem
    else:
        subset = args.subset

    print(f"Zipping {input_dir}.")

    parent_dir = Path(subset) / "OC-SORT" / "data"
    with zipfile.ZipFile(output_file, "w") as zf:
        for file in input_dir.iterdir():
            if file.is_file():
                zf.write(file, parent_dir / file.name)
                print(f"Added {file.name} to {output_file}")

    print(f"Done. Saved to {output_file}.")


if __name__ == "__main__":
    main()
