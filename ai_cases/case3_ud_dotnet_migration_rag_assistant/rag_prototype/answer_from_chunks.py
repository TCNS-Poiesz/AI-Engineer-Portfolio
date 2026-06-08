from pathlib import Path
import sys

from query_chunks_vector import search


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
OUTPUTS_DIR.mkdir(exist_ok=True)


def infer_answer_focus(query):
    query_lower = query.lower()

    if "assignment" in query_lower or "lsp" in query_lower:
        return (
            "The question appears to be about delivery assignment and LSP workflow. "
            "The most relevant files are likely service-layer files because they coordinate business actions."
        )

    if "access" in query_lower or "deliverer" in query_lower or "lock" in query_lower:
        return (
            "The question appears to be about access control. "
            "The most relevant files are likely AccessControlService.cs and AccessRight.cs."
        )

    if "received" in query_lower or "delivered" in query_lower or "status" in query_lower:
        return (
            "The question appears to be about delivery status transitions. "
            "The most relevant files are likely Delivery.cs and DeliveryStatusService.cs."
        )

    if "alert" in query_lower or "notify" in query_lower:
        return (
            "The question appears to be about notifications or alerts. "
            "The most relevant file is likely AlertService.cs."
        )

    return (
        "The question appears to be a general codebase question. "
        "The retrieved chunks below provide the best available local evidence."
    )


def create_answer_report(query, results):
    report_lines = []

    report_lines.append("# UD Dummy Codebase - RAG-Style Answer\n")
    report_lines.append(f"## Question\n\n{query}\n")

    report_lines.append("## Short answer\n")
    report_lines.append(infer_answer_focus(query))
    report_lines.append("")

    if not results:
        report_lines.append("No relevant chunks were found.")
        return "\n".join(report_lines)

    best_chunk = results[0]["chunk"]

    report_lines.append("## Best matching source\n")
    report_lines.append(f"- File: `{best_chunk['relative_path']}`")
    report_lines.append(f"- Layer: {best_chunk['layer']}")
    report_lines.append(f"- Domain area: {best_chunk['domain_area']}")
    report_lines.append(f"- Lines: {best_chunk['start_line']}-{best_chunk['end_line']}")
    report_lines.append("")

    report_lines.append("## Evidence from retrieved code\n")

    for index, result in enumerate(results, start=1):
        chunk = result["chunk"]

        report_lines.append(f"### Evidence {index}")
        report_lines.append(f"- Similarity: {result['similarity']:.4f}")
        report_lines.append(f"- File: `{chunk['relative_path']}`")
        report_lines.append(f"- Layer: {chunk['layer']}")
        report_lines.append(f"- Domain area: {chunk['domain_area']}")
        report_lines.append(f"- Lines: {chunk['start_line']}-{chunk['end_line']}")
        report_lines.append("")
        report_lines.append("```csharp")
        report_lines.append(result["snippet"])
        report_lines.append("```")
        report_lines.append("")

    report_lines.append("## Interpretation\n")
    report_lines.append(
        "This answer is grounded only in the retrieved dummy codebase chunks. "
        "In a full RAG assistant, this retrieval step would be followed by an LLM that writes a more fluent explanation using these same retrieved sources."
    )

    return "\n".join(report_lines)


def main():
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = input("Ask a question about the UD dummy codebase: ")

    print()
    print("UD Dummy Codebase - RAG-Style Answer")
    print("------------------------------------")
    print(f"Question: {query}")
    print()

    results = search(query, top_k=5)

    if not results:
        print("No matching chunks found.")
        return

    best_chunk = results[0]["chunk"]

    print("Short answer:")
    print(infer_answer_focus(query))
    print()
    print("Best matching source:")
    print(f"File: {best_chunk['relative_path']}")
    print(f"Layer: {best_chunk['layer']}")
    print(f"Domain area: {best_chunk['domain_area']}")
    print(f"Lines: {best_chunk['start_line']}-{best_chunk['end_line']}")
    print()

    report = create_answer_report(query, results)
    report_path = OUTPUTS_DIR / "rag_answer.md"
    report_path.write_text(report, encoding="utf-8")

    print(f"RAG-style answer saved to: {report_path}")


if __name__ == "__main__":
    main()