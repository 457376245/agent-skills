---
name: "agy-task-executor"
description: "将用户明确授权的代码或需求文档任务交给 Antigravity CLI（agy）执行并核对结构化结果；仅用于显式委派，不负责正式验收、提交、发布或无明确工作区的任务。"
---

# AGY Task Executor

把一个已经明确范围、工作区和验收标准的任务委派给 Antigravity CLI（agy），并把可审计的执行结果交回 Codex 主 agent。该 skill 只在用户显式调用 `$agy-task-executor` 时使用；它不替代需求澄清、正式 Requirement Doc Review 或人工决策。

## 输入与边界

调用前必须能明确得到：

- 任务目标和成功标准；
- 一个主项目根目录；
- 可选的额外工作区目录（只有用户明确列出的目录才能作为 `--add-dir`）；
- 可选的需求追踪文档、相邻 `*-handoff.md` 和准确的 Conversation UUID。

如果任务或主目录存在歧义，先停止并询问，不要让 agy 自行猜测。Skill 的显式调用只授权 agy 在声明目录内进行本次实现；不授权 commit、push、deploy、删除外部数据、访问未声明目录或修改其他项目。

## 运行流程

### 1. 预检

1. 读取主目录及其父目录中适用的 `AGENTS.md`，再读取任务明确指定的需求文档和交接文档。需求文档模式下还要读取本 skill 的 [执行提示模板](references/executor-prompt.md) 和 [结果 Schema](references/result-schema.json)。
2. 确认 `agy` 可执行文件存在，并确认所有工作区路径是已解析的绝对路径。不要把用户输入拼进 shell 命令字符串。
3. 对每个 Git 项目只读执行 `git status --short --branch` 和 `git rev-parse HEAD`。把现有未提交修改展示给用户；只有用户在当前请求中明确允许“在当前未提交工作区重叠执行”时才继续。Skill 不得替用户丢弃、暂存、提交或覆盖既有修改。
4. 默认启动新会话。禁止使用含义不明确的 `--continue`；只有用户提供并确认格式正确的 UUID 时才追加 `--conversation <UUID>`。
5. 若提供需求追踪文档，检查其范围、验收标准、主项目和关键设计是否仍有实质性 `TBD`。只要未决内容会改变实现、接口、数据、权限或验收，就在启动 agy 前停止，并建议先调用 `$requirement-handoff`；不要替需求文档发明答案。仅元数据类 TBD 可继续，但必须在结果中保留。

### 2. 构造任务 Prompt

以 [执行提示模板](references/executor-prompt.md) 为骨架填入任务、主目录、额外目录、需求文档、交接文档、验收标准和允许的变更范围。Prompt 必须要求 agy：

- 先阅读适用的 `AGENTS.md`、需求文档和交接文档；
- 遵守最小实现和手术式修改，只触碰完成任务所需的文件；
- 保护调用前已有修改，不执行 commit、push、deploy 或越界删除；
- 运行与验收标准对应的验证，并如实区分通过、失败、未运行和无法验证；
- 需求增强模式下更新真实的实施状态、代码清单、验证记录、偏差、风险和审查目标；
- 最终只输出符合 `result-schema.json` 的 JSON 对象。

### 3. 启动 agy

通过本环境的 PowerShell 执行能力，以主项目根目录作为当前工作目录，使用参数数组直接调用 `agy`。默认参数固定为：

```text
-p <prompt>
--mode accept-edits
--dangerously-skip-permissions
--effort high
--output-format json
--json-schema <absolute path to references/result-schema.json>
--print-timeout 30m
--disable-slash-commands
```

不固定 `--model` 或 `--agent`，不追加 `--project` 或 `--new-project`，除非用户明确要求。每个额外目录分别追加 `--add-dir <absolute path>`。若有准确 Conversation UUID，再追加 `--conversation <UUID>`。

参数数组的最小形状如下；`$prompt`、`$schemaPath`、`$primaryRoot` 和 `$additionalRoots` 必须来自已经预检并解析的值，不要用字符串拼接伪造命令：

```powershell
$schemaPath = [System.IO.Path]::GetFullPath(
    (Join-Path -Path $skillRoot -ChildPath 'references/result-schema.json')
)
$agyArgs = @(
    '-p', $prompt,
    '--mode', 'accept-edits',
    '--dangerously-skip-permissions',
    '--effort', 'high',
    '--output-format', 'json',
    '--json-schema', $schemaPath,
    '--print-timeout', '30m',
    '--disable-slash-commands'
)
foreach ($additionalRoot in $additionalRoots) {
    $agyArgs += @('--add-dir', $additionalRoot)
}
if ($conversationId) {
    $agyArgs += @('--conversation', $conversationId)
}
& agy @agyArgs
$agyExitCode = $LASTEXITCODE
```

如需分离 stdout 和 stderr，只能使用任务专用的临时文件或等价的进程 API，且不得写入项目目录；结束后只清理本次创建并已确认的临时文件。记录退出码、原始 JSON、stderr 和超时信息。

### 4. 结果核对与交接

agy 返回后，Codex 主 agent 只做只读核对：

- 退出码是否为 0，stdout 是否能解析为 agy 的 JSON 运行结果；当顶层包含 `structured_output` 时，取该字段作为最终结果并单独按 Schema 校验（顶层的 `conversation_id`、`response`、`usage` 等是 CLI envelope，不属于任务结果 Schema）；只有没有 envelope 时才直接校验顶层对象；
- `status`、变更文件、验证命令/结果、验收证据、偏差、阻塞和风险是否与实际输出一致；
- Git diff、变更路径和测试证据是否只落在已声明范围；
- 需求增强模式下，需求文档是否记录真实实施状态、实际文件和验证结果。完成时必须是 `实施状态：已完成`、`审查状态：待审查`，审查目标必须包含 `未提交工作区 + 当前 HEAD SHA`；阻塞或失败必须保持真实状态，不能伪造完成。

如果 JSON 无法解析、Schema 不合规、退出码非零、超时、结果缺少关键证据或发生越界修改，报告为失败/未验证并停止。不要自动重试、不要自动调用 `$requirement-doc-review`、不要修改 agy 的实现结果，也不要由 Codex 静默接管实现。只有用户另行明确要求时，才进入正式验收流程。

最终向用户返回：agy 结构化结果、退出码、只读 Git 核对、需求文档状态、未验证事项和剩余风险；不要把“agy 声称完成”改写为 Codex 的正式验收结论。
