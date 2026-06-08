from pathlib import Path
import json
import re
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
CHUNKS_PATH = OUTPUTS_DIR / "code_chunks.json"


def normalize_text(text):
    return text.lower()


def tokenize(text):
    return re.findall(r"[a-zA-Z0-9_]+", text.lower())


def expand_query_terms(query):
    """
    Very small, transparent query expansion.
    This helps business-language questions find code-language chunks.
    """
    terms = set(tokenize(query))

    synonym_map = {
        "delivery": ["delivery", "deliveries"],
        "assignment": ["assignment", "assign", "assigned", "lsp"],
        "assigned": ["assignment", "assign", "assigned", "lsp"],
        "lsp": ["lsp", "logistics", "provider"],
        "access": ["access", "accessright", "accessrights"],
        "temporary": ["temporary", "validfrom", "validuntil"],
        "permanent": ["permanent", "ownerpermanentaccess"],
        "receiver": ["receiver", "received", "owner"],
        "received": ["received", "markreceived"],
        "delivered": ["delivered", "markdelivered"],
        "status": ["status", "deliverystatus"],
        "space": ["space", "deliveryspace", "smartbox"],
        "box": ["box", "smartbox", "space"],
        "lock": ["lock", "smartlock"],
        "alert": ["alert", "notify", "notification"],
        "failed": ["failed", "fail", "failure", "failurereason"],
        "cancelled": ["cancelled", "cancel", "cancellationreason"],
    }

    for term in list(terms):
        if term in synonym_map:
            terms.update(synonym_map[term])

    return terms


def load_chunks():
    if not CHUNKS_PATH.exists():
        raise FileNotFoundError(
            f"Could not find {CHUNKS_PATH}. "
            "Please run split_code_files.py first."
        )

    with CHUNKS_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def score_chunk(chunk, query, query_terms):
    """
    Simple retrieval scoring.
    Later, we can replace or complement this with embeddings.
    """
    content = normalize_text(chunk["content"])
    file_name = normalize_text(chunk["file_name"])
    relative_path = normalize_text(chunk["relative_path"])
    layer = normalize_text(chunk["layer"])
    domain_area = normalize_text(chunk["domain_area"])

    metadata_text = " ".join([file_name, relative_path, layer, domain_area])

    score = 0

    # Exact phrase in content is valuable.
    if normalize_text(query) in content:
        score += 20

    # Terms in file/path/domain metadata are highly useful for code search.
    for term in query_terms:
        if term in metadata_text:
            score += 5
        if term in content:
            score += 2

    # Small boost for service files when looking for where something is handled.
    if "where" in query_terms or "handled" in query_terms:
        if chunk["layer"] == "Services":
            score += 3

    return score


def make_snippet(content, query_terms, max_chars=600):
    content_lower = content.lower()

    first_match_index = None

    for term in query_terms:
        index = content_lower.find(term.lower())
        if index != -1:
            if first_match_index is None or index < first_match_index:
                first_match_index = index

    if first_match_index is None:
        return content[:max_chars].strip()

    start = max(0, first_match_index - 180)
    end = min(len(content), start + max_chars)

    return content[start:end].strip()


def search_chunks(query, top_k=5):
    chunks = load_chunks()
    query_terms = expand_query_terms(query)

    results = []

    for chunk in chunks:
        score = score_chunk(chunk, query, query_terms)

        if score > 0:
            results.append(
                {
                    "score": score,
                    "chunk": chunk,
                    "snippet": make_snippet(chunk["content"], query_terms),
                }
            )

    results.sort(key=lambda item: item["score"], reverse=True)

    return results[:top_k]


def save_report(query, results):
    report_lines = []
    report_lines.append("# Retrieval Results\n")
    report_lines.append(f"Query: {query}\n")

    for index, result in enumerate(results, start=1):
        chunk = result["chunk"]

        report_lines.append(f"## Result {index}")
        report_lines.append(f"- Score: {result['score']}")
        report_lines.append(f"- File: `{chunk['relative_path']}`")
        report_lines.append(f"- Layer: {chunk['layer']}")
        report_lines.append(f"- Domain area: {chunk['domain_area']}")
        report_lines.append(f"- Lines: {chunk['start_line']}-{chunk['end_line']}")
        report_lines.append("")
        report_lines.append("```csharp")
        report_lines.append(result["snippet"])
        report_lines.append("```")
        report_lines.append("")

    report_path = OUTPUTS_DIR / "retrieval_results.md"
    report_path.write_text("\n".join(report_lines), encoding="utf-8")

    return report_path


def main():
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = input("Ask a question about the UD dummy codebase: ")

    print()
    print("UD Dummy Codebase - Query Chunks")
    print("--------------------------------")
    print(f"Query: {query}")
    print()

    results = search_chunks(query)

    if not results:
        print("No matching chunks found.")
        return

    for index, result in enumerate(results, start=1):
        chunk = result["chunk"]

        print(f"Result {index}")
        print(f"Score: {result['score']}")
        print(f"File: {chunk['relative_path']}")
        print(f"Layer: {chunk['layer']}")
        print(f"Domain area: {chunk['domain_area']}")
        print(f"Lines: {chunk['start_line']}-{chunk['end_line']}")
        print("-" * 60)
        print(result["snippet"])
        print("=" * 60)
        print()

    report_path = save_report(query, results)
    print(f"Retrieval report saved to: {report_path}")


if __name__ == "__main__":
    main()