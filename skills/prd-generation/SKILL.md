---
name: prd-generation
description: Draft structured PRDs from raw feature ideas, business requirements, or project briefs. Use when Codex needs to turn an incomplete product request into a PRD by clarifying missing context, defining scope, writing user stories, listing acceptance criteria, and surfacing assumptions, risks, dependencies, or open questions.
---

# PRD Generation

## Overview

Turn vague or partial product requests into a usable PRD. Clarify first, then draft a document with explicit assumptions, clear scope boundaries, and testable acceptance criteria.

Preserve the user's working language unless asked to translate. Prefer concise, decision-ready output over long narrative writing.

## Workflow

### 1. Build context from the request

Extract whatever is already present:

- problem statement
- target user or customer
- business goal or metric
- requested capability
- constraints such as timeline, platform, compliance, or integrations

If the request already contains enough detail for a credible draft, proceed. If not, ask a short set of focused clarification questions before writing the PRD.

### 2. Clarify only what matters

Use [references/clarification-checklist.md](references/clarification-checklist.md) to decide what is missing.

Ask only the questions that materially affect scope, implementation direction, or acceptance criteria. Keep the list short and grouped. Do not ask obvious questions just to fill a template.

If the user does not answer every question, continue with a draft that:

- states assumptions explicitly
- marks unresolved decisions as open questions
- avoids fabricating precise metrics, dates, or technical commitments

### 3. Choose the output depth

Match the document depth to the request:

- short request or early discovery: produce a lean PRD
- normal feature work: produce a standard PRD
- cross-team or high-risk work: include risks, dependencies, rollout notes, and non-functional requirements

Do not expand every section mechanically. Omit sections that would be empty or meaningless.

### 4. Draft the PRD

Use [references/prd-template.md](references/prd-template.md) as the default structure.

Adapt section titles when the user's organization already follows another PRD style, but keep these concepts whenever relevant:

- context and problem
- goals and non-goals
- users and scenarios
- scope
- requirements
- acceptance criteria
- dependencies and risks
- open questions

### 5. Enforce quality bars

Before finalizing, verify that the draft:

- distinguishes goals from solution details
- separates in-scope items from out-of-scope items
- turns vague requests into observable requirements
- includes acceptance criteria that can be checked
- records assumptions instead of hiding them
- highlights missing information that still blocks execution

## Drafting Rules

- Do not invent research, stakeholder approval, analytics baselines, or delivery dates.
- Prefer concrete statements such as "Users can export CSV from the order list" over abstract statements such as "Improve reporting flexibility."
- Write requirements in a way that engineering, design, QA, and product can all act on.
- When technical design is unknown, describe required behavior and constraints instead of prescribing architecture.
- When the user asks for a very rough PRD, allow placeholders and clearly tag them as assumptions or open questions.
- When the user asks for a final PRD, tighten wording and reduce brainstorming language.

## Output Guidance

Use clean markdown with short sections and flat bullets where useful.

If information is missing, structure the response in this order:

1. Clarifying questions
2. Draft PRD
3. Assumptions and open questions

If enough information is already available, go straight to the PRD and include a brief assumptions section only when needed.

## Example Triggers

Requests that should trigger this skill include:

- "Write a PRD for adding supplier chat to the tender workflow."
- "Turn this rough feature brief into a proper product requirements doc."
- "I have a requirement idea. Help me clarify it and produce a PRD."
- "Generate a Chinese PRD from these notes."

