from __future__ import annotations

import math
<<<<<<< HEAD
from pathlib import Path
from typing import Any, Dict, Iterable, Sequence

import numpy as np
from PIL import Image

from app.core.config import LIVENESS_THRESHOLD
from app.core.exceptions import AppException


class LivenessEngine:
    """
    Multi-frame heuristic liveness detector.

    It combines:
    - single-frame texture / sharpness / color clues
    - temporal movement between consecutive face crops
    - detection box motion across frames

    This is lighter than a dedicated anti-spoof model, but stronger than a
    single-frame rule engine and better aligned with the course requirement for
    "plan B" multi-frame liveness.
    """
=======
import random
import threading
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Sequence
from uuid import uuid4

import numpy as np

from app.core.config import (
    DATETIME_FORMAT,
    LIVENESS_CHALLENGE_DEFAULT_ENABLED,
    LIVENESS_DEFAULT_MODE,
    LIVENESS_THRESHOLD,
)
from app.core.exceptions import AppException
from app.services.model_liveness_engine import passive_liveness_engine


class LivenessEngine:
    _CHALLENGE_ACTIONS: dict[str, dict[str, str]] = {
        "turn_left": {
            "label": "向左转头",
            "prompt": "请先正视摄像头，然后向左转头，再回正。",
        },
        "turn_right": {
            "label": "向右转头",
            "prompt": "请先正视摄像头，然后向右转头，再回正。",
        },
        "nod_down": {
            "label": "低头",
            "prompt": "请先正视摄像头，然后低头，再回正。",
        },
    }
    _CHALLENGE_PURPOSES = {"attendance", "security_test"}
    _DEFAULT_BASELINE_FRAMES = 3
    _DEFAULT_ACTION_FRAMES = 6
    _DEFAULT_THRESHOLD = LIVENESS_THRESHOLD
    _DEFAULT_EXPIRE_SECONDS = 90
>>>>>>> 98bf8e49 (update)

    def __init__(self) -> None:
        self._status: Dict[str, Any] = {
            "initialized": True,
<<<<<<< HEAD
            "mode": "multi_frame_heuristic",
            "threshold": LIVENESS_THRESHOLD,
            "recommended_frames": 5,
            "last_error": None,
        }

    def get_status(self) -> Dict[str, Any]:
        return dict(self._status)

    @staticmethod
    def _read_image(image_path: Path) -> Image.Image:
        if not image_path.exists():
            raise AppException(message="图片文件不存在", code=4001, status_code=400)
        try:
            return Image.open(image_path).convert("RGB")
        except Exception as exc:
            raise AppException(
                message=f"活体检测图片读取失败: {exc}",
                code=5006,
                status_code=500,
            )

    @staticmethod
    def _clip_bbox(
        bbox: Sequence[float], width: int, height: int
    ) -> tuple[int, int, int, int]:
        x1, y1, x2, y2 = bbox
        pad_x = (x2 - x1) * 0.12
        pad_y = (y2 - y1) * 0.12
        left = max(0, int(x1 - pad_x))
        top = max(0, int(y1 - pad_y))
        right = min(width, int(x2 + pad_x))
        bottom = min(height, int(y2 + pad_y))
        if left >= right or top >= bottom:
            raise AppException(message="检测到的人脸区域无效", code=5007, status_code=500)
        return left, top, right, bottom
