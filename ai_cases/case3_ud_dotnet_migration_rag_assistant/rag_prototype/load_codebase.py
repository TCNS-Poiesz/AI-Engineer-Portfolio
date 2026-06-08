from pathlib import Path
import json


PROJECT_ROOT = Path(__file__).resolve().parents[1]

CODEBASE_ROOT = (
    PROJECT_ROOT
    / "dummy_codebase"
    / "UD_Dummy_Codebase_v0_2"
)

OUTPUTS_DIR = PROJECT_ROOT / "outputs"
OUTPUTS_DIR.mkdir(exist_ok=True)


def detect_layer(file_path: Path) -> str:
    """
    Detects the architectural layer from the folder name.
    This is our first simple metadata step for RAG.
    """
    parts = file_path.parts

    if "Domain" in parts:
        return "Domain"
    if "Services" in parts:
        return "Services"
    if "Infrastructure" in parts:
        return "Infrastructure"
    if "Docs" in parts:
        return "Docs"

    return "Unknown"


def load_code_files():
    """
    Loads all C# files from the dummy codebase and creates a small inventory.
    Later, this will become the first input to our RAG pipeline.
    """
    code_files = []

    for file_path in CODEBASE_ROOT.rglob("*.cs"):
        content = file_path.read_text(encoding="utf-8")

        code_files.append(
            {
                "file_name": file_path.name,
                "relative_path": str(file_path.relative_to(CODEBASE_ROOT)),
                "layer": detect_layer(file_path),
                "extension": file_path.suffix,
                "line_count": len(content.splitlines()),
                "character_count": len(content),
            }
        )

    return code_files


def main():
    print("UD Dummy Codebase RAG Prototype")
    print("--------------------------------")
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Codebase root: {CODEBASE_ROOT}")
    print()

    if not CODEBASE_ROOT.exists():
        print("ERROR: Codebase root not found.")
        return

    code_files = load_code_files()

    print(f"Number of C# files found: {len(code_files)}")
    print()

    for item in code_files:
        print(
            f"{item['layer']:15} | "
            f"{item['file_name']:30} | "
            f"{item['line_count']:4} lines | "
            f"{item['relative_path']}"
        )

    output_path = OUTPUTS_DIR / "codebase_inventory.json"

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(code_files, f, indent=2)

    print()
    print(f"Inventory saved to: {output_path}")


if __name__ == "__main__":
    main()