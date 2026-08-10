---
name: "requirement-doc-tracking"
description: "Create and maintain a Chinese requirement implementation tracking document for feature requirements only, then final-align it for later Requirement Doc Review. Use only when starting or continuing a user-facing feature requirement, product capability, business workflow, or explicitly requested requirement-tracking/docs-trail work. Do not auto-trigger for bugs, fixes, configuration changes, operational changes, investigation/analysis, code review, refactoring, dependency updates, environment setup, or simple code edits unless the user explicitly asks to create or maintain a requirement document."
---

# Requirement Doc Tracking

Keep one requirement implementation tracking document aligned with feature requirement work from kickoff to delivery. Create the project doc before substantive feature implementation, update it as scope or decisions change, and finish by making it ready for an independent Requirement Doc Review.

## Trigger Boundary

Use this skill only for feature requirements:

- New user-facing features or product capabilities.
- Business workflow changes that need acceptance criteria.
- Cross-service feature work where the feature contract should be documented.
- Cases where the user explicitly asks for requirement tracking, a requirement document, a docs trail, or later requirement review.

Do not auto-trigger this skill for:

- Bug reports, bug fixes, regressions, or production incidents.
- Configuration, `.env`, port, address, credentials, deployment, or operational changes.
- Investigation, analysis, troubleshooting, exploration, or "find why" tasks.
- Code review, audit, verification, or acceptance review; use `requirement-doc-review` only when applicable.
- Refactoring, cleanup, formatting, comments, dependency updates, tests-only changes, or simple code edits.

If a task is ambiguous, default to not using this skill and proceed with the normal coding workflow unless the user explicitly asks for requirement tracking.

## Workflow

1. Identify the target project and its documentation location.
2. Before making substantive code changes for a new feature requirement, create or update a tracking document in that project's `docs/` or `docs/requirements/` directory.
3. Use `references/需求文档模版.md` as the starting structure. Fill unknown details with `TBD` instead of inventing answers.
4. Preserve the user's original request separately from later conclusions, final delivery notes, and implementation decisions.
5. Define explicit acceptance criteria before or early in implementation. If the user has not provided them, derive the smallest verifiable criteria from the request and mark assumptions clearly.
6. Update the document whenever the plan, scope, interfaces, database changes, risks, progress, validation status, or rollout assumptions change.
7. Before closing the task, compare the final code and behavior with the document. Remove stale plans, capture deviations, and make the document describe what actually shipped.
8. When the requirement is complete, paused for handoff, or ready for independent audit, keep the implementation status truthful and set only the review status to `待审查`. Fill the required review target using the Git snapshot rules below.
9. In the final response, include the document path and confirm whether the document now matches the delivered business and technical state.

## Required behaviors

- Create the requirement document before the first substantive implementation edit for a new feature requirement.
- Prefer one document per user-visible requirement or tightly related change set.
- Record both business intent and technical design; do not leave the document as code notes only.
- Keep the original request, assumptions, acceptance criteria, and final delivery facts distinguishable.
- Keep the document updated during execution, not only at the end.
- If the work spans multiple repos or services, capture the dependency chain and note which side changed.
- If the task is blocked or paused, leave the document in a state that lets the next engineer resume quickly.
- Replace outdated statements instead of appending contradictory notes.
- Map changed code, APIs, configs, tables, jobs, or routes back to the acceptance criteria whenever possible.
- Record what was not verified and why; do not imply validation that did not happen.
- Keep implementation status, review status, and the latest review conclusion separate. Do not write a formal review conclusion; that belongs to `requirement-doc-review`.
- Document name and content should be in Chinese.

## Review handoff and re-review

- Set new documents to `实施状态：已计划`, `审查状态：不需要`, and `最近审查结论：未审查`.
- For review handoff, set `审查状态：待审查` without changing `实施状态` from its truthful value (`进行中`, `已阻塞`, or `已完成`).
- Fill `审查目标` with one of: an exact commit SHA; a PR number or URL plus its head SHA; or `未提交工作区` plus the current HEAD SHA. Fill `实现基线` only when the review must be limited to a specific diff. For multi-repository work, record these values for every repository.
- After a review finding requires remediation, restore `实施状态：进行中` while keeping `审查状态：已审查` and the previous `最近审查结论`. Update the actual changes, validation results, risks, and deviations. Only when remediation is complete, set the truthful implementation status, record the new exact review target, and set `审查状态：待审查`; preserve the previous conclusion until the new review finishes.
- Do not silently weaken the requirement or acceptance criteria to satisfy review findings.

## Legacy status compatibility

Migrate legacy documents only when they are being updated; do not scan or batch-migrate documents:

- Rename `状态：已计划 | 进行中 | 已阻塞 | 已完成` to `实施状态` and preserve the value.
- For `状态：待审查`, set `实施状态：TBD`, set a missing review status to `待审查`, and set a missing latest conclusion to `TBD`.
- For `状态：已审查`, set `实施状态：TBD`, set a missing review status to `已审查`, and set a missing latest conclusion to `TBD`.
- For `状态：通过 | 有条件通过 | 不通过 | 无法确认 | 阶段性审查`, set `实施状态：TBD`, move the old value to `最近审查结论`, and set a missing review status to `已审查`.
- Preserve existing explicit review status, report path, review focus, and known issues. If the old status is unrecognized, do not modify it; stop and ask the user what it means.

## Minimum content

Every requirement document should cover:

- Metadata, implementation status, review status, and latest review conclusion
- Original request
- Summary, background, and goal
- Scope, out of scope, assumptions, and open questions
- Acceptance criteria
- Affected systems, files, routes, APIs, tables, configs, jobs, or external dependencies
- Implementation plan and key decisions
- Progress log
- Code change list mapped to acceptance criteria
- Validation and testing, including unverified items
- Risks and follow-up work
- Final alignment check
- Requirement Doc Review handoff entry

## Final audit checklist

Before declaring the task complete, verify that:

- The implemented behavior matches the documented business goal.
- The document names the actual files, modules, routes, tables, configs, or jobs that changed.
- Cross-project dependencies and contracts are described correctly.
- Deviations from the original plan are captured.
- Validation status reflects what was actually run and what was not verified.
- Remaining risks and follow-up work are explicit.
- The document does not describe code or behavior that was never shipped.
- The review entry identifies whether an independent `requirement-doc-review` pass is recommended and where its report should go.
- The review target identifies the exact Git snapshot; the optional implementation baseline is present only when needed to delimit the diff.

## Trigger examples

Use this skill for requests like:

- "Implement this new feature requirement in this project."
- "Add this feature and keep a docs trail."
- "Before coding, create a docs file to track the demand."
- "This feature spans two services; document the dependency and update it until done."

Do not use this skill for requests like:

- "Fix this bug."
- "Change the service address/port/config."
- "Investigate why this endpoint fails."
- "Review whether this implementation is correct."
- "Refactor or simplify this code."

## Relationship to Requirement Doc Review

Use this skill while the requirement is being discussed, implemented, paused, or finalized. It creates the source-of-truth tracking document.

Do not perform the independent delivery review here. When the user asks to review, audit, verify, accept,复核,验收, or check whether an implemented requirement meets its tracking document, use `requirement-doc-review` instead.

## Reference map

- Read `references/需求文档模版.md` when creating or refreshing the project tracking document.
- Read `references/可选章节清单.md` only when the requirement involves interfaces, database changes, rollout, rollback, or other complex delivery concerns.