=======
            "mode": LIVENESS_DEFAULT_MODE,
            "threshold": self._DEFAULT_THRESHOLD,
            "recommended_frames": self._DEFAULT_BASELINE_FRAMES + self._DEFAULT_ACTION_FRAMES,
            "challenge_enabled": LIVENESS_CHALLENGE_DEFAULT_ENABLED,
            "last_error": None,
        }
        self._challenge_lock = threading.Lock()
        self._challenge_sessions: dict[str, Dict[str, Any]] = {}

    def get_status(self) -> Dict[str, Any]:
        passive_status = passive_liveness_engine.get_status()
        status = dict(self._status)
        status.update(
            {
                "initialized": bool(passive_status.get("initialized")),
                "mode": LIVENESS_DEFAULT_MODE,
                "passive_enabled": True,
                "passive_mode": passive_status.get("mode"),
                "passive_model_name": passive_status.get("model_name"),
                "passive_model_path": passive_status.get("model_path"),
                "passive_initialized": passive_status.get("initialized"),
                "passive_threshold": passive_status.get("threshold"),
                "passive_last_error": passive_status.get("last_error"),
            }
        )
        if not passive_status.get("initialized"):
            status["last_error"] = passive_status.get("last_error")
        return status

    @staticmethod
    def _now() -> datetime:
        return datetime.now()

    @staticmethod
    def _format_now(value: Optional[datetime] = None) -> str:
        return (value or datetime.now()).strftime(DATETIME_FORMAT)

    def _cleanup_challenges_locked(self, now: Optional[datetime] = None) -> None:
        now_ts = (now or self._now()).timestamp()
        expired = [
            challenge_id
            for challenge_id, session in self._challenge_sessions.items()
            if session["expires_at_ts"] <= now_ts
        ]
        for challenge_id in expired:
            self._challenge_sessions.pop(challenge_id, None)

    @staticmethod
    def _challenge_public_payload(session: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "challenge_id": session["challenge_id"],
            "purpose": session["purpose"],
            "challenge_action": session["challenge_action"],
            "challenge_action_label": session["challenge_action_label"],
            "challenge_prompt": session["challenge_prompt"],
            "baseline_frame_count": session["baseline_frame_count"],
            "action_frame_count": session["action_frame_count"],
            "recommended_frame_count": session["recommended_frame_count"],
            "threshold": session["threshold"],
            "created_at": session["created_at"],
            "expires_at": session["expires_at"],
            "operator_username": session.get("operator_username"),
            "operator_role": session.get("operator_role"),
        }

    def issue_challenge(
        self,
        *,
        purpose: str,
        operator_username: Optional[str] = None,
        operator_role: Optional[str] = None,
    ) -> Dict[str, Any]:
        if purpose not in self._CHALLENGE_PURPOSES:
            raise AppException(message="invalid challenge purpose", code=4228, status_code=422)

        now = self._now()
        challenge_id = uuid4().hex
        action = random.choice(list(self._CHALLENGE_ACTIONS.keys()))
        action_meta = self._CHALLENGE_ACTIONS[action]
        session = {
            "challenge_id": challenge_id,
            "purpose": purpose,
            "challenge_action": action,
            "challenge_action_label": action_meta["label"],
            "challenge_prompt": action_meta["prompt"],
            "baseline_frame_count": self._DEFAULT_BASELINE_FRAMES,
            "action_frame_count": self._DEFAULT_ACTION_FRAMES,
            "recommended_frame_count": self._DEFAULT_BASELINE_FRAMES + self._DEFAULT_ACTION_FRAMES,
            "threshold": self._DEFAULT_THRESHOLD,
            "created_at": self._format_now(now),
            "created_at_ts": now.timestamp(),
            "expires_at": self._format_now(now + timedelta(seconds=self._DEFAULT_EXPIRE_SECONDS)),
            "expires_at_ts": (now + timedelta(seconds=self._DEFAULT_EXPIRE_SECONDS)).timestamp(),
            "operator_username": operator_username,
            "operator_role": operator_role,
        }
        with self._challenge_lock:
            self._cleanup_challenges_locked(now)
            self._challenge_sessions[challenge_id] = session
        return self._challenge_public_payload(session)

    def _consume_challenge(
        self,
        challenge_id: str,
        *,
        purpose: Optional[str] = None,
        operator_username: Optional[str] = None,
    ) -> Dict[str, Any]:
        now = self._now()
        with self._challenge_lock:
            self._cleanup_challenges_locked(now)
            session = self._challenge_sessions.pop(challenge_id, None)
        if session is None:
            raise AppException(message="challenge does not exist or has expired", code=4401, status_code=422)
        if purpose and session["purpose"] != purpose:
            raise AppException(message="challenge purpose mismatch", code=4402, status_code=422)
        if (
            operator_username
            and session.get("operator_username")
            and session.get("operator_username") != operator_username
        ):
            raise AppException(message="challenge does not belong to current operator", code=4403, status_code=403)
        return session

    @staticmethod
    def _landmark_features(
        landmarks: Optional[Sequence[Sequence[float]]],
        bbox: Sequence[float],
    ) -> Optional[Dict[str, float]]:
        if not landmarks or len(landmarks) < 5:
            return None
        points = np.asarray(landmarks[:5], dtype=np.float32)
        left_eye, right_eye, nose, mouth_left, mouth_right = points
        eye_center = (left_eye + right_eye) / 2.0
        mouth_center = (mouth_left + mouth_right) / 2.0
        eye_distance = max(float(np.linalg.norm(right_eye - left_eye)), 1.0)
        face_width = max(float(bbox[2] - bbox[0]), 1.0)
        face_height = max(float(bbox[3] - bbox[1]), 1.0)
        return {
            "yaw_proxy": round(float((nose[0] - eye_center[0]) / eye_distance), 6),
            "pitch_proxy": round(float((nose[1] - eye_center[1]) / face_height), 6),
            "mouth_drop": round(float((mouth_center[1] - nose[1]) / face_height), 6),
            "face_width": round(face_width, 6),
            "face_height": round(face_height, 6),
            "eye_tilt": round(
                float(
                    math.degrees(
                        math.atan2(
                            float(right_eye[1] - left_eye[1]),
                            max(float(right_eye[0] - left_eye[0]), 1e-6),
                        )
                    )
                ),
                6,
            ),
        }

    @staticmethod
    def _frame_debug_payload(
        features: Sequence[Dict[str, float]],
        baseline_count: int,
    ) -> list[Dict[str, Any]]:
        return [
            {
                "index": index + 1,
                "phase": "baseline" if index < baseline_count else "action",
                "yaw_proxy": item.get("yaw_proxy"),
                "pitch_proxy": item.get("pitch_proxy"),
                "eye_tilt": item.get("eye_tilt"),
                "face_width": item.get("face_width"),
                "face_height": item.get("face_height"),
            }
            for index, item in enumerate(features)
        ]
