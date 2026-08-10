---
name: requirement-handoff
description: Plan-only handoff for coding requirements. Use when Codex must clarify and freeze a requirement, invoke requirement-doc-tracking to create or update the Chinese requirement document, and write a separate self-contained implementation handoff for a later model or tool that will know only those two documents. Stop after producing the documents; do not implement, review, remediate, or launch workers.
---

# Requirement Handoff

Convert a confirmed coding requirement into exactly two execution inputs:

1. A requirement tracking document.
2. A self-contained implementation handoff document.

Treat the later executor as having no conversation history. It knows only these two documents.

## Hard Boundaries

- Operate in plan-only mode.
- Invoke only `requirement-doc-tracking`; do not invoke other skills.
- Do not edit product source code, tests, migrations, configuration, UI assets, or business logic.
- Do not run mutating implementation commands.
- Do not launch subagents, workers, or external implementation tools.
- Do not implement, wait for results, review, accept, or write remediation instructions.
- Allow read-only repository inspection only when needed to make the two documents accurate.
- Finish immediately after returning the two document paths and a concise readiness statement.

## Workflow

1. Confirm the requirement.
   - State assumptions, goal, non-goals, scope, risks, acceptance criteria, and unresolved questions.
   - Resolve every question that could materially change implementation.
   - Do not write an executable handoff while a material decision remains `TBD`.
2. Inspect only the repository facts needed for an accurate plan.
   - Record exact project paths, relevant files, symbols, interfaces, existing patterns, and verification commands.
   - Distinguish verified facts from assumptions.
3. Invoke `requirement-doc-tracking`.
   - Create or update one Chinese requirement document under the target project's `docs/` or `docs/requirements/`.
   - Keep it as the durable source of truth for intent, scope, decisions, acceptance criteria, risks, and review preparation.
4. Write one separate implementation handoff document beside the requirement document.
   - Use a clearly related filename ending in `-handoff.md`.
   - Make it sufficient for execution without access to the conversation.
5. Cross-check both documents.
   - Ensure names, paths, scope, decisions, acceptance criteria, and commands agree.
   - Remove conversational shorthand such as “as discussed”, “use the approach above”, or references to unstated context.
   - If the documents conflict, correct them before handoff.
6. Return both paths and stop.

## Requirement Document Contract

Follow `requirement-doc-tracking`. In addition, ensure the document clearly records:

- The user's confirmed goal and observable success criteria.
- In-scope and out-of-scope behavior.
- Locked decisions and explicit assumptions.
- Verified repository facts and affected areas.
- Acceptance criteria that can be checked independently.
- Known risks and any genuinely non-blocking unknowns.

The requirement document is authoritative for requirement intent and acceptance scope.

## Handoff Document Contract

Keep the handoff concise, operational, and decision-complete. Include:

1. Goal.
2. Required reading, naming the requirement document by exact relative path.
3. Verified context and relevant repository facts.
4. Allowed changes, including exact files or bounded modules when known.
5. Forbidden changes and non-goals.
6. Locked implementation decisions and constraints.
7. Ordered implementation steps with expected outcomes.
8. Acceptance criteria mapped to implementation and verification steps.
9. Exact verification commands and expected pass conditions.
10. Stop conditions requiring escalation instead of guessing.
11. Required executor report format:
    - Changed files and symbols.
    - Concise diff summary.
    - Commands run and complete results.
    - Acceptance-criteria evidence.
    - Deviations, risks, blockers, and unresolved decisions.

Do not repeat background that does not affect implementation. Repeat critical constraints when omission could cause scope drift.

## Isolation Check

Before finishing, verify that an executor reading only the two documents can answer:

- What must be built?
- What must not change?
- Which repository areas may be edited?
- Which decisions are already fixed?
- What exact steps should be followed?
- How is each acceptance criterion verified?
- When must execution stop and ask for a decision?
- What evidence must be returned?

If any answer depends on conversation history, revise the documents before returning them.

## Completion

The skill is complete only when both documents exist and pass the isolation check. Report:

- Requirement document path.
- Handoff document path.
- Whether material open questions remain.

Then stop. Later implementation and `requirement-doc-review` usage are outside this skill.
