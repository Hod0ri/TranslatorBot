"""채널별 설정: 번역 ON, AI 번역 ON, 주제. state.json 에 저장되어 재시작해도 유지된다."""
import json
import logging

from .config import DEFAULT_CHANNELS, STATE_FILE

log = logging.getLogger(__name__)


def _load() -> tuple[set[int], set[int], dict[int, str]]:
    try:
        data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        topics = {int(ch): t for ch, t in data.get("topic", {}).items()}
        return set(data["active"]), set(data["ai"]), topics
    except FileNotFoundError:
        pass
    except (ValueError, KeyError) as e:
        log.warning("%s is broken (%s), using defaults", STATE_FILE.name, e)
    return set(DEFAULT_CHANNELS), set(DEFAULT_CHANNELS), {}


# 다른 모듈은 이 객체들을 직접 고치고 save() 를 부른다
active_channels, ai_channels, channel_topic = _load()


def save():
    data = {
        "active": sorted(active_channels),
        "ai":     sorted(ai_channels),
        "topic":  {str(ch): t for ch, t in channel_topic.items()},
    }
    # 쓰는 도중에 꺼져도 파일이 깨지지 않도록 임시 파일에 쓰고 바꿔치기한다
    tmp = STATE_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(STATE_FILE)
