from __future__ import annotations

import sys
from pathlib import Path


def find_repo_root(start: Path) -> Path:
    current = start.resolve()
    for parent in [current, *current.parents]:
        if (parent / ".git").exists():
            return parent
    return current


def pick_dataset_csv(data_dir: Path) -> Path:
    csvs = sorted(data_dir.glob("*.csv"))
    if not csvs:
        raise FileNotFoundError(f"No .csv files found in: {data_dir}")
    return csvs[0]


def main() -> int:
    print("=== TCNS Portfolio — Sanity Check ===")
    print(f"Python: {sys.version.split()[0]}")

    try:
        import pandas as pd
    except Exception as e:
        print("ERROR: Could not import pandas.")
        print(f"Reason: {e}")
        return 2

    print(f"pandas: {pd.__version__}")

    repo_root = find_repo_root(Path(__file__).parent)
    print(f"Repo root: {repo_root}")

    data_dir = repo_root / "ai_cases" / "data"
    if not data_dir.exists():
        print("ERROR: Expected data directory not found:")
        print(f"  {data_dir}")
        return 3

    print(f"Data dir:  {data_dir}")

    try:
        csv_path = pick_dataset_csv(data_dir)
    except Exception as e:
        print("ERROR: Could not select a dataset CSV.")
        print(f"Reason: {e}")
        return 4

    print(f"Dataset:   {csv_path.relative_to(repo_root)}")

    try:
        df = pd.read_csv(csv_path)
        expected_cols = {"parcel_id", "width", "depth", "height", "stackable"}
        missing = expected_cols - set(df.columns)
        if missing:
            print("ERROR: Dataset missing expected columns:")
            print(f"Missing: {sorted(missing)}")
            print(f"Found:   {df.columns.tolist()}")
            return 6

    except Exception as e:
        print("ERROR: Failed to read CSV with pandas.")
        print(f"Reason: {e}")
        return 5

    print(f"Shape:     {df.shape[0]} rows x {df.shape[1]} cols")
    print("Columns:   " + ", ".join(map(str, df.columns.tolist())))

    print("\nPreview (first 5 rows):")
    print(df.head(5).to_string(index=False))

    print("\n✅ Sanity check OK — environment + data load working.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
