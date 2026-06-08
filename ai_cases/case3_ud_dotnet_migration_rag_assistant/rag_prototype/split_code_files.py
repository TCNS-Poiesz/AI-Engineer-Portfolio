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

CHUNK_MAX_LINES = 45
CHUNK_OVERLAP_LINES = 8


def detect_layer(file_path: Path) -> str:
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


def detect_domain_area(file_path: Path) -> str:
    file_name = file_path.stem.lower()

    if "delivery" in file_name:
        return "Delivery"
    if "access" in file_name:
        return "AccessControl"
    if "lock" in file_name:
        return "SmartLock"
    if "space" in file_name or "box" in file_name:
        return "DeliverySpace"
    if "alert" in file_name or "notification" in file_name:
        return "Alerts"
    if "organisation" in file_name or "user" in file_name:
        return "IdentityAndRoles"

    return "General"


def split_text_by_lines(lines, max_lines=CHUNK_MAX_LINES, overlap_lines=CHUNK_OVERLAP_LINES):
    chunks = []
    start = 0

    while start < len(lines):
        end = min(start + max_lines, len(lines))
        chunk_lines = lines[start:end]

        chunks.append(
            {
                "start_line": start + 1,
                "end_line": end,
                "content": "".join(chunk_lines),
            }
        )

        if end == len(lines):
            break

        start = end - overlap_lines

    return chunks


def load_and_split_code_files():
    all_chunks = []

    for file_path in CODEBASE_ROOT.rglob("*.cs"):
        content = file_path.read_text(encoding="utf-8")
        lines = content.splitlines(keepends=True)

        file_chunks = split_text_by_lines(lines)

        for chunk_index, chunk in enumerate(file_chunks, start=1):
            all_chunks.append(
                {
                    "chunk_id": f"{file_path.stem}_chunk_{chunk_index}",
                    "file_name": file_path.name,
                    "relative_path": str(file_path.relative_to(CODEBASE_ROOT)),
                    "layer": detect_layer(file_path),
                    "domain_area": detect_domain_area(file_path),
                    "extension": file_path.suffix,
                    "start_line": chunk["start_line"],
                    "end_line": chunk["end_line"],
                    "line_count": chunk["end_line"] - chunk["start_line"] + 1,
                    "character_count": len(chunk["content"]),
                    "content": chunk["content"],
                }
            )

    return all_chunks


def create_markdown_report(chunks):
    report_lines = []
    report_lines.append("# UD Dummy Codebase Chunk Report\n")
    report_lines.append("This report shows the first RAG-ready chunks created from the dummy C# codebase.\n")
    report_lines.append(f"Total chunks: {len(chunks)}\n")

    by_layer = {}

    for chunk in chunks:
        by_layer.setdefault(chunk["layer"], 0)
        by_layer[chunk["layer"]] += 1

    report_lines.append("## Chunks by layer\n")

    for layer, count in sorted(by_layer.items()):
        report_lines.append(f"- {layer}: {count}")

    report_lines.append("\n## Chunk inventory\n")

    for chunk in chunks:
        report_lines.append(
            f"- `{chunk['chunk_id']}` | "
            f"{chunk['layer']} | "
            f"{chunk['domain_area']} | "
            f"`{chunk['relative_path']}` | "
            f"lines {chunk['start_line']}-{chunk['end_line']}"
        )

    return "\n".join(report_lines)


def main():
    print("UD Dummy Codebase - Split Code Files")
    print("------------------------------------")
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Codebase root: {CODEBASE_ROOT}")
    print()

    if not CODEBASE_ROOT.exists():
        print("ERROR: Codebase root not found.")
        return

    chunks = load_and_split_code_files()

    print(f"Number of chunks created: {len(chunks)}")
    print()

    for chunk in chunks[:10]:
        print(
            f"{chunk['chunk_id']:35} | "
            f"{chunk['layer']:15} | "
            f"{chunk['domain_area']:18} | "
            f"lines {chunk['start_line']}-{chunk['end_line']} | "
            f"{chunk['relative_path']}"
        )

    chunks_output_path = OUTPUTS_DIR / "code_chunks.json"

    with chunks_output_path.open("w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2)

    report_output_path = OUTPUTS_DIR / "chunk_report.md"
    report_output_path.write_text(create_markdown_report(chunks), encoding="utf-8")

    print()
    print(f"Chunks saved to: {chunks_output_path}")
    print(f"Report saved to: {report_output_path}")


if __name__ == "__main__":
    main()