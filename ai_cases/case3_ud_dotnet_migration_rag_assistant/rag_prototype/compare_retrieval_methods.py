from pathlib import Path

from query_chunks import search_chunks
from query_chunks_vector import search as vector_search


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
OUTPUTS_DIR.mkdir(exist_ok=True)


TEST_QUERIES = [
    "Where is delivery assignment handled?",
    "Where is temporary deliverer access granted?",
    "Where does a delivery become Received?",
    "Where is the LSP alert triggered?",
    "Which files relate to smart-lock access?",
    "Which files would be relevant for a .NET version migration?",
]


def format_keyword_result(result):
    chunk = result["chunk"]

    return {
        "method": "Keyword / rule-based retrieval",
        "score": result["score"],
        "file": chunk["relative_path"],
        "layer": chunk["layer"],
        "domain_area": chunk["domain_area"],
        "lines": f"{chunk['start_line']}-{chunk['end_line']}",
        "snippet": result["snippet"],
    }


def format_vector_result(result):
    chunk = result["chunk"]

    return {
        "method": "Vector-style TF-IDF retrieval",
        "score": round(result["similarity"], 4),
        "file": chunk["relative_path"],
        "layer": chunk["layer"],
        "domain_area": chunk["domain_area"],
        "lines": f"{chunk['start_line']}-{chunk['end_line']}",
        "snippet": result["snippet"],
    }


def compare_for_query(query):
    keyword_results = search_chunks(query, top_k=3)
    vector_results = vector_search(query, top_k=3)

    formatted_keyword_results = [
        format_keyword_result(result) for result in keyword_results
    ]

    formatted_vector_results = [
        format_vector_result(result) for result in vector_results
    ]

    return {
        "query": query,
        "keyword_results": formatted_keyword_results,
        "vector_results": formatted_vector_results,
    }


def create_markdown_report(comparisons):
    report_lines = []

    report_lines.append("# UD Dummy Codebase - Retrieval Comparison Report\n")
    report_lines.append(
        "This report compares two retrieval methods over the UD dummy C# codebase:\n"
    )
    report_lines.append("- Keyword / rule-based retrieval")
    report_lines.append("- Vector-style TF-IDF retrieval\n")

    report_lines.append(
        "The purpose is to understand how different retrieval methods find relevant code chunks before moving to a full LangChain/vector-store RAG setup.\n"
    )

    for comparison in comparisons:
        query = comparison["query"]

        report_lines.append("---\n")
        report_lines.append(f"## Query\n\n{query}\n")

        report_lines.append("## Keyword / rule-based retrieval\n")

        if not comparison["keyword_results"]:
            report_lines.append("No keyword results found.\n")
        else:
            for index, result in enumerate(comparison["keyword_results"], start=1):
                report_lines.append(f"### Keyword result {index}")
                report_lines.append(f"- Score: {result['score']}")
                report_lines.append(f"- File: `{result['file']}`")
                report_lines.append(f"- Layer: {result['layer']}")
                report_lines.append(f"- Domain area: {result['domain_area']}")
                report_lines.append(f"- Lines: {result['lines']}")
                report_lines.append("")
                report_lines.append("```csharp")
                report_lines.append(result["snippet"])
                report_lines.append("```")
                report_lines.append("")

        report_lines.append("## Vector-style TF-IDF retrieval\n")

        if not comparison["vector_results"]:
            report_lines.append("No vector results found.\n")
        else:
            for index, result in enumerate(comparison["vector_results"], start=1):
                report_lines.append(f"### Vector result {index}")
                report_lines.append(f"- Similarity: {result['score']}")
                report_lines.append(f"- File: `{result['file']}`")
                report_lines.append(f"- Layer: {result['layer']}")
                report_lines.append(f"- Domain area: {result['domain_area']}")
                report_lines.append(f"- Lines: {result['lines']}")
                report_lines.append("")
                report_lines.append("```csharp")
                report_lines.append(result["snippet"])
                report_lines.append("```")
                report_lines.append("")

        report_lines.append("## Quick interpretation\n")
        report_lines.append(
            "Keyword retrieval is strong when the query uses exact words that appear in file names, method names, or code comments. "
            "Vector-style retrieval is useful when the query is more conceptual, because it compares weighted term patterns across chunks. "
            "In a full RAG system, both approaches can be combined with real embeddings."
        )
        report_lines.append("")

    return "\n".join(report_lines)


def main():
    print("UD Dummy Codebase - Retrieval Comparison")
    print("----------------------------------------")
    print()

    comparisons = []

    for query in TEST_QUERIES:
        print(f"Comparing retrieval methods for: {query}")
        comparison = compare_for_query(query)
        comparisons.append(comparison)

        keyword_best = comparison["keyword_results"][0] if comparison["keyword_results"] else None
        vector_best = comparison["vector_results"][0] if comparison["vector_results"] else None

        if keyword_best:
            print(f"  Keyword best: {keyword_best['file']}")

        if vector_best:
            print(f"  Vector best:  {vector_best['file']}")

        print()

    report = create_markdown_report(comparisons)
    report_path = OUTPUTS_DIR / "retrieval_comparison_report.md"
    report_path.write_text(report, encoding="utf-8")

    print(f"Comparison report saved to: {report_path}")


if __name__ == "__main__":
    main()