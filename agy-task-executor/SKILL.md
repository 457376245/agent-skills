---
name: "agy-task-executor"
description: "将用户明确授权的代码或需求文档任务交给 Antigravity CLI（agy）执行，由调用方审查并持续委派返修至可提交；仅用于显式委派，不负责正式验收、提交、发布或无明确工作区的任务。"
---

# AGY Task Executor

把一个已经明确范围、工作区和验收标准的任务委派给 Antigravity CLI（agy），由 Codex 主 agent 审查实际改动；发现可修复问题时继续委派 agy，直至达到可提交状态或出现明确阻塞。该 skill 只在用户显式调用 `$agy-task-executor` 时使用；它不替代需求澄清、正式 Requirement Doc Review 或人工决策。

## 输入与边界

调用前必须能明确得到：

- 任务目标和成功标准；
- 一个主项目根目录；
- 可选的额外工作区目录（只有用户明确列出的目录才能作为 `--add-dir`）；
- 可选的需求追踪文档、相邻 `*-handoff.md` 和准确的 Conversation UUID。

如果任务或主目录存在歧义，先停止并询问，不要让 agy 自行猜测。Skill 的显式调用授权 agy 在声明目录内完成本次实现及其审查返修轮次；不授权 commit、push、deploy、删除外部数据、访问未声明目录或修改其他项目。“可提交”只表示调用方审查通过，不表示已经执行 Git 提交。

## 运行流程

### 1. 预检

1. 读取主目录及其父目录中适用的 `AGENTS.md`，再读取任务明确指定的需求文档和交接文档。需求文档模式下还要读取本 skill 的 [执行提示模板](references/executor-prompt.md) 和 [结果 Schema](references/result-schema.json)。
2. 确认 `agy` 可执行文件存在，并确认所有工作区路径是已解析的绝对路径。不要把用户输入拼进 shell 命令字符串。只读执行 `agy models`，从形如 `gemini-<版本>-flash-high` 的可用模型中按数值版本选择最新版；例如当前应选择 `gemini-3.8-flash-high`。如果模型列表无法读取或没有匹配项，停止执行，不要回退到其他模型。
3. 对每个 Git 项目只读执行 `git status --short --branch` 和 `git rev-parse HEAD`。把现有未提交修改展示给用户；只有用户在当前请求中明确允许“在当前未提交工作区重叠执行”时才继续。Skill 不得替用户丢弃、暂存、提交或覆盖既有修改。
4. 首轮默认启动新会话；若用户提供并确认格式正确的 UUID，则从该会话开始。禁止使用含义不明确的 `--continue`。返修轮次优先使用上一轮 CLI envelope 返回的准确 `conversation_id` 追加 `--conversation <UUID>`；若上一轮没有返回准确 UUID，则启动新会话，并在返修 Prompt 中补全原任务和审查结论。
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
--model <预检得到的最新版 Gemini Flash High 模型标识>
--effort high
--output-format json
--json-schema <absolute path to references/result-schema.json>
--print-timeout 30m
--disable-slash-commands
```

不固定 `--agent`，不追加 `--project` 或 `--new-project`，除非用户明确要求。`--model` 使用预检得到的最新版 Gemini Flash High 模型标识；只有用户明确指定其他模型时才覆盖该默认选择。每个额外目录分别追加 `--add-dir <absolute path>`。若有准确 Conversation UUID，再追加 `--conversation <UUID>`。

参数数组的最小形状如下；`$prompt`、`$schemaPath`、`$model`、`$primaryRoot` 和 `$additionalRoots` 必须来自已经预检并解析的值，不要用字符串拼接伪造命令：

```powershell
$schemaPath = [System.IO.Path]::GetFullPath(
    (Join-Path -Path $skillRoot -ChildPath 'references/result-schema.json')
)
$agyArgs = @(
    '-p', $prompt,
    '--mode', 'accept-edits',
    '--dangerously-skip-permissions',
    '--model', $model,
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

agy 进入后台执行后，只在启动后的第 5、10、15、20、25 分钟查询一次状态。除进程提前完成、失败或达到 `--print-timeout 30m` 外，不得在这些时间点之间轮询。状态未变化时只向用户返回一句简短进度，不重复命令、Prompt 或既有日志；第 25 分钟查询后直接等待进程完成或 30 分钟超时。

如需分离 stdout 和 stderr，只能使用任务专用的临时文件或等价的进程 API，且不得写入项目目录；结束后只清理本次创建并已确认的临时文件。记录退出码、原始 JSON、stderr 和超时信息。

### 4. 调用方审查与返修闭环

agy 每轮返回后，Codex 主 agent 必须独立审查，不得只采信 agy 的完成声明。调用方可以读取文件、Git 状态和 diff，并运行与验收标准直接相关的验证，但不得亲自修改 agy 的实现结果。审查至少包括：

- 退出码是否为 0，stdout 是否能解析为 agy 的 JSON 运行结果；当顶层包含 `structured_output` 时，取该字段作为最终结果并单独按 Schema 校验（顶层的 `conversation_id`、`response`、`usage` 等是 CLI envelope，不属于任务结果 Schema）；只有没有 envelope 时才直接校验顶层对象；
- `status`、变更文件、验证命令/结果、验收证据、偏差、阻塞和风险是否与实际文件和行为一致；
- Git status、diff、未跟踪文件、变更路径和测试证据是否只落在已声明范围，且没有覆盖调用前已有修改；
- 实现是否满足原任务、验收标准、适用的 `AGENTS.md`、需求文档和交接文档，相关验证是否真实通过，是否仍有阻止提交的正确性、兼容性、安全性或维护性问题；
- 需求增强模式下，需求文档是否记录真实实施状态、实际文件和验证结果。完成时必须是 `实施状态：已完成`、`审查状态：待审查`，审查目标必须包含 `未提交工作区 + 当前 HEAD SHA`；阻塞或失败必须保持真实状态，不能伪造完成。

只有同时满足以下条件，调用方才能判定“可提交”：所有验收标准均有可信证据并满足，必要验证已通过，Git 变更完整且在授权范围内，没有未解决的阻断级审查发现，需求文档（若有）已与真实实现对齐。未验证事项会影响正确性或验收时，不得判定可提交。

若实现尚不可提交但问题可在原任务和授权目录内修复，调用方必须整理一份具体返修 Prompt，逐项写明问题位置、可观察证据、违反的验收标准和期望结果，再继续委派 agy。不要替 agy 直接改代码，也不要扩大原范围或指定不必要的实现方式。返修轮次沿用相同的模型、权限、结构化输出、超时和状态查询规则，并优先续接上一轮准确的 `conversation_id`。每轮返修后重新执行完整审查；新问题或未修复问题继续进入下一轮。

以下情况停止闭环并如实报告阻塞或失败：JSON 无法解析、Schema 不合规、退出码非零或超时；修复需要用户决策、新权限或超出声明目录；发生越界修改；同一阻断问题经过连续两轮返修仍存在；或连续两轮没有实质进展。不要自动调用 `$requirement-doc-review`，不要由 Codex 静默接管实现。只有用户另行明确要求时，才进入正式验收流程。

最终向用户返回：总执行轮次、agy 最后一轮结构化结果与退出码、调用方的“可提交”或“阻塞/失败”审查结论、Git 核对、验证结果、需求文档状态、未验证事项和剩余风险。明确说明 skill 没有执行 commit 或 push；调用方自己的审查结论必须与证据对应，不能把“agy 声称完成”直接改写为可提交。
