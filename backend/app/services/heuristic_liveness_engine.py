from __future__ import annotations

import math
from pathlib import Path
from typing import Any, Dict, Iterable, Sequence

import numpy as np
from PIL import Image

from app.core.config import HEURISTIC_LIVENESS_THRESHOLD
from app.core.exceptions import AppException


class HeuristicLivenessEngine:
    """
    Multi-frame heuristic liveness detector.

    It combines:
    - single-frame texture / sharpness / color clues
    - temporal movement between consecutive face crops
    - detection box motion across frames
    """

    def __init__(self) -> None:
        self._status: Dict[str, Any] = {
            "initialized": True,
            "mode": "multi_frame_heuristic",
            "threshold": HEURISTIC_LIVENESS_THRESHOLD,
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

    @staticmethod
    def _normalize(value: float, lower: float, upper: float) -> float:
        if upper <= lower:
            return 0.0
        return float(np.clip((value - lower) / (upper - lower), 0.0, 1.0))

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

        if temporal_texture_n < 0.12 and face_motion_n < 0.12 and temporal_brightness_n < 0.10:
            score *= 0.82

        score = float(np.clip(score, 0.0, 1.0))
        result = "real" if score >= HEURISTIC_LIVENESS_THRESHOLD else "fake"
        confidence = abs(score - HEURISTIC_LIVENESS_THRESHOLD) + 0.5
        confidence = float(np.clip(confidence, 0.5, 0.98))

        return {
            "result": result,
            "score": round(score, 6),
            "confidence": round(confidence, 6),
            "threshold": HEURISTIC_LIVENESS_THRESHOLD,
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
        return self.evaluate_sequence([image_path], [list(bbox)])


heuristic_liveness_engine = HeuristicLivenessEngine()
