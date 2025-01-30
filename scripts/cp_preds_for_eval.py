import argparse
import shutil
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Copy predictions to match TrackEval directory structure."
    )
    parser.add_argument(
        "--input-dir",
        "-i",
        type=str,
        required=True,
        help="Path to predictions directory.",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        type=str,
        help="Path to output directory.",
        default="eval_inputs",
    )
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)

    print(f"Starting to copy predictions from {input_dir} to {output_dir}.")

    if not input_dir.is_dir():
        raise ValueError(f"{input_dir} is not a directory.")

    subset_name = input_dir.stem
    data_dir = output_dir / "res" / subset_name / "OC-SORT" / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    for file in input_dir.iterdir():
        if file.is_file():
            dest = data_dir / file.name
            shutil.copy(file, dest)
            print(f"Copying {file} to {dest}.")

    print(f"Done. Predictions are in {data_dir}.")


if __name__ == "__main__":
    main()
