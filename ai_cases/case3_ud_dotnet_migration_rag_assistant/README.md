# Case 3 - UD .NET Migration RAG Assistant

**Project status:** v0.5 - Local RAG Skeleton Complete  
**Project type:** Portfolio prototype / educational RAG case  
**Domain:** Unattended Delivery, C#/.NET codebase understanding, migration support, AI-assisted retrieval

## 1. Project purpose
This project is a safe, educational, portfolio-quality prototype of a Retrieval-Augmented Generation (RAG) assistant for understanding a UD-like C#/.NET codebase and exploring how RAG can support future migration to the latest .NET version.

The purpose is to explore how AI can help a product owner, business architect, or developer understand software structure, locate relevant code, and prepare migration-oriented questions by connecting:

- business and logistics concepts
- domain models
- service-layer logic
- source-code files
- retrieval methods
- grounded explanation

The project bridges business knowledge and technical code navigation. Longer term, the same pattern can support onboarding, architecture understanding, bug investigation, migration planning, and product-owner/developer collaboration.

## 2. Why this project uses a dummy codebase

This project deliberately uses a dummy C#/.NET-style codebase instead of real UD production source code.

This keeps the project safe for:

- learning and experimentation
- public portfolio use
- Git/GitHub preparation
- AI retrieval prototyping
- future demonstration to partners, developers, or clients

The dummy codebase is designed to resemble important UD concepts without exposing production code, credentials, customer data, lock provider details, or private operational information.

## 3. Project folder structure

Current local project folder:

```text
C:\Users\annet\Documents\tcns-portfolio\ai_cases\case3_ud_dotnet_migration_rag_assistant
```

Main structure:

```text
case3_ud_dotnet_migration_rag_assistant/
  dummy_codebase/
  outputs/
  rag_prototype/
  releases/
```

Current active dummy codebase:

```text
dummy_codebase/
  UD_Dummy_Codebase_v0_2/
```

Frozen release package:

```text
releases/
  UD_Dummy_Codebase_v0_2.zip
```

## 4. Dummy UD codebase overview

The dummy codebase models a simplified Unattended Delivery system.

Important business concepts included:

- Organisation
- User
- Delivery
- DeliveryStatus
- DeliveryAssignment
- DeliverySpace
- SmartBox
- SmartLock
- AccessRight
- Alert

Important UD-specific status logic:

- `Delivered` means the deliverer has placed the delivery in the authorized box or space.
- `Received` means the receiver has retrieved the delivery from the box or space.
- `Received` is the final successful state.

Access-right logic:

- The receiver or owner of the delivery box or delivery space has permanent access.
- The deliverer receives temporary access for one delivery and one time window.

Cancellation and failure are modeled separately:

- `DeliveryCancelled` is a status.
- `CancellationReason` explains why the delivery was cancelled.
- `DeliveryFailed` is a status.
- `FailureReason` explains why the delivery failed.

## 5. Dummy codebase folders

```text
Domain/
  AccessRight.cs
  AccessRightStatus.cs
  AccessRightType.cs
  Alert.cs
  AlertType.cs
  AssignmentStatus.cs
  CancellationReason.cs
  Delivery.cs
  DeliveryAssignment.cs
  DeliverySpace.cs
  DeliveryStatus.cs
  FailureReason.cs
  Organisation.cs
  OrganisationType.cs
  SmartBox.cs
  SmartBoxStatus.cs
  SmartLock.cs
  SmartLockStatus.cs
  SpaceType.cs
  User.cs
  UserRole.cs

Services/
  AccessControlService.cs
  AlertService.cs
  DeliveryAssignmentService.cs
  DeliveryStatusService.cs
  SpaceMatchingService.cs

Infrastructure/
  LockProviderGateway.cs
  NotificationGateway.cs
  RepositoryInterfaces.cs

Docs/
  architecture-notes.md
  business-process.md
  rag-questions.md
```

## 6. RAG prototype scripts

All RAG prototype scripts are stored in:

```text
rag_prototype/
```

Scripts created so far:

```text
load_codebase.py
split_code_files.py
query_chunks.py
query_chunks_vector.py
answer_from_chunks.py
compare_retrieval_methods.py
```

## 7. Completed RAG pipeline phases

### Phase 1 - Codebase inventory

Script:

```text
load_codebase.py
```

Purpose:

- finds all `.cs` files
- detects architectural layer: Domain, Services, Infrastructure, Docs
- counts lines and characters
- saves codebase metadata

Output:

```text
outputs/codebase_inventory.json
```

### Phase 2 - Code chunking

Script:

```text
split_code_files.py
```

Purpose:

- splits C# files into RAG-ready chunks
- adds metadata such as file name, path, layer, domain area, and line range
- creates a markdown chunk report

Outputs:

```text
outputs/code_chunks.json
outputs/chunk_report.md
```

### Phase 3 - Keyword / rule-based retrieval

Script:

```text
query_chunks.py
```

Purpose:

- searches code chunks using keyword and rule-based matching
- uses simple business-to-code synonym expansion
- returns relevant files, line ranges, and snippets

Output:

```text
outputs/retrieval_results.md
```

### Phase 4 - Vector-style retrieval

Script:

```text
query_chunks_vector.py
```

Purpose:

- implements local TF-IDF-style vector retrieval
- converts chunks and questions into simple numeric vectors
- computes cosine similarity
- returns ranked relevant chunks

This is not yet full LangChain/OpenAI embeddings. It is a local learning bridge toward real RAG.

