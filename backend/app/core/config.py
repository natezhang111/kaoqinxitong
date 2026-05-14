from __future__ import annotations

from pathlib import Path
from typing import Dict, List

BASE_DIR = Path(__file__).resolve().parents[2]
APP_DIR = BASE_DIR / "app"
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"

JSON_DIR = DATA_DIR / "json"
FACES_DIR = DATA_DIR / "faces"
FEATURES_DIR = DATA_DIR / "features"
UPLOADS_DIR = DATA_DIR / "uploads"
ATTENDANCE_UPLOAD_DIR = UPLOADS_DIR / "attendance"
GROUP_PHOTO_UPLOAD_DIR = UPLOADS_DIR / "group_photos"
ATTACK_SAMPLES_DIR = UPLOADS_DIR / "attack_samples"
REPORTS_DIR = DATA_DIR / "reports"
LOGS_DIR = DATA_DIR / "logs"

USERS_JSON = JSON_DIR / "users.json"
STUDENTS_JSON = JSON_DIR / "students.json"
ATTENDANCE_JSON = JSON_DIR / "attendance_records.json"
ACTIVITIES_JSON = JSON_DIR / "activities.json"
ACTIVITY_FACE_RESULTS_JSON = JSON_DIR / "activity_face_results.json"
EMOTION_RECORDS_JSON = JSON_DIR / "emotion_records.json"
SECURITY_TEST_RECORDS_JSON = JSON_DIR / "security_test_records.json"
EVALUATION_RECORDS_JSON = JSON_DIR / "evaluation_records.json"
AUDIT_LOGS_JSON = JSON_DIR / "audit_logs.json"

DEFAULT_JSON_FILES: List[str] = [
    "users.json",
    "students.json",
    "attendance_records.json",
    "activities.json",
    "activity_face_results.json",
    "emotion_records.json",
    "security_test_records.json",
    "evaluation_records.json",
    "audit_logs.json",
]

APP_NAME = "Attendance Content Security System"
APP_VERSION = "0.3.1"
API_PREFIX = "/api/v1"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

<<<<<<< HEAD
HOST = "127.0.0.1"
=======
HOST = "0.0.0.0"
>>>>>>> 98bf8e49 (update)
PORT = 8000
DEBUG = True

SECRET_KEY = "replace-this-with-a-random-secret-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

ALLOWED_IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

# Face engine config
FACE_EMBEDDING_EXT = ".npy"
FACE_MATCH_THRESHOLD = 0.60
FACE_IMAGE_SIZE = 160
FACE_MARGIN = 20
FACE_MIN_SIZE = 40
<<<<<<< HEAD
LIVENESS_THRESHOLD = 0.50
=======
LIVENESS_THRESHOLD = 0.54
ANTI_SPOOF_MODEL_DIR = MODELS_DIR / "antispoof"
ANTI_SPOOF_ENABLED = True
ANTI_SPOOF_MODEL_NAME = "MiniFASNetV2"
ANTI_SPOOF_MODEL_PATH = ANTI_SPOOF_MODEL_DIR / "minifasnet_v2.onnx"
ANTI_SPOOF_THRESHOLD = 0.62
ANTI_SPOOF_UNCERTAIN_MARGIN = 0.05
ANTI_SPOOF_CROP_SCALE = 2.7
ANTI_SPOOF_FRAME_COUNT = 5
ANTI_SPOOF_FRAME_INTERVAL_MS = 220
ANTI_SPOOF_REAL_CLASS_INDEX = 1
ANTI_SPOOF_INPUT_COLOR = "rgb"
ANTI_SPOOF_INPUT_RANGE = "raw_255"
ANTI_SPOOF_SCORE_AGGREGATION = "mean"
ANTI_SPOOF_REAL_FRAME_RATIO = 0.60
ANTI_SPOOF_MODEL_WEIGHT = 0.80
ANTI_SPOOF_HEURISTIC_WEIGHT = 0.20
HEURISTIC_LIVENESS_THRESHOLD = 0.50
LIVENESS_DEFAULT_MODE = "passive_anti_spoof"
LIVENESS_CHALLENGE_OPTIONAL = True
LIVENESS_CHALLENGE_DEFAULT_ENABLED = False
EMOTION_MODEL_DIR = MODELS_DIR / "emotion"
EMOTION_MODEL_NAME = "dan_affectnet8"
EMOTION_DAN_CHECKPOINT = EMOTION_MODEL_DIR / "affecnet8_epoch5_acc0.6209.pth"
EMOTION_DAN_IMAGE_SIZE = 224
EMOTION_DAN_NUM_HEAD = 4
EMOTION_DAN_LABELS = [
    "neutral",
    "happy",
    "sad",
    "surprise",
    "fear",
    "disgust",
    "anger",
    "contempt",
]
EMOTION_FALLBACK_ENABLED = True
>>>>>>> 98bf8e49 (update)

MODEL_STATUS: Dict[str, str] = {
    "face_recognition": "not_initialized",
    "liveness_detection": "not_loaded",
    "emotion_recognition": "not_loaded",
}


def ensure_directories() -> None:
    required_dirs = [
        DATA_DIR,
        MODELS_DIR,
<<<<<<< HEAD
=======
        ANTI_SPOOF_MODEL_DIR,
        EMOTION_MODEL_DIR,
>>>>>>> 98bf8e49 (update)
        JSON_DIR,
        FACES_DIR,
        FEATURES_DIR,
        UPLOADS_DIR,
        ATTENDANCE_UPLOAD_DIR,
        GROUP_PHOTO_UPLOAD_DIR,
        ATTACK_SAMPLES_DIR,
        REPORTS_DIR,
        LOGS_DIR,
    ]
    for path in required_dirs:
        path.mkdir(parents=True, exist_ok=True)


def ensure_json_files() -> None:
    ensure_directories()
    for filename in DEFAULT_JSON_FILES:
        file_path = JSON_DIR / filename
        if not file_path.exists():
            file_path.write_text("[]", encoding="utf-8")
<<<<<<< HEAD


# Anti-spoofing model config
ANTI_SPOOF_ENABLED = True
ANTI_SPOOF_MODEL_NAME = "MiniFASNetV2"
ANTI_SPOOF_MODEL_PATH = MODELS_DIR / "anti_spoofing" / "MiniFASNetV2.onnx"
ANTI_SPOOF_THRESHOLD = 0.65
ANTI_SPOOF_CROP_SCALE = 2.7
=======
>>>>>>> 98bf8e49 (update)
