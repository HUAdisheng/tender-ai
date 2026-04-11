# Diagram Guidelines

Use diagrams to reduce ambiguity, not to decorate the document.

## Preferred diagram types

### `flowchart`

Use for:

- global architecture overview
- upload to processing to output flow
- feature-level business or system flow

### `sequenceDiagram`

Use for:

- service-to-service interactions
- request to async job handoff
- callback or polling flows

### `stateDiagram-v2`

Use for:

- task lifecycle
- document generation status transitions
- approval or processing states

## Diagram rules

- Keep node names short and concrete.
- Match names used in the text.
- Do not include every storage table or internal helper in the top-level diagram.
- Split large diagrams into multiple focused diagrams instead of one overloaded graph.
- If a diagram duplicates the text without adding clarity, omit it.

## Recommended usage by mode

- `global-design`: usually one architecture `flowchart`, optionally one processing `sequenceDiagram`
- `feature-design`: one flow diagram is often enough; add sequence or state only when needed
- `design-revision`: update only the diagram sections affected by the revision

