---
name: simplify-business-code
description: Simplify or refactor business code into the smallest readable implementation that still satisfies the current requirement. Use when the user asks to 精简代码, 简化业务代码, 最小实现, 删除过度封装, 去掉重复判空, 删除无价值 try/catch, 合并过度分层, or explicitly prefers simple business code over defensive programming and enterprise-style abstractions.
---

# Simplify Business Code

将实现收敛到“满足当前需求的最小可用版本”，优先减少代码量、判断、抽象和认知负担，不为假想风险付出复杂度成本。

## Default Stance

- 默认选择更简单、更直接、但已满足当前需求的方案。
- 只做当前需求；不要脑补未来扩展点。
- 可读性优先于工程炫技；命名直接、流程线性、跳转更少。
- 不主动补日志、监控、埋点、告警、重试、熔断、扩展接口或单元测试，除非用户明确要求。

## Keep

- 保留外部输入的必要校验。
- 保留业务规则明确要求的校验。
- 保留会导致明显运行错误的关键前置条件。
- 保留必要的安全、权限、事务、资源清理和异常语义转换。

## Remove First

1. 删除一次性且没有复用价值的小方法封装。
2. 删除上下文已保证的重复判空、判空集合、默认值兜底。
3. 删除只记录日志再抛出、或不增加业务语义的 `try-catch`。
4. 删除与当前需求无关的 fallback、降级、重试、兼容层、预扩展抽象。
5. 合并过度分层、无价值 DTO/helper/adapter 包装。
6. 删除只为理论风险存在的防御式分支。

## Method Split Rule

只有满足以下至少一项时才拆方法：

- 逻辑会在多个地方复用。
- 拆分后明显更好读。
- 该段逻辑本身就是独立业务语义。

否则保持在主流程中，优先内联。

## Refactor Workflow

1. 先读取相关代码，确认真实需求、外部输入边界和上下文已保证的前置条件。
2. 找出真正影响功能正确性的判断、异常处理和业务规则。
3. 优先删除冗余封装、重复校验和无价值异常处理。
4. 合并能线性表达的分支和中间变量，让主流程顺着读就能懂。
5. 输出时默认给最简可用版本，不额外附带“企业级增强版”。

## Guardrails

- 不改变核心功能和对外契约。
- 不删除明确必要的安全和业务规则。
- 无法证明安全可删时，保留并简短说明原因。
- 如果代码已经足够简洁，直接说明不建议继续压缩。

## Response Style

- 先给精简后的最终代码，再给极简说明。
- 说明只聚焦：删了什么、为什么能删、还有什么剩余风险。
- 如果用户还没给代码，先索要目标文件、代码片段或模块范围，不臆造重构结果。
- 当方案 A 更健壮但明显更复杂、方案 B 更简单且已满足当前需求时，默认选择 B。

## Rule of Thumb

只做当前需求需要的最小实现，不为假想风险付出复杂度成本。
