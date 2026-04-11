# Clarification Checklist

Use this checklist to decide whether to ask follow-up questions before drafting the PRD. Ask only the missing items that materially change the document.

## Core questions

- What problem is being solved?
- Who is the primary user or customer?
- What outcome matters to the business or team?
- What user action or capability is requested?

## Scope questions

- What is explicitly in scope?
- What is explicitly out of scope?
- Is this a net-new feature, a workflow change, or an optimization of an existing feature?
- Which platforms or surfaces are included: web, mobile, admin, API, internal tools?

## Constraint questions

- Are there deadlines, release windows, or compliance constraints?
- Are there integration dependencies on other systems or teams?
- Are there performance, security, audit, localization, or accessibility expectations?

## Success questions

- How will the team know the feature is successful?
- Are there target metrics, or should success remain qualitative for now?
- What must be true for QA or stakeholders to accept the feature?

## Safe fallback

If several answers are missing, continue only when a draft would still be useful. In that case:

- add an `Assumptions` section
- add an `Open Questions` section
- avoid false precision
- keep acceptance criteria behavioral and observable

