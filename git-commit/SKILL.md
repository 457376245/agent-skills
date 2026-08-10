---
name: git-commit
description: Generate and execute concise, single-line Conventional Commit messages in Chinese for Java projects, then push the commit to the remote repository. Use when the user runs /git-commit, says "commit", "create commit", "commit changes", "commit and push", "提交", or "提交并推送", or asks to commit completed code changes.
---

# Git Commit and Push

Generate a short Chinese Conventional Commit message, execute the commit, and push it to the remote repository.

## Message Format

Use exactly one physical line:

```text
<type>(<scope>): <subject>
```

Apply these constraints:

- Output only the message as plain text, without a Markdown code fence.
- Never add a body, footer, bullet list, explanation, issue reference, `BREAKING CHANGE`, or line break.
- Keep `type` and `scope` lowercase.
- Write `subject` in concise Chinese, preferably within 50 characters.
- Do not end the subject with punctuation.
- Summarize the primary logical change instead of listing implementation details.
- For a breaking change, use `!` before the colon only when it adds necessary information; still keep the message to one line.

## Types

- `feat`: 新功能或新 API
- `fix`: 缺陷修复
- `refactor`: 不改变功能的重构
- `test`: 新增或更新测试
- `docs`: 仅文档变更
- `perf`: 性能优化
- `build`: Maven、Gradle 或构建依赖变更
- `chore`: 维护性变更

Choose the scope from the affected module, component, or business area, such as `core`, `api`, `issuer`, or `plugin-loader`.

## Workflow

1. Read staged changes once with `git diff --staged --stat` and targeted staged diffs.
2. Identify the primary logical change, type, and scope.
3. Generate one single-line Chinese message following all format constraints.
4. Execute `git commit -m "<message>"`.
5. Execute `git push` immediately after the commit succeeds.
6. Return only that same single-line message after both commands succeed. If the push fails, report the push error and state that the commit exists locally.

## Examples

Correct:

```text
refactor(issuer): 存量债评级字段改为英文名
```

```text
fix(plugin-loader): 修复插件目录缺失时的空指针
```

```text
build(deps): 升级 Spring Boot 到 3.2.1
```

Incorrect:

```text
refactor(issuer): 存量债评级字段改为英文名

将「存量债市场隐含评级」「存量综合MIRS」调整为英文键名，
并同步更新字段说明与测试。

BREAKING CHANGE: 中文响应字段名已替换为英文键名。
```

The incorrect example contains detail and line breaks that must be omitted.
