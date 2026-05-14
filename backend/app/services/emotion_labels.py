from __future__ import annotations

from typing import Dict, Iterable, List


DAN_EMOTION_LABELS: List[str] = [
    "neutral",
    "happy",
    "sad",
    "surprise",
    "fear",
    "disgust",
    "anger",
    "contempt",
]

LEGACY_EMOTION_LABELS: List[str] = [
    "serious",
    "tired",
    "excited",
]

EMOTION_LABELS_ZH: Dict[str, str] = {
    "neutral": "平静",
    "happy": "愉快",
    "sad": "悲伤",
    "surprise": "惊讶",
    "fear": "恐惧",
    "disgust": "厌恶",
    "anger": "愤怒",
    "contempt": "轻蔑",
    "serious": "严肃",
    "tired": "疲惫",
    "excited": "兴奋",
}


def ordered_emotion_keys(extra_values: Iterable[str] | None = None) -> List[str]:
    ordered = list(DAN_EMOTION_LABELS)
    for item in LEGACY_EMOTION_LABELS:
        if item not in ordered:
            ordered.append(item)

    for item in extra_values or []:
        value = str(item or "").strip()
        if value and value not in ordered:
            ordered.append(value)
    return ordered

