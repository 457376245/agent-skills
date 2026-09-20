---
name: log
description: 查看 D:\H\tmp\log 目录中按最后修改时间倒序排列的最新一个 .log 或 .txt 日志文件。用户要求查看最新日志、最近日志、log 或该固定目录日志时使用。
---

# 查看最新日志

无需二次确认，直接执行：

1. 使用 PowerShell 获取目录顶层最后修改时间最新的 `.log` 或 `.txt` 文件：

```powershell
Get-ChildItem -LiteralPath 'D:\H\tmp\log' -File |
  Where-Object { $_.Extension -in '.log', '.txt' } |
  Sort-Object LastWriteTime -Descending |
  Select-Object -First 1 -ExpandProperty FullName
```

2. 使用读取工具打开返回的文件，并向用户展示日志内容和文件路径。
3. 目录不存在、没有 `.log` / `.txt` 文件或读取失败时，直接报告具体错误。

仅查看日志；不要修改、移动或删除任何文件。
