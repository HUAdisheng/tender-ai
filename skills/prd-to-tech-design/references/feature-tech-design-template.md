# Feature Technical Design Template

Use this template for one feature at a time.

## 1. Feature Scope

- Name the feature clearly.
- State whether this is a new feature, enhancement, or revision.
- State the design goal.

## 2. Relevant Context

- Reference the related PRD section.
- Reference the related global architecture if available.
- List feature-specific constraints and user clarifications.

## 3. Boundary Analysis

- What the feature owns
- What it depends on
- What is explicitly out of scope

## 4. Actors and Dependencies

- Primary actors or callers
- Upstream systems or modules
- Downstream systems or modules

## 5. Workflow Analysis

Describe:

- main flow
- alternative flow
- failure flow

Add diagrams when useful:

- `flowchart` for business or system flow
- `sequenceDiagram` for component interaction
- `stateDiagram-v2` for lifecycle

## 6. Technical Design

### Module Placement

- Where the feature lives in the system
- Which modules or services are involved

### Interfaces

- APIs
- internal service calls
- async events or jobs

### Data Design

- entities
- schemas or fields
- storage location

### State and Lifecycle

- statuses
- transitions
- retry behavior

### Failure Handling

- validation failures
- downstream failures
- timeout and retry strategy

## 7. Security and Permissions

- Required roles or access checks
- Audit requirements
- Data sensitivity considerations

## 8. Observability

- logs
- metrics
- traces
- key alerts

## 9. Test Focus

- unit test focus
- integration test focus
- end-to-end test focus

## 10. Risks and Tradeoffs

- feature-specific design risks
- known tradeoffs

## 11. Assumptions

- assumptions used to complete the design

## 12. Open Questions

- unresolved items that affect implementation

