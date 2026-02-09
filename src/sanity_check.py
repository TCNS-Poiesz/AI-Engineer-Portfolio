from __future__ import annotations

import sys
from pathlib import Path
import argparse
import json

def apply_schema(df, schema: dict):
    """
    Apply dataset-specific schema mappings:
    - rename columns (e.g., length_mm -> depth)
    - scale normalized columns (e.g., mm -> m via 0.001)
    """
    if not schema:
        return df

    rename_map = schema.get("rename", {}) or {}
    scale_map = schema.get("scale", {}) or {}

    if rename_map:
        df = df.rename(columns=rename_map)

    for col, factor in scale_map.items():
        if col in df.columns:
            df[col] = df[col].astype(float) * float(factor)

    return df

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
def load_dataset_registry(registry_path: Path) -> dict:
    if not registry_path.exists():
        raise FileNotFoundError(f"Dataset registry not found: {registry_path}")
    with registry_path.open("r", encoding="utf-8") as f:
        return json.load(f)


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
    # CLI options (kept minimal for demo friendliness)
    parser = argparse.ArgumentParser(description="TCNS Portfolio sanity check")
    parser.add_argument("--list", action="store_true", help="List available datasets")
    parser.add_argument("--dataset", type=str, default=None, help="Dataset id from datasets.json")
    args = parser.parse_args()

    # Dataset registry (config, not hardcoding)
    registry_path = data_dir / "datasets.json"
    registry = load_dataset_registry(registry_path)
    datasets = registry.get("datasets", [])

    if args.list:
        print("\nAvailable datasets:")
        for d in datasets:
            ds_id = d.get("id", "<missing id>")
            ds_file = d.get("file", "<missing file>")
            ds_desc = d.get("description", "")
            print(f"- {ds_id}: {ds_desc} ({ds_file})")
        return 0

    try:
        if args.dataset:
            matches = [d for d in datasets if d.get("id") == args.dataset]
            if not matches:
                print(f"ERROR: Unknown dataset id: {args.dataset}")
                print("Use --list to see available datasets.")
                return 7

            chosen = matches[0]
            csv_path = data_dir / chosen["file"]
            if not csv_path.exists():
                print("ERROR: Dataset file missing:")
                print(f"  {csv_path}")
                return 8
        else:
            csv_path = pick_dataset_csv(data_dir)
    except Exception as e:
        print("ERROR: Could not select a dataset CSV.")
        print(f"Reason: {e}")
        return 4


    print(f"Dataset:   {csv_path.relative_to(repo_root)}")

    try:
        df = pd.read_csv(csv_path)
        df = apply_schema(df, chosen.get("schema", {}))
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