>>>>>>> 98bf8e49 (update)

    @staticmethod
    def _normalize(value: float, lower: float, upper: float) -> float:
        if upper <= lower:
            return 0.0
        return float(np.clip((value - lower) / (upper - lower), 0.0, 1.0))

<<<<<<< HEAD
    @staticmethod
    def _laplacian_variance(gray: np.ndarray) -> float:
        padded = np.pad(gray, 1, mode="edge")
        laplacian = (
            padded[:-2, 1:-1]
            + padded[2:, 1:-1]
            + padded[1:-1, :-2]
            + padded[1:-1, 2:]
            - 4 * padded[1:-1, 1:-1]
        )
        return float(np.var(laplacian))

    @staticmethod
    def _entropy(gray: np.ndarray) -> float:
        hist, _ = np.histogram(gray, bins=32, range=(0.0, 1.0), density=False)
        total = float(np.sum(hist))
        if total <= 0:
            return 0.0
        hist = hist / total
        hist = hist[hist > 1e-9]
        return float(-np.sum(hist * np.log2(hist)))

    @staticmethod
    def _colorfulness(rgb: np.ndarray) -> float:
        rg = rgb[:, :, 0] - rgb[:, :, 1]
        yb = 0.5 * (rgb[:, :, 0] + rgb[:, :, 1]) - rgb[:, :, 2]
        std_root = math.sqrt(float(np.var(rg)) + float(np.var(yb)))
        mean_root = math.sqrt(float(np.mean(rg)) ** 2 + float(np.mean(yb)) ** 2)
        return std_root + 0.3 * mean_root

    @staticmethod
    def _edge_density(gray: np.ndarray) -> float:
        grad_x = np.abs(np.diff(gray, axis=1))
        grad_y = np.abs(np.diff(gray, axis=0))
        return float((np.mean(grad_x > 0.08) + np.mean(grad_y > 0.08)) / 2.0)

    @staticmethod
    def _highlight_penalty(gray: np.ndarray) -> float:
        return float(np.mean(gray > 0.95))

    @staticmethod
    def _saturation_mean(rgb: np.ndarray) -> float:
        maxc = np.max(rgb, axis=2)
        minc = np.min(rgb, axis=2)
        saturation = (maxc - minc) / np.clip(maxc, 1e-6, None)
        return float(np.mean(saturation))

    def _prepare_face_crop(
        self, image_path: Path, bbox: Sequence[float]
    ) -> tuple[np.ndarray, np.ndarray]:
        image = self._read_image(image_path)
        left, top, right, bottom = self._clip_bbox(bbox, image.width, image.height)
        face = image.crop((left, top, right, bottom)).resize((160, 160))
        rgb = np.asarray(face, dtype=np.float32) / 255.0
        gray = (
            0.299 * rgb[:, :, 0] + 0.587 * rgb[:, :, 1] + 0.114 * rgb[:, :, 2]
        ).astype(np.float32)
        return rgb, gray

    def _frame_metrics(
        self, image_path: Path, bbox: Sequence[float]
    ) -> Dict[str, Any]:
        rgb, gray = self._prepare_face_crop(image_path, bbox)

        sharpness = self._laplacian_variance(gray)
        contrast = float(np.std(gray))
        entropy = self._entropy(gray)
        colorfulness = self._colorfulness(rgb)
        edge_density = self._edge_density(gray)
        highlight_penalty = self._highlight_penalty(gray)
        saturation = self._saturation_mean(rgb)

        sharpness_n = self._normalize(sharpness, 0.0015, 0.02)
        contrast_n = self._normalize(contrast, 0.08, 0.22)
        entropy_n = self._normalize(entropy, 1.5, 4.5)
        colorfulness_n = self._normalize(colorfulness, 0.05, 0.4)
        edge_density_n = self._normalize(edge_density, 0.03, 0.20)
        saturation_n = self._normalize(saturation, 0.10, 0.45)
        highlight_n = 1.0 - self._normalize(highlight_penalty, 0.02, 0.25)

        static_score = (
            sharpness_n * 0.28
            + contrast_n * 0.16
            + entropy_n * 0.18
            + colorfulness_n * 0.12
            + edge_density_n * 0.10
            + saturation_n * 0.08
            + highlight_n * 0.08
        )
        static_score = float(np.clip(static_score, 0.0, 1.0))

        return {
            "rgb": rgb,
            "gray": gray,
            "static_score": static_score,
            "features": {
                "sharpness": round(sharpness, 6),
                "contrast": round(contrast, 6),
                "entropy": round(entropy, 6),
                "colorfulness": round(colorfulness, 6),
                "edge_density": round(edge_density, 6),
                "saturation": round(saturation, 6),
                "highlight_penalty": round(highlight_penalty, 6),
            },
        }

    @staticmethod
    def _bbox_center_and_size(bbox: Sequence[float]) -> tuple[float, float, float]:
        x1, y1, x2, y2 = bbox
        width = max(x2 - x1, 1.0)
        height = max(y2 - y1, 1.0)
        center_x = (x1 + x2) / 2.0
        center_y = (y1 + y2) / 2.0
        size = math.sqrt(width * height)
        return center_x, center_y, size

    def evaluate_sequence(
        self,
        image_paths: Sequence[Path],
        bboxes: Sequence[Sequence[float]],
    ) -> Dict[str, Any]:
        if not image_paths or not bboxes or len(image_paths) != len(bboxes):
            raise AppException(message="活体检测帧序列无效", code=4224, status_code=422)

        frame_metrics = [
            self._frame_metrics(image_path, bbox)
            for image_path, bbox in zip(image_paths, bboxes)
        ]

        static_scores = [item["static_score"] for item in frame_metrics]
        static_score = float(np.mean(static_scores))

        crop_diffs: list[float] = []
        brightness_diffs: list[float] = []
        centers_x: list[float] = []
        centers_y: list[float] = []
        sizes: list[float] = []
        edge_density_values = [item["features"]["edge_density"] for item in frame_metrics]

        for bbox in bboxes:
            cx, cy, size = self._bbox_center_and_size(bbox)
            centers_x.append(cx)
            centers_y.append(cy)
            sizes.append(size)

        for prev_item, curr_item in zip(frame_metrics[:-1], frame_metrics[1:]):
            prev_gray = prev_item["gray"]
            curr_gray = curr_item["gray"]
            crop_diffs.append(float(np.mean(np.abs(curr_gray - prev_gray))))
            brightness_diffs.append(
                float(abs(np.mean(curr_gray) - np.mean(prev_gray)))
            )

        motion_values: list[float] = []
        scale_values: list[float] = []
        for prev_bbox, curr_bbox in zip(bboxes[:-1], bboxes[1:]):
            prev_cx, prev_cy, prev_size = self._bbox_center_and_size(prev_bbox)
            curr_cx, curr_cy, curr_size = self._bbox_center_and_size(curr_bbox)
            center_shift = math.sqrt((curr_cx - prev_cx) ** 2 + (curr_cy - prev_cy) ** 2)
            motion_values.append(center_shift / max((prev_size + curr_size) / 2.0, 1.0))
            scale_values.append(abs(curr_size - prev_size) / max(prev_size, 1.0))

        temporal_texture = float(np.mean(crop_diffs)) if crop_diffs else 0.0
        temporal_brightness = float(np.mean(brightness_diffs)) if brightness_diffs else 0.0
        face_motion = float(np.mean(motion_values)) if motion_values else 0.0
        face_scale_change = float(np.mean(scale_values)) if scale_values else 0.0
        edge_variation = float(np.std(edge_density_values)) if edge_density_values else 0.0

        temporal_texture_n = self._normalize(temporal_texture, 0.004, 0.030)
        temporal_brightness_n = self._normalize(temporal_brightness, 0.002, 0.020)
        face_motion_n = self._normalize(face_motion, 0.003, 0.030)
        face_scale_change_n = self._normalize(face_scale_change, 0.002, 0.030)
        edge_variation_n = self._normalize(edge_variation, 0.0005, 0.010)

        score = (
            static_score * 0.44
            + temporal_texture_n * 0.18
            + temporal_brightness_n * 0.14
            + face_motion_n * 0.14
            + face_scale_change_n * 0.05
            + edge_variation_n * 0.05
        )

        # A very static sequence should be penalized even if single-frame quality is high.
        if temporal_texture_n < 0.12 and face_motion_n < 0.12 and temporal_brightness_n < 0.10:
            score *= 0.82

        score = float(np.clip(score, 0.0, 1.0))
        result = "real" if score >= LIVENESS_THRESHOLD else "fake"
        confidence = abs(score - LIVENESS_THRESHOLD) + 0.5
        confidence = float(np.clip(confidence, 0.5, 0.98))

