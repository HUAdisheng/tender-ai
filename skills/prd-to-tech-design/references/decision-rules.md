# Decision Rules

Use these rules to determine which mode to apply.

## Choose `global-design` when

- the user asks for architecture, stack selection, service decomposition, or deployment direction
- the request covers the whole system or several major modules
- there is no accepted system-level design yet

## Choose `feature-design` when

- the user names one feature or one bounded capability
- the user asks for detailed flow, API, data model, or implementation approach for a specific function
- the user wants technical design for one module under an existing architecture

## Choose `design-revision` when

- the user adds a new constraint that changes an existing design
- the user asks to revise only part of a design
- the user asks how an earlier decision changes because of scale, compliance, async processing, or stack changes

## Escalate uncertainty explicitly

If the request could fit more than one mode:

- state the mode you selected
- state why
- state what was intentionally deferred to a later phase

## Priority rule

If the system-level architecture is still unstable, avoid over-specifying feature internals. Establish the global design first or clearly tag the feature design as provisional.

