---
name: direct-test-command-writer
description: Generate direct, copyable local test commands and write them to files after or alongside testing, using --args-file JSON inputs for MCP/tool tests. Use when the user asks to create testing commands, save test commands to a file, avoid complex scripts, avoid PowerShell-specific JSON quoting, produce cmd commands for MCP/tools/API tests, or preserve the exact commands and test input files used for later reuse.
---

# Direct Test Command Writer

## Workflow

Use this skill when producing reusable local test commands, especially for Windows MCP/tool tests.

1. Prefer direct one-line commands over wrapper scripts.
2. Use `cmd /d /c "..."` when the command may be pasted into either PowerShell or cmd.
3. Start with `cd /d <project-dir> &&` inside the command so it works from any current directory.
4. For MCP tool tests, write tool arguments to a JSON file and use `--args-file <json-file>`. Do not inline JSON or lenient `{key:value}` arguments in PowerShell/cmd commands by default.
5. Keep command files simple: one direct command per line, optionally separated by blank lines. Do not create variables, loops, `@echo off`, or `setlocal` unless the user explicitly requests a runnable script.
6. After testing or finalizing the commands, write both the exact commands and their JSON input files. Use user-specified paths when given; otherwise place them near the relevant test scripts, such as `scripts/test_<topic>.cmd` and `scripts/<tool>_args.json`.

## Command Style

Prefer this shape:

```cmd
cmd /d /c "cd /d E:\path\to\project && chcp 65001 >nul && .\.venv\Scripts\python.exe .\scripts\test_mcp_tool.py --endpoint http://127.0.0.1:9000/info/mcp --tool tool_name --args-file .\scripts\tool_name_args.json"
```

Keep each command on one physical line in the file. Blank lines between commands are acceptable.

Use `chcp 65001 >nul` for consistency. Prefer ASCII-only JSON files for Chinese values by using JSON unicode escapes when helpful, e.g. `"\u5168\u90e8"` for `全部`.

## File Contents

The command file should contain only directly copyable commands unless the user asks for comments or executable script behavior. The argument JSON files should be valid strict JSON.

Good:

```cmd
cmd /d /c "cd /d E:\ZHONGZHAI\DQ_Project\dq-ai && chcp 65001 >nul && .\.venv\Scripts\python.exe .\scripts\test_mcp_tool.py --endpoint http://127.0.0.1:9000/info/mcp --tool get_ccdc_observe_news --args-file .\scripts\ccdc_observe_args.json"

cmd /d /c "cd /d E:\ZHONGZHAI\DQ_Project\dq-ai && chcp 65001 >nul && .\.venv\Scripts\python.exe .\scripts\test_mcp_tool.py --endpoint http://127.0.0.1:9000/info/mcp --tool get_monitor_reminder_news --args-file .\scripts\monitor_reminder_args.json"
```

Good argument file:

```json
{"query_date":"2026-05-28","monitor_reminder_type":"\u5168\u90e8"}
```

Avoid:

```cmd
cmd /d /c "cd /d E:\ZHONGZHAI\DQ_Project\dq-ai && chcp 65001 >nul && .\.venv\Scripts\python.exe .\scripts\test_mcp_tool.py --endpoint http://127.0.0.1:9000/info/mcp --tool get_monitor_reminder_news --args {query_date:2026-05-28,monitor_reminder_type:全部}"
```

## Verification

When feasible, run the direct commands once before saving or after saving. If the service is not running or the command depends on user-local state, still write the command file and state that runtime verification was not performed.

For MCP tool tests, successful output usually includes:

```text
has_<tool_name>=True
is_error=False
```
