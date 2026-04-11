# Global Architecture Template

Use this template for system-level design generated from a PRD.

## 1. Design Scope

- State what product or system is being designed.
- State whether this is an MVP architecture, standard production architecture, or a higher-scale target.

## 2. Goals and Constraints

- Summarize the product goal.
- List important functional boundaries.
- List non-functional constraints such as latency, scale, compliance, security, audit, or cost.
- List explicit tech stack constraints from the user or team.

## 3. Recommended Stack and Rationale

- Suggest language, framework, storage, queue, vector store, OCR, and document processing choices only when relevant.
- Explain why the choices fit the system.
- Mark optional alternatives separately from the recommended baseline.

## 4. System Architecture

- Describe the overall architecture in prose.
- Add a `mermaid flowchart` when there are several components or processing stages.

Cover these areas when relevant:

- client or admin surfaces
- business backend
- AI orchestration service
- file storage
- relational storage
- vector retrieval
- async jobs and workers
- export service
- external model or OCR providers

## 5. Module or Service Boundaries

- List each module or service.
- State its responsibility.
- State what it owns.
- State what it depends on.

## 6. Core Data and Storage Design

- Identify primary entities.
- Identify storage responsibilities by datastore.
- Explain which data belongs in relational storage, object storage, cache, or vector storage.

## 7. Processing Pipelines

Describe the key end-to-end technical flows.

Typical examples:

- document upload and parsing
- knowledge base ingestion and indexing
- image ingestion and recognition
- generation request and async job execution
- export generation

## 8. Security, Auth, and Audit

- Describe access model, role model, and isolation model.
- Describe where audit logs should exist.
- Mention data protection requirements if relevant.

## 9. Observability and Operations

- Logging
- metrics
- tracing
- failure alerts
- retry strategy

## 10. Risks and Tradeoffs

- List the key architecture risks.
- Explain important tradeoffs rather than pretending there is one perfect answer.

## 11. Assumptions

- List assumptions made due to missing input.

## 12. Open Questions

- List the decisions that still need confirmation before implementation.

