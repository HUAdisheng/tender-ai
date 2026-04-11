# PRD Template

Use this as the default structure. Remove sections that do not add value, but keep the logic clear.

## Title

Use a direct feature or initiative name.

## 1. Background

- Describe the current context.
- Describe the problem or opportunity.
- State why this work matters now.

## 2. Goal

- State the primary business or user outcome.
- Add secondary goals only when they matter.

## 3. Non-Goals

- List what this work will not solve.
- Prevent scope creep by naming adjacent but excluded areas.

## 4. Target Users

- Identify primary users.
- Identify secondary users only if the feature materially affects them.

## 5. User Scenarios

- Describe the main user journey or jobs to be done.
- Prefer short scenario bullets or user stories.

Example:

- As a procurement manager, I want to compare supplier responses in one view so that I can make decisions faster.

## 6. Scope

### In Scope

- List the capabilities or changes that will be delivered.

### Out of Scope

- List excluded work that might otherwise be assumed.

## 7. Functional Requirements

- Write observable product behaviors.
- Separate independent requirements into distinct bullets.

Example:

- The system must allow users to filter tenders by status, owner, and submission deadline.
- The system must export the filtered result set to CSV.

## 8. Non-Functional Requirements

- Include only relevant quality constraints.
- Common dimensions: performance, security, auditability, availability, localization, accessibility.

## 9. Acceptance Criteria

- Write criteria that QA, product, and engineering can verify.
- Prefer "given/when/then" style when it improves clarity.

Example:

- Given a user has permission to manage tenders, when they open the tender list, then they can filter by status.
- Given a filtered list is displayed, when the user clicks export, then the CSV contains only filtered rows.

## 10. Dependencies and Risks

- List cross-team dependencies, external systems, or sequencing constraints.
- List key delivery or adoption risks.

## 11. Assumptions

- Record assumptions used to complete the draft.

## 12. Open Questions

- List unresolved questions that still need product, business, design, or engineering input.

