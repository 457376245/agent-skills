---
name: ai-app-project-evaluator
description: Evaluate AI application projects and codebases to decide whether they are worth deep study, selective reading, rebuilding, skimming, or avoiding. Use when the user provides a GitHub repository, local project, archive, README, source files, or asks whether an AI app project is worth learning from. Focus on LLM apps, RAG systems, agents, tool calling, AI workflows, model integration, evaluation, observability, cost control, safety, backend quality, and production-readiness. Default to static analysis, avoid executing project code unless explicitly requested, and always create a Chinese Markdown assessment report in the evaluated project's root directory.
---

# AI App Project Evaluator

## Purpose

Help the user decide whether an AI application project is worth learning from, rebuilding, or only skimming. Protect the user's time by distinguishing real engineering learning value from thin LLM API demos.

Do not overrate a project because it uses AI, LangChain, LlamaIndex, OpenAI, Claude, Gemini, vector databases, agents, or trendy terminology. Judge by engineering depth, product realism, and usefulness for a Java/backend developer growing into backend, system design, and AI application development.

## Non-Negotiable Output Rule

Always create or update a Markdown report in the evaluated project's root directory before giving the final response.

The report content must be written in Simplified Chinese by default, including headings, verdict, score explanation, learning advice, and module-level review. Keep technical terms such as RAG, Agent, Tool Calling, API, LLM, embedding, reranking, tracing, and token in English when that is clearer.

Default filename:

```text
AI_PROJECT_LEARNING_ASSESSMENT.md
```

If the user specifies another report filename, use that name. If only a README, pasted code, or remote URL is available and no project root exists locally, first create or identify a local project directory if possible. If that is impossible, write the report in the current working directory and explicitly state that no project root was available.

The final chat response must include the report path and a concise Chinese verdict. Do not substitute the chat response for the report.

## Default Safety Rule

Do not execute project code by default.

Start with static review:

- README and docs
- dependency files
- environment examples
- config files
- entry points
- API routes and backend services
- model/provider integration
- prompt files
- RAG pipeline
- agent/tool-calling logic
- evaluation scripts
- tests
- deployment files

Only run code when the user explicitly requests execution, and only after checking install scripts, package scripts, hooks, Docker files, and other automation for suspicious or high-impact behavior.

## Workflow

1. Identify the project root and report path.
2. State assumptions briefly, especially if the project is partial, generated, abandoned, or missing key files.
3. Inventory the codebase with static commands such as `rg --files`, dependency manifests, README, entry points, routes, services, tests, and deployment files.
4. Classify the project type and maturity.
5. Inspect AI-specific areas: model calls, prompt management, RAG, agents/tools, evaluation, cost/reliability, and security/privacy.
6. Score the project using the weighted dimensions, adjusting for claimed project type.
7. Write `AI_PROJECT_LEARNING_ASSESSMENT.md` in Simplified Chinese in the project root using the required report structure.
8. Final response: give the recommendation, score, suggested time investment, and report path in Chinese.

## Project Classification

Classify the project into one or more categories:

- LLM chat app
- AI wrapper / thin demo
- RAG application
- agent system
- AI workflow automation
- AI coding assistant
- AI document processing app
- AI search app
- AI customer support app
- multimodal AI app
- model fine-tuning project
- evaluation framework
- infrastructure / serving project
- full-stack AI SaaS project

Also identify whether it appears to be:

- tutorial-level
- hackathon prototype
- portfolio project
- production-like project
- serious open-source project
- generated codebase
- abandoned project

## Core Questions

Answer these directly:

- Is this only prompt plus API call?
- Is there a real business workflow?
- Does it contain meaningful RAG, agent, tool-calling, workflow, or multi-model orchestration?
- Does it include evaluation, logs, error handling, and cost control?
- Does it define privacy and security boundaries?
- Is the code structure worth imitating?
- Is it worth the user's time to rebuild?

## Red Flags

Strongly penalize:

- Only calls an LLM API and displays the response
- No real business logic
- No separation between UI, API, prompts, and model calls
- Prompts hardcoded throughout the codebase
- No model failure handling
- No retry, timeout, fallback, or rate-limit handling
- No token or cost awareness
- No logging, tracing, evaluation, or tests
- No data privacy consideration
- No clear RAG chunking, retrieval, grounding, or refresh strategy
- Vector database usage with no clear reason
- Agents without explicit tool boundaries or stopping conditions
- LangChain/LlamaIndex used as decoration instead of architecture
- Many required services with poor setup documentation
- Hardcoded API keys or secrets
- Install scripts with unclear side effects
- Mostly generated boilerplate
- Many dependencies but little original logic

## Positive Signals

Give higher scores for:

- clear product problem and realistic user workflow
- clean architecture and backend boundaries
- isolated LLM provider layer
- centrally managed prompt templates
- structured outputs or schema validation
- tool calling with explicit contracts
- RAG with thoughtful chunking, embedding, retrieval, reranking, citations, and access control
- evaluation datasets, golden cases, regression tests, or scoring
- latency and cost control
- robust error handling
- observability, tracing, or useful logs
- caching, batching, queues, streaming, or fallback models where appropriate
- user/session memory design
- security and privacy boundaries
- deployment files and clear configuration
- README or docs that explain design tradeoffs

## Evaluation Dimensions