=======
    def _evaluate_random_challenge(
        self,
        session: Dict[str, Any],
        frame_features: Sequence[Dict[str, float]],
    ) -> Dict[str, Any]:
        baseline_count = max(1, int(session.get("baseline_frame_count", self._DEFAULT_BASELINE_FRAMES)))
        threshold = float(session.get("threshold", self._DEFAULT_THRESHOLD))

        if len(frame_features) < baseline_count + 2:
            return {
                "result": "uncertain",
                "score": None,
                "confidence": 0.5,
                "threshold": threshold,
                "action": session["challenge_action"],
                "action_label": session["challenge_action_label"],
                "prompt": session["challenge_prompt"],
                "reason": "动作采样帧数不足，请重试",
                "accepted_frame_count": len(frame_features),
                "rejected_frame_count": 0,
                "quality_insufficient": True,
                "frame_debug": self._frame_debug_payload(frame_features, baseline_count),
            }

        baseline = frame_features[:baseline_count]
        action = frame_features[baseline_count:]
        baseline_yaw = np.asarray([item["yaw_proxy"] for item in baseline], dtype=np.float32)
        baseline_pitch = np.asarray([item["pitch_proxy"] for item in baseline], dtype=np.float32)
        baseline_eye_tilt = np.asarray([item["eye_tilt"] for item in baseline], dtype=np.float32)
        baseline_width = np.asarray([item["face_width"] for item in baseline], dtype=np.float32)
        baseline_height = np.asarray([item["face_height"] for item in baseline], dtype=np.float32)

        baseline_stability = float(
            np.std(baseline_yaw) * 2.0
            + np.std(baseline_pitch) * 1.8
            + np.std(baseline_eye_tilt) / 18.0
            + np.std(baseline_width) / max(float(np.mean(baseline_width)), 1.0)
            + np.std(baseline_height) / max(float(np.mean(baseline_height)), 1.0)
        )
        if baseline_stability > 0.50:
            return {
                "result": "uncertain",
                "score": None,
                "confidence": 0.5,
                "threshold": threshold,
                "action": session["challenge_action"],
                "action_label": session["challenge_action_label"],
                "prompt": session["challenge_prompt"],
                "reason": "基线画面不够稳定，请正视摄像头后重试",
                "accepted_frame_count": len(frame_features),
                "rejected_frame_count": 0,
                "quality_insufficient": True,
                "frame_debug": self._frame_debug_payload(frame_features, baseline_count),
            }

        baseline_yaw_value = float(np.median(baseline_yaw))
        baseline_pitch_value = float(np.median(baseline_pitch))
        action_yaw = np.asarray([item["yaw_proxy"] for item in action], dtype=np.float32)
        action_pitch = np.asarray([item["pitch_proxy"] for item in action], dtype=np.float32)

        action_name = str(session["challenge_action"])
        if action_name == "turn_left":
            deltas = baseline_yaw_value - action_yaw
            min_peak = 0.016
            min_return = 0.30
            reason_text = "请向左转头并回正"
        elif action_name == "turn_right":
            deltas = action_yaw - baseline_yaw_value
            min_peak = 0.016
            min_return = 0.30
            reason_text = "请向右转头并回正"
        elif action_name == "nod_down":
            deltas = action_pitch - baseline_pitch_value
            min_peak = 0.014
            min_return = 0.26
            reason_text = "请低头并回正"
        else:
            raise AppException(message="unknown challenge action", code=4231, status_code=422)

        peak = float(np.max(deltas)) if len(deltas) else 0.0
        tail = float(deltas[-1]) if len(deltas) else 0.0
        positive_threshold = max(0.004, peak * 0.30)
        direction_ratio = float(np.mean(deltas > positive_threshold)) if len(deltas) else 0.0
        return_ratio = 1.0 - min(abs(tail) / max(peak, 1e-6), 1.0)
        motion_variation = float(np.std(deltas)) if len(deltas) > 1 else 0.0

        if peak < min_peak * 0.65 or direction_ratio < 0.25:
            return {
                "result": "uncertain",
                "score": None,
                "confidence": 0.5,
                "threshold": threshold,
                "action": action_name,
                "action_label": session["challenge_action_label"],
                "prompt": session["challenge_prompt"],
                "reason": f"动作幅度不足，{reason_text}",
                "accepted_frame_count": len(frame_features),
                "rejected_frame_count": 0,
                "quality_insufficient": False,
                "frame_debug": self._frame_debug_payload(frame_features, baseline_count),
            }

        peak_score = self._normalize(peak, min_peak, min_peak * 4.5)
        direction_score = self._normalize(direction_ratio, 0.35, 0.90)
        return_score = self._normalize(return_ratio, 0.20, 0.95)
        stability_score = 1.0 - self._normalize(baseline_stability, 0.10, 0.45)
        motion_bonus = self._normalize(motion_variation, 0.002, 0.030) * 0.08
        score = float(
            np.clip(
                peak_score * 0.46
                + direction_score * 0.24
                + return_score * 0.22
                + stability_score * 0.08
                + motion_bonus,
                0.0,
                1.0,
            )
        )

        if score >= threshold and peak >= min_peak and direction_ratio >= 0.45 and return_ratio >= min_return:
            result = "real"
            reason = "随机动作挑战通过"
        elif score >= threshold - 0.07:
            result = "uncertain"
            reason = "动作接近阈值，请重试"
        else:
            result = "fake"
            reason = f"随机动作挑战未通过，{reason_text}"

        confidence = float(np.clip(0.55 + abs(score - threshold) + (0.05 if result == "real" else 0.0), 0.5, 0.98))
