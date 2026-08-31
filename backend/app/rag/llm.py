import asyncio

from fastapi import HTTPException, status
from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import settings

_llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=settings.GEMINI_API_KEY,
)


async def generate_answer(context: str, question: str) -> str:
    prompt = f"""
주어진 참고자료를 기반으로 답변해 주세요.
참고자료에 없는 내용은 추측하지 말고, 모르면 모른다고 답변해 주세요.

[참고자료]
{context}

[질문]
{question}

[답변]
"""

    try:
        if hasattr(_llm, "ainvoke"):
            response = await _llm.ainvoke(prompt)
        else:
            response = await asyncio.to_thread(_llm.invoke, prompt)
        return response.content
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="LLM 호출에 실패했습니다.",
        ) from exc
