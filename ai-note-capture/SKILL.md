---
name: ai-note-capture
description: >-
  Capture discussed AI engineering knowledge into the user's Obsidian AI
  knowledge base. Use when the user asks to record, summarize, organize, or
  synthesize knowledge about Agents, MCP, tool use, LLMs, RAG, memory, planning,
  context or prompt engineering, evaluation, or multi-agent systems, including
  mixed Python-and-AI code discussions where AI concepts must be separated from
  Python language mechanisms.
---

# AI Note Capture

## Scope

Create or update durable AI engineering notes from discussion, source material,
or code reading. Keep AI architecture, mechanisms, tradeoffs, failure modes,
and reusable engineering guidance here. Leave Python syntax, typing, async,
standard-library, FastAPI, and general Python mechanisms to
`python-note-capture`; add a cross-link when both notes are useful. Do not
duplicate the same explanation in both knowledge bases.

## Vault root

Use `F:\我的坚果云\obsidian_note\Obsidian Note\AI` by default. A vault path
explicitly supplied by the user overrides this default. Verify the selected
root exists; never fall back to another drive or create a new vault.

Before editing, read the selected root's `AGENTS.md` and the relevant template
under `模板/`. Treat those instructions, the actual tree, and the templates as
authoritative.

## Topic routing

Route to the smallest existing theme that fits:

- Agent architecture and lifecycle: `主题/Agent/`
- MCP protocol and integration: `主题/MCP/`
- General tool selection and ownership: `主题/Tool Use/`
- Retrieval and grounding: `主题/RAG/`
- Context engineering: `主题/Agent/Context Engineering/`
- Memory, planning, evaluation, prompt design, or another theme only when a
  real note requires it.

Create a theme or capability subfolder only while writing an actual note. Do
not pre-create empty topics or `地图/` folders. Route multi-agent material by
its primary engineering topic (often Agent or Tool Use); create a standalone
theme only after enough independent material exists.

## Mainline organization

When a theme has enough real notes, maintain exactly one clearly named
`00 <主题>主线.md` or `00 <主题>总览.md` entry; `00` must sort first in its
directory. Keep the entry as an ordered reading path with stage relationships,
cross-theme links, sources, and explicit gaps. Do not create parallel entry
pages.

Aggregation comes first. Before creating a note, search sibling titles and
content. Append or merge continuous, strongly dependent, same-source material
into an existing cohesive article by default. Split only when the material is
independently reusable by multiple themes, independently sourced or evolving,
independently understandable, or the merged article clearly harms readability.
Never create a new file merely because a new subquestion appears. Use the
practical structure in `模板/主题笔记模板.md` when a new file is justified.
In `## 阅读位置`, label links directionally as `上层主线`,
`前置`, `下一步/相关方案`, `跨主题`, or `工程案例`; include the appropriate
theme `00` mainline link.

Sources remain evidence. Preserve their metadata and `source_type`; link source
notes to extracted knowledge and link knowledge notes back to sources. Do not
invent claims, metadata, dates, URLs, or source text.

## Workflow

1. Identify reusable AI engineering knowledge and separate Python mechanisms.
2. Search existing titles, aliases, and distinctive terms before creating.
3. For external material, create or normalize a source note under
   `原始资料/<type>/`, then synthesize into the primary theme.
4. For discussion or code-reading knowledge, expand or merge an existing
   cohesive note first; create one from `模板/主题笔记模板.md` only when the
   split criteria above are met, and state when no external source was provided.
5. Update the relevant `00` mainline/overview entry only when it has real navigation
   value; keep one entry per mature theme.
6. Verify frontmatter, directional links, source traceability, and that every
   wikilink resolves against the whole vault.

## Editing rules

Preserve existing note bodies and make surgical changes. Do not delete or
broadly reorganize notes unless the user explicitly requests it. Prefer
Chinese filenames while retaining important English terms. Avoid speculative
future notes and accidental placeholders. Do not introduce a MOC entry-kind
field or knowledge-kind taxonomy tags.
