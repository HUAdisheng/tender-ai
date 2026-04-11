---
name: prd-to-tech-design
description: Turn PRDs, product briefs, and follow-up constraints into technical design documents. Use when Codex needs to produce a global system architecture, recommend technical choices, design a specific feature in detail, analyze feature workflows, or revise an existing design based on new requirements while keeping alignment with the broader system.
---

# PRD To Tech Design

## Overview

Generate technical design in two layers: global architecture first, feature design second. Support incremental revision so later feature work stays consistent with the earlier system design.

Preserve the user's working language unless asked to translate. Prefer explicit design decisions, assumptions, tradeoffs, and open questions over vague architecture prose.

## Request Classification

Before writing, classify the request into one of three modes:

- `global-design`: create overall architecture and baseline technical choices from a PRD and user constraints
- `feature-design`: design one specific feature in detail using the PRD, user notes, and any existing global design
- `design-revision`: revise or extend an existing design after the user adds new constraints or corrections

If the request mixes multiple modes, split the response into phases instead of blending everything into one document.

## Core Workflow

### 1. Gather inputs

Collect the relevant artifacts:

- PRD or feature brief
- user follow-up notes
- tech stack constraints
- team constraints
- deployment, cost, compliance, latency, or timeline constraints
- existing global design document if present
- existing feature design document if present

If an existing design document is available, treat it as the current source of truth unless the user explicitly wants a redesign.

### 2. Extract design facts

Separate facts into these buckets:

- product goals
- functional scope
- non-functional constraints
- integration dependencies
- known stack constraints
- unresolved decisions

Do not silently infer hard constraints. Mark inferred items as assumptions.

### 3. Choose the output mode

Use these decision rules:

- if the user asks how the whole system should be built, use `global-design`
- if the user asks how one function should be implemented, use `feature-design`
- if the user asks to adjust a prior design because of new information, use `design-revision`

Use [references/decision-rules.md](references/decision-rules.md) when the boundary is unclear.

### 4. Design in the correct order

When doing `feature-design`, inherit these from the global design if available:

- system boundaries
- service boundaries
- storage choices
- async job model
- auth and audit model
- document and AI processing pipeline

Do not produce a feature design that contradicts the chosen global architecture without explicitly calling out the conflict.

### 5. Validate before finalizing

Verify that the output:

- distinguishes confirmed decisions from assumptions
- describes why the design fits the PRD
- keeps feature design aligned with global architecture
- includes flows, interfaces, and failure handling where relevant
- does not pretend unknown implementation details are settled

## Mode-Specific Instructions

### Global Design

Use [references/global-architecture-template.md](references/global-architecture-template.md).

Output the system-level design needed to answer:

- what services or modules exist
- why the chosen stack is appropriate
- how data, files, AI, and async tasks move through the system
- where major risks and boundaries are

Include architecture diagrams in `mermaid` when they add clarity.

Typical output should cover:

- system goals and constraints
- baseline stack choices
- overall architecture
- module or service decomposition
- storage and retrieval design
- AI and document processing pipeline
- async workflow and task orchestration
- security, audit, and operations considerations
- risks and open questions

### Feature Design

Use [references/feature-tech-design-template.md](references/feature-tech-design-template.md).

Start with feature analysis before technical design:

- define feature boundary
- identify actors and upstream/downstream dependencies
- describe main and exceptional flows
- identify what the feature owns versus what it delegates

Then design the implementation:

- module placement
- interfaces
- data structures
- state transitions
- async behavior
- failure handling
- observability
- test focus

If the feature depends on unresolved global design decisions, call that out early.

### Design Revision

Do not rewrite the whole design unless required. Instead:

- identify which decisions remain valid
- identify what new constraint changes
- update only affected sections
- explain downstream impacts on APIs, data, jobs, or diagrams

When a revision invalidates earlier choices, say so explicitly.

## Diagram Guidance

Use [references/diagram-guidelines.md](references/diagram-guidelines.md).

Prefer:

- `flowchart` for global architecture and business flow
- `sequenceDiagram` for component interaction
- `stateDiagram-v2` for status lifecycle

Do not add diagrams mechanically. Add them when they remove ambiguity.

## Missing Information Policy

Ask focused questions only when the missing information changes the design materially.

Good reasons to ask:

- storage choice depends on scale or query pattern
- sync versus async depends on latency expectation
- auth design depends on tenant or role model
- file processing design depends on size or format constraints

If the user does not answer, continue with explicit assumptions and limit the specificity of the design.

## Output Guidance

Use short sections and direct markdown. Default order:

1. Design scope or mode
2. Known constraints
3. Design output
4. Assumptions
5. Open questions

For feature work, prefer one feature per document or section. Avoid mixing multiple unrelated feature designs in the same block unless the user explicitly asks for a package design.

## Example Triggers

- "Based on this PRD, design the overall architecture and technical stack."
- "Use the existing global design and produce a detailed technical design for the knowledge base feature."
- "Revise the document generation design because the export flow must become asynchronous."
- "Analyze the workflow for tender parsing and output the technical design in Chinese."

