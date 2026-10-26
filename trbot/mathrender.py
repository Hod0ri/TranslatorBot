"""LaTeX 수식을 PNG 이미지로 (matplotlib mathtext)."""
import asyncio
import io
import logging

from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties
from matplotlib.mathtext import MathTextParser

from .config import MATH_MAX_CHARS

log = logging.getLogger(__name__)

_parser = MathTextParser("agg")
_font   = FontProperties(size=18, math_fontfamily="cm")   # Computer Modern (LaTeX 기본 글꼴)


def _render(formula: str) -> bytes | None:
    line = f"${' '.join(formula.strip().strip('$').split())}$"
    if len(line) <= 2 or len(line) > MATH_MAX_CHARS:
        return None
    try:
        _parser.parse(line, prop=_font)   # mathtext 가 지원하지 않는 문법이면 ValueError
    except ValueError:
        return None

    fig = Figure(facecolor="white")
    fig.text(0, 0, line, fontproperties=_font, color="black")
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=200, bbox_inches="tight", pad_inches=0.2)
    return buf.getvalue()


async def render_math(formula: str) -> bytes | None:
    """렌더링할 수 없는 수식이면 None."""
    try:
        return await asyncio.to_thread(_render, formula)
    except Exception:
        log.exception("math render failed")
        return None
