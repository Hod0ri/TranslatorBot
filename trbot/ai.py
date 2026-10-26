"""OpenAI 호출과 사용량 집계."""
import re

import openai

from .config import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_SERVICE_TIER

client = openai.AsyncOpenAI(api_key=OPENAI_API_KEY)

# 이번 실행의 누적 사용량 (/tr credits)
usage_stats = {"prompt": 0, "completion": 0, "calls": 0}

# 모델별 단가 (입력, 출력) $/1M 토큰. 2026-10 기준 https://developers.openai.com/api/docs/pricing
PRICES = {
    "gpt-4o-mini":  (0.15, 0.60),
    "gpt-4.1-mini": (0.40, 1.60),
    "gpt-4.1":      (2.00, 8.00),
    "gpt-5.4-mini": (0.75, 4.50),
    "gpt-6-luna":   (0.10, 0.50),
}

# 추론형 모델(gpt-5 이후, o 시리즈)은 temperature 를 받지 않는다.
# 짧은 작업이라 추론을 끈다(none). 기본값(medium)이면 느려서 AI_TIMEOUT 에 걸리기 쉽다
IS_REASONING_MODEL = re.match(r"gpt-([5-9]|\d\d)|o\d", OPENAI_MODEL) is not None

# 모델이 입력을 감싼 태그를 따라 출력하는 경우가 있어 결과에서 지운다
_TAG_RE = re.compile(r"</?(?:text|context|participants)>")


async def complete(system: str, user: str, temperature: float, max_tokens: int) -> str:
    """시스템/사용자 메시지 하나씩으로 호출하고, 입력 태그를 지운 응답 텍스트를 돌려준다."""
    options = {"reasoning_effort": "none"} if IS_REASONING_MODEL else {"temperature": temperature}
    if OPENAI_SERVICE_TIER:
        options["service_tier"] = OPENAI_SERVICE_TIER
    response = await client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": user},
        ],
        max_completion_tokens=max_tokens,
        **options,
    )
    if usage := response.usage:
        usage_stats["prompt"]     += usage.prompt_tokens
        usage_stats["completion"] += usage.completion_tokens
        usage_stats["calls"]      += 1

    content = response.choices[0].message.content
    if not content:
        raise RuntimeError(f"empty response (finish_reason={response.choices[0].finish_reason})")
    return _TAG_RE.sub("", content).strip()


def estimated_cost() -> float | None:
    price = PRICES.get(OPENAI_MODEL)
    if price is None:
        return None
    cost = (usage_stats["prompt"] * price[0] + usage_stats["completion"] * price[1]) / 1_000_000
    # Fast 모드(예전 이름 priority)는 일반 단가의 2배
    return cost * 2 if OPENAI_SERVICE_TIER in ("fast", "priority") else cost
