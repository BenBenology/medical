from uuid import uuid4

from app.models.chat import ChatRequest, ChatResponse


DEFAULT_DISCLAIMER = "该结果仅供参考，不能替代线下医生诊疗。"


def generate_chat_response(request: ChatRequest) -> ChatResponse:
    question = request.question.strip()
    answer = (
        f"你提到的问题是：{question}。当前版本先返回一个结构化的基础建议，"
        "后续会接入更完整的风险判断和 PDF 检索能力。"
    )

    return ChatResponse(
        answer=answer,
        mode="answer",
        risk_level="medium",
        follow_up_question=None,
        citations=[],
        disclaimer=DEFAULT_DISCLAIMER,
        trace_id=f"trace-{uuid4().hex[:12]}",
    )
