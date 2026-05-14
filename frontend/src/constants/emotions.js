export const EMOTION_LABELS = {
  neutral: "平静",
  happy: "愉快",
  sad: "悲伤",
  surprise: "惊讶",
  fear: "恐惧",
  disgust: "厌恶",
  anger: "愤怒",
  contempt: "轻蔑",
  serious: "严肃",
  tired: "疲惫",
  excited: "兴奋",
};

export const DEFAULT_EMOTION_ORDER = [
  "neutral",
  "happy",
  "sad",
  "surprise",
  "fear",
  "disgust",
  "anger",
  "contempt",
  "serious",
  "tired",
  "excited",
];

export const EMOTION_OPTIONS = DEFAULT_EMOTION_ORDER.map((value) => ({
  value,
  label: EMOTION_LABELS[value] || value,
}));

export function formatEmotion(value) {
  return EMOTION_LABELS[value] || value || "-";
}
