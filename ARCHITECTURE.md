# ARCHITECTURE.md

## Overview

`Medical Consultation System` 采用 `Python-first` 的后端架构，目标是在尽量少的复杂度下完成一个可演示的 AI 医疗问答闭环。

第一版默认形态：

- 后端：`FastAPI`
- 前端：独立前端预留，通过 HTTP API 调用
- 编排：轻量 `Agent/Orchestrator`
- 检索：本地 PDF 最小 RAG
- 模型：可替换的 LLM Provider
- 调试：基础日志与 trace

系统核心目标不是“最智能”，而是“最小闭环稳定、结构清晰、便于展示和扩展”。

## Current Implementation Snapshot

当前已落地的实现非常轻，主要用于跑通 `V0`：

- [`app/main.py`](/Users/henryking/Desktop/medical/app/main.py) 创建 FastAPI 应用
- [`app/api/routes.py`](/Users/henryking/Desktop/medical/app/api/routes.py) 暴露 `/health` 和 `/api/chat`
- [`app/models/chat.py`](/Users/henryking/Desktop/medical/app/models/chat.py) 定义基础 schema
- [`app/services/chat_service.py`](/Users/henryking/Desktop/medical/app/services/chat_service.py) 返回占位式结构化回答
- [`tests/test_api.py`](/Users/henryking/Desktop/medical/tests/test_api.py) 覆盖最小接口测试

这说明骨架已经成型，但离完整的 Agent 决策、Safety、RAG 和 LLM 调用还有距离。

## Architecture Principles

- 先跑通主流程，再增强效果
- 模块分层明确，避免路由层直接承载业务复杂度
- 风险控制与解释性是核心能力，不是补丁能力
- 检索和生成可独立替换
- 前端与后端通过稳定 schema 解耦

## High-Level Components

### 1. API Layer

职责：

- 接收前端请求
- 参数校验
- 注入 trace id
- 调用编排层
- 返回统一结构响应

建议目录：

```text
app/api/
```

典型接口：

- `GET /health`
- `POST /api/chat`

### 2. Orchestrator Layer

职责：

- 汇总上下文
- 判断当前处理模式
- 决定是否需要追问、升级提示或触发 RAG
- 调用 LLM 生成最终回答

建议目录：

```text
app/services/orchestrator.py
```

第一版不需要复杂多 Agent 系统。一个清晰的编排器比多个“看起来高级”的 Agent 更适合当前范围。

当前状态：

- 尚未单独拆出 `orchestrator.py`
- 目前由 [`app/services/chat_service.py`](/Users/henryking/Desktop/medical/app/services/chat_service.py) 临时承担最小响应生成职责

### 3. Safety Layer

职责：

- 判断高风险场景
- 在紧急或不确定场景下抬高提示级别
- 控制输出语气，避免形成明确医疗诊断暗示

建议实现方式：

- 第一版以规则 + prompt 约束为主
- 后续再视需要加入更细分的风险分类器

### 4. RAG Layer

职责：

- 解析本地 PDF
- 清洗文本并切片
- 建立检索索引
- 根据用户问题召回相关片段
- 组装引用元数据

建议目录：

```text
app/rag/
```

可拆分为：

- `loader.py`: 文档发现与载入
- `parser.py`: PDF 文本提取
- `chunker.py`: 切片
- `indexer.py`: 索引构建
- `retriever.py`: 检索

### 5. LLM Client Layer

职责：

- 封装模型供应商调用
- 管理 prompt 输入输出
- 处理超时、重试和错误降级

建议目录：

```text
app/core/llm.py
```

当前状态：

- 尚未实现
- 下一步应先补一个可替换的 provider 封装和最小错误处理

### 6. Schema Layer

职责：

- 统一请求和响应数据结构
- 限制前后端契约漂移
- 为日志、测试和接口文档提供基础

建议目录：

```text
app/models/
```

当前状态：

- 已落地 [`app/models/chat.py`](/Users/henryking/Desktop/medical/app/models/chat.py)
- 已包含 `ChatRequest`、`ChatResponse`、`Citation`

## Suggested Request Flow

```text
User Question
  -> FastAPI /api/chat
  -> Request validation + trace id
  -> Orchestrator
     -> Safety check
     -> Mode decision
     -> Optional RAG retrieval
     -> LLM generation
     -> Citation assembly
  -> Structured response
  -> Frontend rendering
```

## Mode Decision

第一版建议把系统行为限制在三种模式：

- `answer`: 信息足够，可直接回答
- `follow_up`: 信息不足，先追问一个关键问题
- `escalate`: 风险较高，优先建议尽快就医或升级处理

这样做的好处是：

- 响应结构稳定
- 前端展示简单
- 日志和测试更容易写
- 避免过早走向复杂状态机

## Response Contract

建议统一响应结构如下：

```json
{
  "answer": "string",
  "mode": "answer | follow_up | escalate",
  "risk_level": "low | medium | high",
  "follow_up_question": "string | null",
  "citations": [
    {
      "id": "string",
      "title": "string",
      "snippet": "string",
      "source": "string",
      "page": 1
    }
  ],
  "disclaimer": "string",
  "trace_id": "string"
}
```

## Knowledge Base Strategy

知识库默认来源于本地 PDF 或指南类资料。

第一版策略：

- 只接少量高质量 PDF
- 保留文件名和页码
- 保持切片规则简单稳定
- 优先保证引用能回溯，而不是追求复杂召回策略

已知风险：

- PDF 解析质量可能不稳定
- 不同文档格式会影响切片质量
- 引用质量上限取决于源文档质量

## Error Handling Strategy

系统至少要处理以下失败路径：

- LLM 调用失败
- PDF 解析失败
- 检索结果为空
- 输出结构不完整

建议降级策略：

- LLM 失败：返回保守说明和建议稍后重试
- RAG 失败：允许返回无引用回答，但标记依据不足
- 高风险命中：即使生成失败，也优先返回升级提示

## Logging And Trace

第一版只做最小能力：

- 每次请求生成 `trace_id`
- 记录请求时间、模式决策、是否触发 RAG、错误摘要
- 不记录不必要的用户隐私明文

## Testing Strategy

建议优先覆盖四类验证：

- API 主流程是否可用
- 模式判断是否稳定
- PDF 检索是否能返回至少一个有效引用
- 高风险场景是否能触发升级提示

## Future Evolution

后续可以按这个方向演进：

1. 接入独立前端应用
2. 引入更稳的会话状态管理
3. 加入更完善的评测集和回归测试
4. 加入更细粒度的安全分类
5. 替换或增强检索与 rerank 能力

## Boundary Statement

这套架构的定位是“适合第一版演示系统的清晰骨架”，不是生产级医疗平台设计。

如果未来要走生产化，需要单独补齐：

- 合规与审计
- 隐私与安全治理
- 更严格的医学内容评估
- 更稳的可观测性与部署体系
