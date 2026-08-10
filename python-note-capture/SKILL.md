---
name: python-note-capture
description: >-
  Capture discussed Python code-learning points into the user's Obsidian Python vault. Use when the user asks to summarize one or more Python syntax, standard-library, typing, async, engineering, or Web-development knowledge points from code reading or prior discussion into Markdown notes (resolve vault: F: then E: per Vault root), following the user's directory rules: Chinese names first, key English terms preserved, Agent knowledge excluded except as code context.
---

# Python Note Capture

## Scope

Create or update Obsidian notes for Python knowledge learned during code reading.

Keep this vault focused on Python language, standard library, typing/object model, async/concurrency, engineering, and Web API development. Do not turn Agent, RAG, LLM, business workflow, product logic, or domain medicine content into this vault's main topic. If source code is Agent-related, record only the Python mechanism and link the code as context.

## Vault root

Candidate paths (check **in this order**, use the **first path that exists**):

1. F:\\我的坚果云\\obsidian_note\\Obsidian Note\\Python (preferred when the vault is on F:)
2. E:\\我的坚果云\\obsidian_note\\Obsidian Note\\Python

If the user specifies a vault path in the message, that overrides the list.

Before creating or updating notes, verify the chosen root exists. Do not create a new vault on the wrong drive when the other candidate already exists.

## Directory Rules

Use these target directories unless the user overrides them:

- `00 - 索引`: index files, problem backlog, templates, Java-to-Python perspective.
- `01 - 语言机制`: syntax and runtime mechanisms, such as `yield`, decorators, context managers, imports.
- `02 - 类型与对象`: type annotations, dataclass, object model, sentinel objects, mutability, Protocol.
- `03 - 异步与并发`: `async` / `await`, `asyncio`, `AsyncIterator`, `AsyncGenerator`, locks, tasks, cancellation.
- `04 - 标准库`: standard-library modules such as `contextlib`, `collections`, `datetime`, `json`, `logging`.
- `05 - 工程化`: project structure, dependency management, testing, logging conventions, code style.
- `06 - Web 开发`: FastAPI, Pydantic, request/response, streaming, SSE.
- `07 - 工作代码案例`: project-specific code-reading notes that only navigate to Python topics.
- `99 - Inbox`: temporary unresolved questions and snippets.

Name files in Chinese first, preserving key English terms where useful:

- `类型注解 Type Annotations.md`
- `AsyncIterator 与 AsyncGenerator.md`
- `object sentinel 哨兵对象.md`

## Workflow

0. Resolve vault root per **Vault root** (F: then E: unless user overrides).
1. Identify the discussed Python knowledge points. If multiple points are mixed together, split them into separate topic notes when they have different reusable meanings.
2. Choose the smallest correct target directory. Prefer a theme note over a project note.
3. Create or update the topic note using the note format below.
4. If the knowledge came from a real source file, add a short entry to a code-case note under `07 - 工作代码案例/<project>/`.
5. Update `00 - 索引/Python 知识索引.md` when a new stable topic note is created.
6. Update `00 - 索引/工作中遇到的 Python 问题.md` by moving completed items from pending to done when applicable.

Do not create many empty future notes. Create only notes for knowledge points actually discussed or requested.

## Note Format

Use this structure for topic notes:

````markdown
# 知识点名称

## 一句话理解

## 它解决什么问题

## 最小示例

```python

```

## 工作代码中的例子

来源：

`文件路径`

代码片段：

```python

```

## Java 对比

## 常见坑

## 什么时候使用

## 相关笔记

- [[]]
````

Keep sections concise. Omit a section only when it is clearly irrelevant, but keep `一句话理解`, `最小示例`, and `相关笔记` for stable topic notes.

## Code-Case Notes

Use code-case notes to preserve source context without turning a project into the taxonomy.

Example path:

`07 - 工作代码案例/medical_agent/chat.py 学习笔记.md`

Use this structure:

````markdown
# chat.py 学习笔记

## 来源

`F:\maven_product\medical_agent\backend-agent\app\api\chat.py`

## 这段代码主要做什么

一句话描述代码职责，只写理解 Python 代码所需的上下文。

## 涉及的 Python 知识点

- `具体写法`：[[对应主题笔记]]

## 待继续追的问题

- [ ] 问题
````

Do not document Agent architecture or business details here.

## Editing Rules

Use surgical edits:

- Preserve existing user notes unless updating the same knowledge point.
- Prefer appending or lightly reshaping over rewriting a user's full note.
- Do not delete unrelated content.
- Do not invent source-code examples. If the exact code was not provided and cannot be read, use a minimal synthetic example and mark it as such.
- Keep Obsidian links as wiki links, such as `[[asyncio.Lock]]`.
