"""언어 감지와, 번역하지 않고 그대로 둘 구간(코드, 이모지)."""
import re

from langdetect import LangDetectException, detect


def is_japanese(text: str) -> bool:
    return any(
        0x3040 <= ord(c) <= 0x309F or   # 히라가나
        0x30A0 <= ord(c) <= 0x30FF or   # 가타카나
        0x4E00 <= ord(c) <= 0x9FFF      # 한자
        for c in text
    )


def is_korean(text: str) -> bool:
    return any(0xAC00 <= ord(c) <= 0xD7A3 for c in text)


def has_kanji(text: str) -> bool:
    return any(0x4E00 <= ord(c) <= 0x9FFF for c in text)


def detect_language(text: str) -> str | None:
    """'ko', 'ja', 또는 둘 다 아니면 None."""
    has_ko = is_korean(text)
    has_ja = is_japanese(text)
    if has_ko != has_ja:
        return "ko" if has_ko else "ja"
    if has_ko:   # 둘 다 섞여 있으면 langdetect 로 판단
        try:
            lang = detect(text)
            if lang in ("ko", "ja"):
                return lang
        except LangDetectException:
            pass
    return None


# ```코드 블록``` 과 `인라인 코드`
CODE = r"```.*?```|`[^`\n]+`"
# 커스텀 이모지 <:name:id> 와 유니코드 이모지. ZWJ(200D), 이모지 표시(FE0F), 키캡(20E3)까지 한 덩어리로 묶는다
EMOJI = r"<a?:\w+:\d+>|[⌀-⏿☀-➿⬀-⯿\U0001F000-\U0001FAFF‍️⃣]+"

# split 하면 짝수 인덱스가 번역할 텍스트, 홀수 인덱스가 그대로 둘 구간이 된다.
# AI 는 이모지를 문장째로 받아 자연스럽게 배치하므로 코드만 떼고(CODE_RE),
# Google 은 이모지를 망가뜨리므로 이모지까지 뗀다(KEEP_RE)
CODE_RE = re.compile(f"({CODE})", re.DOTALL)
KEEP_RE = re.compile(f"({CODE}|{EMOJI})", re.DOTALL)


def strip_kept(text: str) -> str:
    """코드와 이모지를 뺀 텍스트. 언어 감지용."""
    return "".join(KEEP_RE.split(text)[::2])