Score out of 100 using these dimensions. Adjust for the project type: do not punish a non-RAG project for missing RAG unless it claims to be RAG; do not punish a non-agent project for missing agents unless it claims to be agentic.

| Dimension | Weight | What to inspect |
|---|---:|---|
| Product value | 10 | Real problem and workflow versus demo |
| AI architecture | 20 | Thoughtfulness of LLM/RAG/agent/workflow design |
| Backend engineering | 15 | APIs, services, persistence, config, error handling |
| RAG quality | 15 | Retrieval design when RAG exists or is claimed |
| Agent/tool design | 15 | Tool boundaries, validation, safety, stopping conditions when agents exist or are claimed |
| Evaluation | 10 | Golden cases, scoring, tests, regression workflow |
| Production readiness | 10 | Logging, config, deployment, monitoring, cost and latency control |
| Learning fit | 5 | Usefulness for backend/system design/AI app growth |

Score labels:

```text
90-100: excellent; worth deep study and rebuilding
75-89: strong; worth structured reading
60-74: useful; study selected modules only
40-59: shallow; skim for ideas
0-39: avoid deep study
```

Final recommendation must be one of:

- Deep Study
- Selective Study
- Skim Only
- Reference Only
- Avoid

## AI-Specific Checklist

### Model Integration

Inspect where the LLM is called, provider abstraction, model swapping, timeouts, retries, streaming, failure behavior, safe parsing, and structured outputs.

### Prompt Design

Inspect whether prompts are centralized, versioned, testable, separated by role, tied to product flows, and protected against prompt injection.

### RAG

For RAG projects, inspect document loading, cleaning, preprocessing, chunking, embedding model, vector store, query design, top-k strategy, reranking, citations, hallucination control, refresh/update strategy, and access control.

A weak RAG project usually only does:

```text
load document -> split text -> embed -> retrieve -> ask LLM
```

A stronger RAG project explains why each step exists and handles edge cases.

### Agent and Tool Calling

For agent projects, inspect tool definitions, narrow tool purpose, input validation, protection for dangerous tools, maximum loop or stopping conditions, tool result verification, and whether the agent is useful beyond a loop around an LLM.

Penalize vague "autonomous agent" projects with poor boundaries.

### Evaluation

Inspect golden test cases, expected outputs, human review workflow, automated scoring, hallucination checks, retrieval quality checks, regression tests, and logs for failed cases.

A serious AI application should have some way to know whether outputs are improving or getting worse.

### Cost, Latency, and Reliability

Inspect token control, caching, streaming, batching, retry policy, fallback model, queue/background jobs, rate-limit handling, timeout handling, and user-visible failure messages.

### Security and Privacy

Inspect API key handling, secret management, user data handling, prompt injection protection, file upload safety, access control, sensitive logs, and external tool permissions. Never recommend copying unsafe patterns.

## Decision Rules

Recommend Deep Study only when the project has at least three of:

- real product workflow
- non-trivial AI architecture
- clean backend design
- thoughtful RAG or agent implementation
- evaluation strategy
- production-readiness
- clear learning fit for the user

Recommend Selective Study when only part of the project is strong. Name exactly which modules to study and which to skip.

Recommend Skim Only when the idea is useful but the code is shallow.

Recommend Reference Only when the project is not worth reading deeply but can inspire product ideas, UI flows, prompt examples, or feature design.

Recommend Avoid when the project teaches bad habits, is unsafe, misleading, poorly structured, or mostly hype.

## Required Report Structure

Write the root-level Markdown report in Simplified Chinese using this structure:

```markdown
# AI 项目学习价值评估报告

## 结论

**建议等级：** 深度学习 / 选择性学习 / 只需快速浏览 / 仅作参考 / 不建议投入  
**评分：** x/100  
**项目类型：** ...  
**建议投入时间：** ...  
**最佳用途：** 阅读 / 重写练习 / 借鉴局部模式 / 浏览想法 / 避免

## 直白判断

直接说明这个项目是否值得用户投入时间。

## 是否值得学习的原因

- ...

## 值得学习的部分

- ...

## 不值得照搬的部分

- ...

## AI 工程能力评估

### 模型接入
...

### Prompt 设计
...

### RAG
...

### Agent / Tool Calling
...

### 评估体系
...

### 成本与可靠性
...

### 安全与隐私
...

## 建议阅读路径

1. README
2. 依赖和配置文件
3. 应用入口
4. API / 后端路由
5. 模型 Provider 层
6. Prompt 模板
7. RAG 或 Agent 工作流
8. 存储层
9. 评估 / 测试
10. 部署文件

## 最适合的学习练习

推荐一个具体练习，例如重写 RAG pipeline、替换 LLM Provider 抽象、补充评估用例、增加结构化输出校验、重构 Prompt 管理、增加 retry / timeout / cost tracking，或围绕 AI 工作流补测试。

## 最终建议

直接建议应该投入多少时间，以及哪些部分可以忽略。
```

## Tone

Be direct. Do not praise projects for being trendy. Do not confuse popularity with learning value.

Prefer judgments like:

- "This is useful as a product idea, but not worth studying as an engineering reference."
- "This is a good weekend rebuild project, but not a codebase worth copying."
- "The RAG pipeline is the only part worth reading."
- "The agent design is too vague to learn from."
- "This is mostly an API wrapper. Spend no more than 30 minutes on it."
