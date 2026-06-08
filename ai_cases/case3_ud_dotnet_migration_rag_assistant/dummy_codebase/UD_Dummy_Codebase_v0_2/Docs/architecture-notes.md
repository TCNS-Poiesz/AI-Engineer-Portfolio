# UD Dummy Codebase v0.2 - Architecture Notes

The dummy codebase is intentionally small and educational.

## Layers

- Domain: business objects and enums.
- Services: workflow logic and coordination between domain objects.
- Infrastructure: repository and gateway interfaces.
- Docs: business process notes and RAG test questions.

## RAG design intention

The project is designed to support code-aware RAG experiments later.

Useful metadata for indexing:

- file_path
- file_name
- layer
- domain_area
- business_process
- user_role
- language
- extension
