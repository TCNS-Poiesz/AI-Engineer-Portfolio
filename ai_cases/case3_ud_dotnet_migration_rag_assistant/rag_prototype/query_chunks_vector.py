from pathlib import Path
import json
import math
import re
import sys
from collections import Counter, defaultdict


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
CHUNKS_PATH = OUTPUTS_DIR / "code_chunks.json"


def tokenize(text):
    """
    Simple tokenizer for code and business-language questions.
    Keeps words, numbers, and underscores.
    """
    return re.findall(r"[a-zA-Z0-9_]+", text.lower())


def expand_query(query):
    """
    Small business-to-code vocabulary bridge.
    This helps words like 'received' find methods like MarkReceived().
    """
    synonym_map = {
        "assignment": ["assignment", "assign", "assigned", "lsp"],
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

    tokens = tokenize(query)
    expanded = []

    for token in tokens:
        expanded.append(token)
        if token in synonym_map:
            expanded.extend(synonym_map[token])

    return " ".join(expanded)


def load_chunks():
    if not CHUNKS_PATH.exists():
        raise FileNotFoundError(
            f"Could not find {CHUNKS_PATH}. Run split_code_files.py first."
        )

    with CHUNKS_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def chunk_text_for_vector(chunk):
    """
    Combine code content with metadata.
    Metadata is important because file names and layers carry meaning.
    """
    return " ".join(
        [
            chunk["file_name"],
            chunk["relative_path"],
            chunk["layer"],
            chunk["domain_area"],
            chunk["content"],
        ]
    )


def build_tfidf_vectors(chunks):
    documents = [chunk_text_for_vector(chunk) for chunk in chunks]
    tokenized_docs = [tokenize(doc) for doc in documents]

    document_frequency = defaultdict(int)

    for tokens in tokenized_docs:
        for token in set(tokens):
            document_frequency[token] += 1

    number_of_documents = len(tokenized_docs)
    vectors = []

    for tokens in tokenized_docs:
        term_counts = Counter(tokens)
        total_terms = len(tokens)
        vector = {}

        for token, count in term_counts.items():
            term_frequency = count / total_terms
            inverse_document_frequency = math.log(
                (number_of_documents + 1) / (document_frequency[token] + 1)
            ) + 1

            vector[token] = term_frequency * inverse_document_frequency

        vectors.append(vector)

    return vectors, document_frequency, number_of_documents


def build_query_vector(query, document_frequency, number_of_documents):
    expanded_query = expand_query(query)
    tokens = tokenize(expanded_query)
    term_counts = Counter(tokens)
    total_terms = len(tokens)
    vector = {}

    for token, count in term_counts.items():
        term_frequency = count / total_terms
        inverse_document_frequency = math.log(
            (number_of_documents + 1) / (document_frequency.get(token, 0) + 1)
        ) + 1

        vector[token] = term_frequency * inverse_document_frequency

    return vector


def cosine_similarity(vector_a, vector_b):
    common_tokens = set(vector_a.keys()) & set(vector_b.keys())

    numerator = sum(vector_a[token] * vector_b[token] for token in common_tokens)

    magnitude_a = math.sqrt(sum(value * value for value in vector_a.values()))
    magnitude_b = math.sqrt(sum(value * value for value in vector_b.values()))

    if magnitude_a == 0 or magnitude_b == 0:
        return 0

    return numerator / (magnitude_a * magnitude_b)


def make_snippet(content, query, max_chars=700):
    query_tokens = tokenize(expand_query(query))
    content_lower = content.lower()

    best_index = None

    for token in query_tokens:
        index = content_lower.find(token)
        if index != -1:
            if best_index is None or index < best_index:
                best_index = index

    if best_index is None:
        return content[:max_chars].strip()

    start = max(0, best_index - 180)
    end = min(len(content), start + max_chars)

    return content[start:end].strip()


def search(query, top_k=5):
    chunks = load_chunks()
    chunk_vectors, document_frequency, number_of_documents = build_tfidf_vectors(chunks)
    query_vector = build_query_vector(query, document_frequency, number_of_documents)

    results = []

    for chunk, chunk_vector in zip(chunks, chunk_vectors):
        similarity = cosine_similarity(query_vector, chunk_vector)

        if similarity > 0:
            results.append(
                {
                    "similarity": similarity,
                    "chunk": chunk,
                    "snippet": make_snippet(chunk["content"], query),
                }
            )

    results.sort(key=lambda item: item["similarity"], reverse=True)
    return results[:top_k]


def save_report(query, results):
    report_lines = []
    report_lines.append("# Vector Retrieval Results\n")
    report_lines.append(f"Query: {query}\n")

    for index, result in enumerate(results, start=1):
        chunk = result["chunk"]

        report_lines.append(f"## Result {index}")
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

    report_path = OUTPUTS_DIR / "retrieval_vector_results.md"
    report_path.write_text("\n".join(report_lines), encoding="utf-8")
    return report_path


def main():
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = input("Ask a question about the UD dummy codebase: ")

    print()
    print("UD Dummy Codebase - Vector Query")
    print("--------------------------------")
    print(f"Query: {query}")
    print()

    results = search(query)

    if not results:
        print("No matching chunks found.")
        return

    for index, result in enumerate(results, start=1):
        chunk = result["chunk"]

        print(f"Result {index}")
        print(f"Similarity: {result['similarity']:.4f}")
        print(f"File: {chunk['relative_path']}")
        print(f"Layer: {chunk['layer']}")
        print(f"Domain area: {chunk['domain_area']}")
        print(f"Lines: {chunk['start_line']}-{chunk['end_line']}")
        print("-" * 60)
        print(result["snippet"])
        print("=" * 60)
        print()

    report_path = save_report(query, results)
    print(f"Vector retrieval report saved to: {report_path}")


if __name__ == "__main__":
    main()