Output:

```text
outputs/retrieval_vector_results.md
```

### Phase 5 - RAG-style answer generation

Script:

```text
answer_from_chunks.py
```

Purpose:

- uses vector retrieval results
- produces a simple grounded answer report
- cites retrieved source file, layer, domain area, and line range
- creates a human-readable RAG-style output

Output:

```text
outputs/rag_answer.md
```

### Phase 5b - Retrieval comparison report

Script:

```text
compare_retrieval_methods.py
```

Purpose:

- compares keyword/rule-based retrieval with vector-style TF-IDF retrieval
- runs a fixed set of test questions through both methods
- produces a markdown comparison report

Output:

```text
outputs/retrieval_comparison_report.md
```

## 8. Example questions

The prototype has been tested with questions such as:

```text
Where is delivery assignment handled?
Where is temporary deliverer access granted?
Where does a delivery become Received?
Where is the LSP alert triggered?
```

Example successful mappings:

- Delivery assignment questions point to `Services\DeliveryAssignmentService.cs`.
- Received status questions point to `Services\DeliveryStatusService.cs` and/or `Domain\Delivery.cs`.
- Temporary deliverer access questions point to `Services\AccessControlService.cs` and `Domain\AccessRight.cs`.

## 9. Current output files

The current `outputs/` folder contains:

```text
chunk_report.md
code_chunks.json
codebase_inventory.json
rag_answer.md
retrieval_results.md
retrieval_vector_results.md
retrieval_comparison_report.md
```

## 10. How to run the prototype

When the terminal is inside:

```text
C:\Users\annet\Documents\tcns-portfolio\ai_cases\case3_ud_dotnet_migration_rag_assistant\rag_prototype
```

run scripts like this:

```powershell
python .\load_codebase.py
python .\split_code_files.py
python .\query_chunks.py "Where is delivery assignment handled?"
python .\query_chunks_vector.py "Where is delivery assignment handled?"
python .\answer_from_chunks.py "Where is delivery assignment handled?"
python .\compare_retrieval_methods.py
```

When the terminal is one level higher, inside:

```text
C:\Users\annet\Documents\tcns-portfolio\ai_cases\case3_ud_dotnet_migration_rag_assistant
```

run scripts like this:

```powershell
python .\rag_prototype\load_codebase.py
python .\rag_prototype\split_code_files.py
python .\rag_prototype\query_chunks.py "Where is delivery assignment handled?"
python .\rag_prototype\query_chunks_vector.py "Where is delivery assignment handled?"
python .\rag_prototype\answer_from_chunks.py "Where is delivery assignment handled?"
python .\rag_prototype\compare_retrieval_methods.py
```

Important note:

The command depends on the current PowerShell folder. If the prompt already ends in `rag_prototype>`, do not add another `rag_prototype` in the path.

## 11. Current milestone

Current milestone:

```text
UD Codebase RAG Assistant v0.5
```

Status:

```text
Local RAG skeleton complete.
Keyword retrieval works.
Vector-style retrieval works.
RAG-style answer generation works.
Retrieval comparison report generated successfully.
```

## 12. Future direction: .NET migration-support questions

A next logical phase is to add a migration-oriented question set. This would help explore how a RAG assistant could support developers during a future .NET migration.

Example migration questions:

```text
Which files would be relevant for a .NET version migration?
Where are infrastructure dependencies defined?
Which services coordinate business workflow?
Which files are most important for access-control logic?
Which files should a developer inspect first before upgrading dependencies?
```

This phase would connect code retrieval to practical software maintenance and modernization work.

## 13. Future direction: real embeddings and LangChain

The current vector-style retrieval uses a local TF-IDF-style approach. A future version can move toward full RAG with real embeddings and a vector store.

Possible future additions:

- LangChain text splitters
- C# language-aware splitting where possible
- OpenAI embeddings or local embeddings
- local vector store
- LLM-based answer generation
- improved source citations
- comparison between keyword, TF-IDF, and embedding-based retrieval

## 14. Git and GitHub preparation notes

Suggested future repository name:

```text
ud-codebase-rag-assistant
```

Before publishing or sharing, do not include:

- real UD production source code
- credentials
- API keys
- customer data
- real lock provider credentials
- private operational data

Recommended GitHub preparation steps:

- keep the dummy codebase clearly labeled as dummy/demo code
- include this README at the project root
- add a `.gitignore` for Python cache files, virtual environments, and temporary outputs if needed
- review all output files before publishing
- avoid committing secrets or private operational information
- consider adding a short portfolio case-study summary later

## 15. Why this project matters

This is not just a RAG exercise.

It demonstrates how AI can help a product owner or business architect understand and navigate a software system by connecting business process, domain model, service logic, source-code chunks, retrieval, and grounded explanation.

Longer term, this pattern can support:

- onboarding
- architecture understanding
- codebase navigation
- bug investigation
- migration from .NET 6 to a later .NET version
- product-owner/developer collaboration
- portfolio demonstration of applied AI in logistics

## 16. Portfolio positioning

This project can be positioned as an applied AI case study at the intersection of logistics, software architecture, and source-code RAG.

It shows the ability to:

- translate domain knowledge into a safe demo codebase
- process source files into searchable chunks
- compare retrieval methods
- generate grounded answers from retrieved code context
- prepare a future path toward production-grade RAG tooling

The current version is intentionally local, transparent, and educational. That makes it suitable for learning, iteration, and portfolio storytelling before moving to more advanced embedding-based RAG.

