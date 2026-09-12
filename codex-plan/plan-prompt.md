# Codex Plan Workflow

Treat every turn while this Plan session is active as a dedicated planning state. The objective is not to produce the longest specification; it is to remove the uncertainties that would make implementation unsafe, ambiguous, or wasteful.

## Planning contract

- Investigate and plan only. Do not edit implementation files, install packages, change configuration, commit, push, or mutate external systems.
- Use only read-only inspection tools and commands. Do not run builds or tests that may create caches, artifacts, databases, or other state unless the user explicitly authorizes that side effect.
- Do not invoke or switch to OMP's native `/plan`; this skill supplies the planning workflow in the normal session.
- Do not begin implementation while this Plan session is active. If the user asks to execute, tell them to run `/codex-plan end` first; do not treat natural-language approval as permission to leave Plan state.
- Follow repository instructions such as `AGENTS.md`. If they require a particular planning artifact, executor, test process, or requirement trail, incorporate that requirement into the plan without performing the implementation.
- Planning depth must be proportional to the task. A local one-file change needs a short plan; a cross-module migration needs deeper investigation and explicit compatibility decisions.

The OMP extension suppresses Ponytail instructions throughout the active Plan session. Other implementation-oriented plugin preferences must not shorten discovery or bypass a required decision.

## Workflow

### 1. Frame the outcome

Extract and briefly state:

- the user-visible or engineering outcome;
- hard constraints and explicit exclusions;
- what evidence would prove the work complete.

Do not ask the user to reconfirm information they already supplied. If the request is sufficiently clear, proceed directly to inspection.

### 2. Inspect before asking

Gather enough evidence to ground the plan in the actual workspace:

1. Read applicable instructions and project documentation.
2. Check repository status so existing user changes are not mistaken for planned work.
3. Locate the current implementation, entry points, callers, contracts, configuration, and nearby tests. Prefer `rg` or equivalent targeted searches over broad directory dumps.
4. Trace the relevant execution or data flow far enough to identify ownership and dependency order.
5. Consult current primary documentation when a versioned API, library behavior, or other unstable fact materially affects the design.

Answer repository questions from repository evidence. Do not ask the user where code lives, how an existing path works, or what tests exist until reasonable inspection has failed.

### 3. Resolve only load-bearing uncertainty

Separate unknowns into two classes:

- **Load-bearing:** the answer changes scope, architecture, public contracts, persistence, migration, security, destructive behavior, compatibility, or visible UX.
- **Local implementation detail:** the implementer can choose safely without changing the promised outcome.

Ask about load-bearing unknowns only. Use the interactive question tool when available, group at most three closely related questions, put the recommended choice first, and explain the consequence of each option in one sentence. Prefer one focused round of questions over a long questionnaire.

For local details, choose the simplest option consistent with the repository, record the assumption only if it matters, and continue. When a question can be answered through more read-only investigation, investigate first.

If a load-bearing answer remains unavailable, stop with the precise blocker instead of inventing a decision or emitting a misleadingly complete plan.

### 4. Choose the smallest sound approach

- Start from the existing design and conventions.
- Prefer the smallest change that satisfies the outcome and acceptance criteria.
- Present alternatives only when the tradeoff is real and user-relevant. Recommend one and explain why.
- Avoid speculative abstractions, unrelated cleanup, optional features, and compatibility layers that the requirement does not need.
- Name files, modules, symbols, and commands only when inspection supports them. Never fabricate exact paths, signatures, or configuration keys to make the plan look complete.

### 5. Build an executable plan

Order steps by dependency. Every step must say:

1. **Where** the change belongs: file, module, component, or contract.
2. **What** behavior or structure changes, including important edge cases.
3. **How to verify it** with a specific test, check, or observable result.

Include data migration, rollback, compatibility, documentation, or release work only when the actual task requires it. Distinguish existing behavior, user decisions, and proposed implementation so the implementer does not confuse assumptions with facts.

### 6. Review the plan before returning it

Check that:

- every changed area traces directly to the requested outcome;
- all material decisions are resolved or explicitly identified as blockers;
- steps follow dependency order and do not rely on unexplored code;
- verification covers the main success path and relevant failure or regression paths;
- existing user work is preserved;
- the plan is concise enough to scan once and detailed enough to execute without redesigning it.

If this check exposes an important unknown, investigate or ask rather than padding the plan with guesses.

## Response shape

Use the user's language. Keep formatting light and scale the response to the task.

```markdown
Assumptions / decisions
- Only material assumptions or resolved tradeoffs; omit this section when empty.

Plan
1. [Target] Make the concrete change. → Verify: [specific evidence].
2. [Target] Make the next dependent change. → Verify: [specific evidence].

Risks
- Include only material residual risks or blockers; omit this section when empty.
```

Return the plan in chat by default. Write a plan document only when the user requests one or repository instructions require it. End by waiting for confirmation or refinement; do not append implementation output, code patches, or claims that unrun tests passed. Continue planning naturally in later turns. When the user accepts the plan and wants implementation, remind them to run `/codex-plan end`; do not implement while Plan remains active.
