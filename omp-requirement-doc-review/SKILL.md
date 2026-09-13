---
name: "omp-requirement-doc-review"
description: "OMP-optimized requirement delivery review with batched inputs, background reviewer concurrency, smol patch fallback, and explicit review-plus-remediation stop conditions. Use in Oh My Pi when reviewing, auditing, verifying, accepting, 验收, 审查, 复核, or fixing findings for a tracked requirement. Do not use for creating the tracking document."
---

# OMP Requirement Doc Review

Audit a requirement after implementation, pause, handoff, or delivery preparation. Compare the Requirement Doc Tracking document with the real workspace code and produce a Chinese requirement delivery review report.

## Workflow

1. Locate the requirement tracking document.
   - Use the path provided by the user when available.
   - Otherwise search the target project's `docs/` and `docs/requirements/` directories for the most relevant recent tracking document.
   - If no tracking document can be identified, ask for the document path instead of guessing.
2. Read the tracking document first. Focus on original request, scope, out of scope, assumptions, acceptance criteria, affected systems, code change list, validation records, final alignment check, and review handoff.
3. Verify the declared review target before reviewing the implementation. Only after the exact Git snapshot is corrected and recorded in the tracking document may the review set `审查状态` to `审查中` and begin formal review.
   - Require one of: an exact commit SHA; a PR number or URL plus its head SHA; or `未提交工作区` plus the current HEAD SHA. `实现基线` is optional and is used only to delimit a required diff.
   - Run read-only `git rev-parse HEAD` and `git status` checks. For multi-repository requirements, verify each repository separately.
   - Do not silently review the current workspace when the target is missing or ambiguous, HEAD does not match, a declared clean commit has unrecorded changes, a declared dirty workspace lacks its base HEAD, or a PR lacks a verifiable head SHA. Return the document to `omp-requirement-doc-tracking` to record the exact commit SHA, PR head SHA, or dirty-worktree base HEAD; `omp-requirement-doc-review` must not edit the review target. A general verbal instruction such as “review the current workspace” is not a snapshot correction. If the tracking document remains unaligned and the user asks to finish, conclude `无法确认` without setting `审查状态：审查中`.
   - A formal review requires a Git snapshot. For a non-Git workspace without a user-provided immutable artifact identifier, conclude `无法确认`; do not invent a hashing scheme.
4. Inspect the current workspace implementation.
   - Check relevant diffs, changed files, tests, routes, configs, migrations, and modules named by the tracking document.
   - Treat the document as review input, not as proof. Verify claims against code wherever possible.
5. Compare implementation against the documented acceptance criteria.
   - Mark each criterion as `通过`, `不通过`, `部分通过`, or `无法确认`.
   - Cite concrete code, test, config, or document evidence for each conclusion.
6. Produce or update a requirement delivery review report using `references/需求达标审查报告模板.md`.
   - Default path: place it next to the tracking document as `<tracking-doc-name>-review.md`.
   - For a re-review after fixes, update the existing review report when that is clearer; otherwise create a numbered report such as `<tracking-doc-name>-review-2.md`.
7. After the review report is generated or refreshed, update the original requirement tracking document produced by `omp-requirement-doc-tracking`.
   - Set `审查状态：已审查`, set `最近审查结论` to exactly one Review Conclusion, fill `最近审查时间`, and refresh the review report path.
   - Fill or refresh the tracking document's review report path field when present, for example `- 需求达标审查报告：<review-report-path>` or `- 建议审查报告路径：<review-report-path>`.
   - Never modify `实施状态` based on the review conclusion.
   - Do not rewrite unrelated sections of the tracking document while making these status/path updates.
8. If findings require remediation, return them to the implementation workflow. During remediation, keep `审查状态：已审查` and preserve the previous `最近审查结论`. Only after remediation is complete may `omp-requirement-doc-tracking` align implementation facts and validation records and set `审查状态：待审查` for re-review.
9. In the final response, lead with the review conclusion, list blocking findings first, and include both the review report path and the updated tracking document path.

## OMP execution strategy

### Initial input batch

When the user provides the tracking document path and the repository is known, the first tool wave MUST read or run these inputs in parallel:

- The requirement tracking document.
- `references/需求达标审查报告模板.md`.
- `references/审查清单.md`.
- The existing review report, when present.
- `git rev-parse HEAD`.
- `git status --short --branch`.

Do not read the same input again unless it changed or a narrower line range is required. If the tracking document reveals additional repositories, verify them in one supplemental parallel wave. If the tracking document path is unknown, locate it first, then run this batch.

