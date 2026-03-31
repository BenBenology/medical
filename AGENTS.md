# AGENTS.md

本文件定义本项目中人类开发者与代码 Agent 的默认协作方式。

## Mission

围绕 `Medical Consultation System` 构建一个可演示、可扩展、可解释的 AI 医疗问答 Demo，优先保证：

- 最小闭环可运行
- 结构化输出稳定
- 高风险场景处理谨慎
- 文档与代码保持一致

## Product Guardrails

- 这是 Demo，不是医疗诊断系统
- 不得在文案或代码中暗示“医疗级准确率”或“替代医生”
- 高风险场景必须优先考虑升级提示或建议就医
- 证据展示应明确标注来源，不得伪造引用
- 若知识库不足以支撑结论，应允许系统明确表达不确定性

## Engineering Priorities

按以下顺序决策：

1. 可运行的最小闭环
2. 清晰边界和稳定接口
3. 可解释性与可调试性
4. 扩展性
5. 局部性能优化

## Architecture Expectations

Agent 在实现时应遵守以下边界：

- `api` 负责 HTTP 请求和响应模型，不写复杂业务判断
- `services` 负责业务编排，如会话处理、回答生成
- `rag` 负责 PDF 解析、切片、向量检索和引用组装
- `core` 负责配置、日志、模型客户端、公共基础设施
- `models` 负责 schema、DTO、领域模型
- 前端视为独立调用方，通过稳定 API 对接后端

## Collaboration Rules

- 先读 `PRD.md`、`README.md`、`ARCHITECTURE.md` 再做大改
- 每次开始实现、修改代码或执行关键 action 之前，先阅读相关 Markdown 文档，至少包括需求、架构和任务文档
- 修改接口时同步更新相关文档
- 每次完成代码改动后，必须同步检查并更新相关 Markdown 文档，确保文档与实现一致
- 优先做小步提交，避免一次性大改
- 不为了“看起来高级”引入过度复杂的 Agent 编排
- 不在没有证据的情况下引入复杂持久化、消息队列或微服务

## Coding Rules

- Python 代码优先简单、清晰、可测
- 尽量保持函数职责单一
- 所有核心返回结构都应使用明确 schema 定义
- 外部模型调用必须有 timeout、错误处理和 fallback
- RAG 检索失败时，系统仍应能返回保守回答或显式提示

## Testing Rules

至少覆盖以下测试或自测能力：

- 一个 API 主流程测试
- 一个 Agent 路由判断测试
- 一个最小 RAG 检索测试
- 一个高风险提示场景测试

如果测试尚未完善，至少提供可重复执行的自测脚本。

## Documentation Rules

以下文档视为项目基线，变更时应尽量同步：

- [`PRD.md`](/Users/henryking/Desktop/medical/PRD.md)
- [`README.md`](/Users/henryking/Desktop/medical/README.md)
- [`TASK.md`](/Users/henryking/Desktop/medical/TASK.md)
- [`ARCHITECTURE.md`](/Users/henryking/Desktop/medical/ARCHITECTURE.md)

## Preferred Delivery Style

当 Agent 执行任务时，默认遵循：

- 先确认当前目标属于 `V0`、`V1`、`V2` 还是 `V3`
- 优先完成当前版本最关键路径
- 做完后说明变更点、风险点和验证方式
- 如果发现 PRD 与实现冲突，先更新文档或提出冲突说明

## What To Avoid

- 假设模型输出永远稳定
- 把 prompt 逻辑和 API 路由硬耦合在一起
- 直接把 PDF 原文整段塞给前端作为“证据”
- 用前端临时逻辑掩盖后端响应结构问题
- 跳过风险控制与免责声明

## Default Definition Of Done

一个任务默认完成，需要同时满足：

- 功能达到当前版本目标
- 关键路径可运行或可验证
- 文档与实现一致
- 已说明已知限制与下一步