>>>>>>> 98bf8e49 (update)
        return {
            "result": result,
            "score": round(score, 6),
            "confidence": round(confidence, 6),
<<<<<<< HEAD
            "threshold": LIVENESS_THRESHOLD,
            "mode": self._status["mode"],
            "frame_count": len(image_paths),
            "static_score": round(static_score, 6),
            "temporal": {
                "texture_diff": round(temporal_texture, 6),
                "brightness_diff": round(temporal_brightness, 6),
                "face_motion": round(face_motion, 6),
                "face_scale_change": round(face_scale_change, 6),
                "edge_variation": round(edge_variation, 6),
            },
            "frame_features": [item["features"] for item in frame_metrics],
        }

    def evaluate(
        self, image_path: Path, bbox: Iterable[float]
    ) -> Dict[str, Any]:
=======
            "threshold": threshold,
            "action": action_name,
            "action_label": session["challenge_action_label"],
            "prompt": session["challenge_prompt"],
            "reason": reason,
            "accepted_frame_count": len(frame_features),
            "rejected_frame_count": 0,
            "quality_insufficient": False,
            "frame_debug": self._frame_debug_payload(frame_features, baseline_count),
        }

    def _evaluate_challenge_sequence(
        self,
        image_paths: Sequence[Any],
        bboxes: Sequence[Sequence[float]],
        landmarks: Optional[Sequence[Sequence[Sequence[float]]]] = None,
        *,
        challenge_id: Optional[str],
        purpose: Optional[str],
        operator_username: Optional[str],
    ) -> Dict[str, Any]:
        if not challenge_id:
            raise AppException(message="challenge_id is required for random action verification", code=4232, status_code=422)
        if landmarks is None:
            raise AppException(message="landmarks are required for random action verification", code=4224, status_code=422)

        features: list[Dict[str, float]] = []
        for bbox, frame_landmarks in zip(bboxes, landmarks):
            item = self._landmark_features(frame_landmarks, bbox)
            if item is None:
                raise AppException(
                    message="stable face landmarks are required for random action verification",
                    code=4224,
                    status_code=422,
                )
            features.append(item)

        challenge_session = self._consume_challenge(
            challenge_id,
            purpose=purpose,
            operator_username=operator_username,
        )
        challenge_eval = self._evaluate_random_challenge(challenge_session, features)
        return {
            "result": challenge_eval["result"],
            "decision": "allow" if challenge_eval["result"] == "real" else ("retry" if challenge_eval["result"] == "uncertain" else "block"),
            "reason": challenge_eval["reason"],
            "score": round(float(challenge_eval["score"] or 0.0), 6),
            "confidence": round(float(challenge_eval["confidence"]), 6),
            "threshold": challenge_eval["threshold"],
            "mode": "random_action_challenge",
            "verification_mode": "random_action_challenge",
            "frame_count": len(image_paths),
            "accepted_frame_count": challenge_eval.get("accepted_frame_count", len(features)),
            "rejected_frame_count": challenge_eval.get("rejected_frame_count", 0),
            "quality_insufficient": challenge_eval.get("quality_insufficient", False),
            "challenge_required": False,
            "challenge_used": True,
            "attack_suspected": challenge_eval["result"] == "fake",
            "frame_features": [],
            "risk_indicators": [],
            "frame_debug": challenge_eval.get("frame_debug", []),
            "challenge_id": challenge_id,
            "challenge_action": challenge_eval["action"],
            "challenge_action_label": challenge_eval["action_label"],
            "challenge_prompt": challenge_eval["prompt"],
            "challenge_result": "passed" if challenge_eval["result"] == "real" else ("failed" if challenge_eval["result"] == "fake" else "uncertain"),
            "challenge_score": challenge_eval["score"],
            "challenge_confidence": challenge_eval["confidence"],
            "challenge_threshold": challenge_eval["threshold"],
            "challenge_reason": challenge_eval["reason"],
            "challenge_details": challenge_session,
        }

    @staticmethod
    def _combine_passive_and_challenge(
        passive_eval: Dict[str, Any],
        challenge_eval: Dict[str, Any],
    ) -> Dict[str, Any]:
        passive_result = passive_eval["result"]
        challenge_result = challenge_eval["result"]

        if passive_result == "fake" or challenge_result == "fake":
            final_result = "fake"
            final_reason = passive_eval["reason"] if passive_result == "fake" else challenge_eval["reason"]
        elif passive_result == "uncertain" or challenge_result == "uncertain":
            final_result = "uncertain"
            final_reason = passive_eval["reason"] if passive_result == "uncertain" else challenge_eval["reason"]
        else:
            final_result = "real"
            final_reason = "被动活体与随机动作双重校验通过"

        score_candidates = [float(passive_eval.get("score", 0.0))]
        if challenge_eval.get("challenge_score") is not None:
            score_candidates.append(float(challenge_eval["challenge_score"]))
        final_score = round(float(np.mean(score_candidates)), 6)

        threshold_candidates = [float(passive_eval.get("threshold", 0.0))]
        if challenge_eval.get("challenge_threshold") is not None:
            threshold_candidates.append(float(challenge_eval["challenge_threshold"]))
        final_threshold = round(float(np.mean(threshold_candidates)), 6)

        confidence = round(
            float(
                min(
                    float(passive_eval.get("confidence", 0.5)),
                    float(challenge_eval.get("confidence", 0.5)),
                )
            ),
            6,
        )

        return {
            "result": final_result,
            "decision": "allow" if final_result == "real" else ("retry" if final_result == "uncertain" else "block"),
            "reason": final_reason,
            "score": final_score,
            "confidence": confidence,
            "threshold": final_threshold,
            "mode": LIVENESS_DEFAULT_MODE,
            "verification_mode": "passive_plus_challenge",
            "frame_count": passive_eval.get("frame_count"),
            "accepted_frame_count": min(
                int(passive_eval.get("accepted_frame_count", 0)),
                int(challenge_eval.get("accepted_frame_count", 0)),
            ),
            "rejected_frame_count": int(passive_eval.get("rejected_frame_count", 0)) + int(challenge_eval.get("rejected_frame_count", 0)),
            "quality_insufficient": bool(passive_eval.get("quality_insufficient")) or bool(challenge_eval.get("quality_insufficient")),
            "passive_result": passive_eval.get("passive_result", passive_result),
            "passive_score": passive_eval.get("passive_score", passive_eval.get("score")),
            "passive_confidence": passive_eval.get("passive_confidence", passive_eval.get("confidence")),
            "passive_threshold": passive_eval.get("passive_threshold", passive_eval.get("threshold")),
            "passive_reason": passive_eval.get("passive_reason", passive_eval.get("reason")),
            "passive_attack_type": passive_eval.get("passive_attack_type"),
            "spoof_result": passive_eval.get("spoof_result", passive_result),
            "spoof_score": passive_eval.get("spoof_score", passive_eval.get("score")),
            "spoof_confidence": passive_eval.get("spoof_confidence", passive_eval.get("confidence")),
            "spoof_attack_type": passive_eval.get("spoof_attack_type"),
            "spoof_model_name": passive_eval.get("spoof_model_name"),
            "spoof_reason": passive_eval.get("spoof_reason", passive_eval.get("reason")),
            "spoof_real_threshold": passive_eval.get("spoof_real_threshold"),
            "spoof_fake_threshold": passive_eval.get("spoof_fake_threshold"),
            "challenge_required": False,
            "challenge_used": True,
            "attack_suspected": final_result == "fake",
            "frame_features": passive_eval.get("frame_features", []),
            "risk_indicators": passive_eval.get("risk_indicators", []),
            "frame_debug": passive_eval.get("frame_debug", []),
            "challenge_frame_debug": challenge_eval.get("frame_debug", []),
            "challenge_id": challenge_eval.get("challenge_id"),
            "challenge_action": challenge_eval.get("challenge_action"),
            "challenge_action_label": challenge_eval.get("challenge_action_label"),
            "challenge_prompt": challenge_eval.get("challenge_prompt"),
            "challenge_result": challenge_eval.get("challenge_result"),
            "challenge_score": challenge_eval.get("challenge_score"),
            "challenge_confidence": challenge_eval.get("challenge_confidence"),
            "challenge_threshold": challenge_eval.get("challenge_threshold"),
            "challenge_reason": challenge_eval.get("challenge_reason"),
            "challenge_details": challenge_eval.get("challenge_details"),
        }

    def evaluate_sequence(
        self,
        image_paths: Sequence[Any],
        bboxes: Sequence[Sequence[float]],
        landmarks: Optional[Sequence[Sequence[Sequence[float]]]] = None,
        *,
        challenge_id: Optional[str] = None,
        purpose: Optional[str] = None,
        operator_username: Optional[str] = None,
    ) -> Dict[str, Any]:
        if not image_paths or not bboxes or len(image_paths) != len(bboxes):
            raise AppException(message="invalid liveness frame sequence", code=4224, status_code=422)
        if landmarks is not None and len(landmarks) != len(image_paths):
            raise AppException(message="invalid liveness landmark sequence", code=4224, status_code=422)

        passive_eval = passive_liveness_engine.evaluate_sequence(image_paths, bboxes)
        if not challenge_id:
            return passive_eval

        challenge_eval = self._evaluate_challenge_sequence(
            image_paths,
            bboxes,
            landmarks,
            challenge_id=challenge_id,
            purpose=purpose,
            operator_username=operator_username,
        )
        return self._combine_passive_and_challenge(passive_eval, challenge_eval)

    def evaluate(self, image_path: Any, bbox: Sequence[float]) -> Dict[str, Any]:
>>>>>>> 98bf8e49 (update)
        return self.evaluate_sequence([image_path], [list(bbox)])


liveness_engine = LivenessEngine()
