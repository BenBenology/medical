# Medical Consultation System

一个基于 `LLM + Agent + RAG` 的智能问答/问诊演示系统。

目标不是提供医疗级诊断，而是构建一个可演示、可扩展、可解释的 AI 医疗问答 Demo：用户输入自然语言问题，系统结合上下文、风险判断和本地知识库检索，返回结构化回答、风险提示和引用依据。

## Project Goals

- 跑通一个本地可启动的完整主流程
- 支持用户提问并获得结构化回答
- 支持最小多轮追问或流程控制
- 支持基于本地 PDF 的最小 RAG 检索
- 支持证据引用展示
- 为后续独立前端接入预留清晰接口

## Non-Goals

- 不承诺医疗级准确率
- 不做商业化后台或权限系统
- 不做大规模生产部署
- 不在第一版解决复杂评测与运营能力

## Proposed Stack

- Backend: `FastAPI`
- LLM Access: `OpenAI-compatible API` or other pluggable provider
- RAG: `PDF parsing + chunking + embedding + vector retrieval`
- Frontend: 第一版仅预留独立前端接口，不绑定具体框架
- Storage: 本地文件 + 轻量索引/缓存
- Observability: 基础日志、trace id、调试输出

## Current Status

当前仓库已经完成第一批 `V0` 骨架：

- 已初始化 `FastAPI` 项目
- 已初始化本地 `git` 仓库
- 默认分支已调整为 `main`
- 已提供 `GET /health`
- 已提供 `POST /api/chat`
- 已定义基础请求/响应模型
- 已补充基础配置与日志模块
- 已补充最小 API 测试

当前 `/api/chat` 仍然使用占位式 service 响应，还没有接入真实 LLM、风险路由和 PDF RAG。

## MVP Scope

第一版建议先完成下面这条主链路：

1. 用户提交问题
2. 后端接收请求
3. Agent 判断当前应该直接回答、继续追问，还是给出升级提示
4. 如有需要，系统从本地 PDF 知识库检索相关内容
5. LLM 基于问题、上下文和检索结果生成结构化回答
6. API 返回答案、风险等级、追问建议和引用证据
7. 前端或调用方展示结果

## Suggested Response Shape

后端返回的结构建议保持稳定，便于前端演示和后续扩展：

```json
{
  "answer": "根据你的描述，当前更像是一般性上呼吸道症状，但还需要结合持续时间和体温变化判断。",
  "mode": "answer",
  "risk_level": "medium",
  "follow_up_question": "请问症状已经持续多久，是否伴随高热或呼吸困难？",
  "citations": [
    {
      "id": "pdf-001",
      "title": "Respiratory Guidance",
      "snippet": "Document snippet here",
      "source": "docs/knowledge/respiratory.pdf",
      "page": 3
    }
  ],
  "disclaimer": "该结果仅供参考，不能替代线下医生诊疗。"
}
```

## Recommended Directory Layout

```text
medical/
├── PRD.md
├── README.md
├── AGENTS.md
├── TASK.md
├── ARCHITECTURE.md
├── pyproject.toml
├── app/
│   ├── api/
│   │   └── routes.py
│   ├── core/
│   │   ├── config.py
│   │   └── logging.py
│   ├── services/
│   │   └── chat_service.py
│   ├── models/
│   │   └── chat.py
│   └── main.py
└── tests/
    ├── test_api.py
    └── test_core.py
```

## Quick Start

1. 安装依赖

```bash
python3 -m pip install -e '.[dev]'
```

2. 启动服务

```bash
uvicorn app.main:app --reload
```

3. 运行测试

```bash
pytest tests/test_api.py -q
```

4. 访问接口

```bash
curl http://127.0.0.1:8000/health
```

```bash
curl -X POST http://127.0.0.1:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question":"我最近有点头痛，需要注意什么？","session_id":"demo-1"}'
```

## Development Principles

- 先做最小闭环，再做增强能力
- 输出尽量结构化，便于前端展示与调试
- 所有关键流程都保留 fallback
- 高风险场景优先给出升级提示
- 知识库先少量、高质量、可复现

## Safety Notice

本项目是 AI 医疗问答 Demo，不是医疗器械或临床系统。

- 输出只能作为参考信息
- 涉及急症、持续恶化、严重疼痛、呼吸困难、意识改变等情况时，应优先提示尽快就医
- 系统应避免将输出表述成明确诊断结论

## Milestones

- `V0`: 跑通单轮问答，完成前后端联调
- `V1`: 加入多轮追问和最小 RAG 检索
- `V2`: 加入证据引用、状态持久化和更稳定的错误处理
- `V3`: 加入评测脚本、可观测性增强和 UI 优化

## Runbook Status

当前仓库已经进入 `V0` 骨架阶段。下一步应先按 [`TASK.md`](/Users/henryking/Desktop/medical/TASK.md) 继续补齐：

- LLM 调用封装
- 更真实的模式判断
- `.env` 模板
- trace 透传
- 前后端联调约定
- 再进入 PDF RAG

当前 `README.md` 同时承担项目总览和最小运行指南。