### Background reviewer

After the review snapshot is aligned:

1. Set `审查状态：审查中`.
2. Start exactly one background `reviewer`.
3. Immediately continue the main agent's code, diff, call-site, test, and acceptance-criteria inspection.
4. NEVER call `AgentHandle.wait()`, `hub wait`, `hub jobs`, or send progress queries for the reviewer.
5. Consume the automatically delivered reviewer result.
6. Combine it with the main agent's evidence and immediately produce the review report. Do not start another general review before writing the report.

Do not run tests before the initial review merely to reconfirm validation claims from the tracking document. Run a reproduction or focused command only when needed to establish a finding.

### OMP agent and model roles

- `smol`, `default`, and `slow` are completion model selectors, not assumed Agent roles.
- Use only Agent names explicitly available in the current OMP runtime.
- When the user requests smol remediation and no `smol` Agent exists, call `completion(model: "smol")` once with the accepted findings and exact affected code context. Smol proposes a patch but does not edit the workspace.
- The main agent MUST review and correct the proposal, inspect affected call sites, apply the complete patch in one edit wave, and own validation.

### Combined review and remediation request

When the user requests review and remediation in the same request:

1. Perform one formal review and write the initial report.
2. Preserve that review conclusion while remediating findings.
3. Collect all accepted findings before requesting or applying a patch.
4. Apply all accepted fixes before validation.
5. Run one focused regression command covering the findings. If it fails, fix the failure and rerun only that command.
6. Run the full suite once only when required by the acceptance criteria.
7. Return to `omp-requirement-doc-tracking` to align implementation facts and set `审查状态：待审查`, preserving the previous review conclusion.
8. Stop after remediation delivery. Do not automatically start a second `reviewer`.

A second formal review is allowed only when the user explicitly asks for `复审`, `重新验收`, `确认修复后通过`, or an equivalent final review.

Without that explicit re-review, the final response MUST distinguish the previous formal review conclusion, the findings fixed and validated, and the requirement's current `待审查` state. It MUST NOT claim that the requirement passed review.

## Required behaviors

- Review only after a requirement has implementation, is paused for handoff, is ready to deliver, or the user explicitly asks for a stage review.
- Do not create the requirement tracking document; that belongs to `omp-requirement-doc-tracking`.
- Do not edit implementation code unless the user explicitly asks to fix review findings.
- Do update only the tracking document's review status, latest review conclusion, review time, and review report path after producing or refreshing the review report. If other content is inaccurate, record the mismatch in the report and return it to `omp-requirement-doc-tracking`.
- If the tracking document uses a recognized legacy `状态` field, migrate only that field and missing review handoff fields using the rules below. If it has no recognizable status structure, record that the update could not be applied in the report and final response.
- Distinguish requirement gaps, document-code mismatches, test gaps, and unconfirmable items.
- Prefer tight file and line references for findings when possible.
- Keep the review report in Chinese.

## Legacy status compatibility

Migrate a legacy tracking document only as part of the requested review:

- Rename `状态：已计划 | 进行中 | 已阻塞 | 已完成` to `实施状态` and preserve the value.
- For `状态：待审查`, set `实施状态：TBD`, set a missing review status to `待审查`, and set a missing latest conclusion to `TBD`.
- For `状态：已审查`, set `实施状态：TBD`, set a missing review status to `已审查`, and set a missing latest conclusion to `TBD`.
- For `状态：通过 | 有条件通过 | 不通过 | 无法确认 | 阶段性审查`, set `实施状态：TBD`, move the old value to `最近审查结论`, and set a missing review status to `已审查`.
- Existing explicit review status wins. Preserve existing report paths, review focus, and known issues. Do not rewrite other sections. If the old status is unrecognized, do not modify it; stop and ask the user what it means.

## Review Conclusions

Use one of these conclusions:

- `通过`：验收标准有足够代码和验证证据支撑，未发现阻塞问题。
- `有条件通过`：核心目标达成，但存在非阻塞文档偏差、测试缺口或低风险后续项。
- `不通过`：存在未实现、实现错误、范围偏差、关键验证缺失或交付风险。
- `无法确认`：缺少追踪文档、代码上下文、测试证据或必要环境，无法可靠判断。
- `阶段性审查`：需求尚未完成，报告当前完成度、缺口和交接风险。

## Reference map

- Read `references/需求达标审查报告模板.md` when creating or refreshing the review report.
- Read `references/审查清单.md` while comparing the tracking document with workspace code.
