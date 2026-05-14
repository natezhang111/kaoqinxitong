from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, Sequence

<<<<<<< HEAD
import cv2
import numpy as np
import onnxruntime as ort
=======
import numpy as np
from PIL import Image
>>>>>>> 98bf8e49 (update)

from app.core.config import (
    ANTI_SPOOF_CROP_SCALE,
    ANTI_SPOOF_ENABLED,
<<<<<<< HEAD
    ANTI_SPOOF_MODEL_NAME,
    ANTI_SPOOF_MODEL_PATH,
    ANTI_SPOOF_THRESHOLD,
)
from app.services.liveness_engine import LivenessEngine


class ModelLivenessEngine:
    def __init__(self) -> None:
        self.model_path = Path(ANTI_SPOOF_MODEL_PATH)
        self.threshold = float(ANTI_SPOOF_THRESHOLD)
        self.crop_scale = float(ANTI_SPOOF_CROP_SCALE)
        self.heuristic_engine = LivenessEngine()

        self.session = None
        self.input_name = None
        self.output_name = None
        self.input_size = (80, 80)

        self._status: Dict[str, Any] = {
            "initialized": False,
            "enabled": bool(ANTI_SPOOF_ENABLED),
            "mode": f"{ANTI_SPOOF_MODEL_NAME}_onnx",
            "model_path": str(self.model_path),
            "threshold": self.threshold,
            "crop_scale": self.crop_scale,
            "last_error": None,
        }

        if ANTI_SPOOF_ENABLED:
            self._load_model()

    def _load_model(self) -> None:
        if not self.model_path.exists():
            self._status["last_error"] = f"Anti-spoofing model not found: {self.model_path}"
            return

        try:
            self.session = ort.InferenceSession(
                str(self.model_path),
                providers=["CPUExecutionProvider"],
            )
            input_cfg = self.session.get_inputs()[0]
            output_cfg = self.session.get_outputs()[0]

            self.input_name = input_cfg.name
            self.output_name = output_cfg.name

            shape = input_cfg.shape
            if len(shape) == 4:
                h = shape[2] if isinstance(shape[2], int) else 80
                w = shape[3] if isinstance(shape[3], int) else 80
                self.input_size = (int(h), int(w))

            self._status["initialized"] = True
            self._status["input_name"] = self.input_name
            self._status["output_name"] = self.output_name
            self._status["input_size"] = self.input_size

        except Exception as exc:
            self._status["initialized"] = False
            self._status["last_error"] = str(exc)

    def get_status(self) -> Dict[str, Any]:
        return dict(self._status)

    @staticmethod
    def _read_bgr_image(image_path: Path) -> np.ndarray:
        image_path = Path(image_path)
        if not image_path.exists():
            raise FileNotFoundError(f"Image file not found: {image_path}")

        data = np.fromfile(str(image_path), dtype=np.uint8)
        image = cv2.imdecode(data, cv2.IMREAD_COLOR)

        if image is None:
            raise RuntimeError(f"Failed to read image: {image_path}")

        return image

    @staticmethod
=======
    ANTI_SPOOF_FRAME_COUNT,
    ANTI_SPOOF_HEURISTIC_WEIGHT,
    ANTI_SPOOF_INPUT_COLOR,
    ANTI_SPOOF_INPUT_RANGE,
    ANTI_SPOOF_MODEL_NAME,
    ANTI_SPOOF_MODEL_PATH,
    ANTI_SPOOF_MODEL_WEIGHT,
    ANTI_SPOOF_REAL_CLASS_INDEX,
    ANTI_SPOOF_REAL_FRAME_RATIO,
    ANTI_SPOOF_SCORE_AGGREGATION,
    ANTI_SPOOF_THRESHOLD,
    ANTI_SPOOF_UNCERTAIN_MARGIN,
)
from app.core.exceptions import AppException
from app.services.heuristic_liveness_engine import heuristic_liveness_engine

try:
    import onnxruntime as ort
except Exception as exc:  # pragma: no cover
    ort = None
    _onnx_import_error = exc
else:
    _onnx_import_error = None


class PassiveLivenessEngine:
    def __init__(self) -> None:
        self._session = None
        self._input_name = None
        self._output_name = None
        self._input_size = (80, 80)
        self._status: Dict[str, Any] = {
            "initialized": False,
            "mode": "passive_anti_spoof_fused",
            "model_name": ANTI_SPOOF_MODEL_NAME,
            "model_path": str(ANTI_SPOOF_MODEL_PATH),
            "model_exists": ANTI_SPOOF_MODEL_PATH.exists(),
            "threshold": ANTI_SPOOF_THRESHOLD,
            "uncertain_margin": ANTI_SPOOF_UNCERTAIN_MARGIN,
            "crop_scale": ANTI_SPOOF_CROP_SCALE,
            "recommended_frames": ANTI_SPOOF_FRAME_COUNT,
            "providers": [],
            "real_class_index": ANTI_SPOOF_REAL_CLASS_INDEX,
            "input_color": ANTI_SPOOF_INPUT_COLOR,
            "input_range": ANTI_SPOOF_INPUT_RANGE,
            "aggregation": ANTI_SPOOF_SCORE_AGGREGATION,
            "model_weight": ANTI_SPOOF_MODEL_WEIGHT,
            "heuristic_weight": ANTI_SPOOF_HEURISTIC_WEIGHT,
            "last_error": None,
        }

    def get_status(self) -> Dict[str, Any]:
        self._status["model_exists"] = ANTI_SPOOF_MODEL_PATH.exists()
        if self._session is None and ANTI_SPOOF_ENABLED:
            try:
                self._ensure_session()
            except AppException:
                pass
        return dict(self._status)

    @staticmethod
>>>>>>> 98bf8e49 (update)
    def _softmax(logits: np.ndarray) -> np.ndarray:
        logits = np.asarray(logits, dtype=np.float32)
        if logits.ndim == 1:
            logits = logits[None, :]
        logits = logits - np.max(logits, axis=1, keepdims=True)
        exp = np.exp(logits)
<<<<<<< HEAD
        return exp / np.sum(exp, axis=1, keepdims=True)

    def _xyxy_to_xywh(self, bbox_xyxy: Sequence[float]) -> list[int]:
        x1, y1, x2, y2 = [float(v) for v in bbox_xyxy]
        return [
            int(x1),
            int(y1),
            int(max(x2 - x1, 1.0)),
            int(max(y2 - y1, 1.0)),
        ]

    def _crop_face(self, image: np.ndarray, bbox_xywh: Sequence[int]) -> np.ndarray:
        src_h, src_w = image.shape[:2]
        x, y, box_w, box_h = [int(v) for v in bbox_xywh]

        box_w = max(box_w, 1)
        box_h = max(box_h, 1)

        scale = min(
            (src_h - 1) / box_h,
            (src_w - 1) / box_w,
            self.crop_scale,
        )

        new_w = box_w * scale
        new_h = box_h * scale
        center_x = x + box_w / 2.0
        center_y = y + box_h / 2.0

        x1 = max(0, int(center_x - new_w / 2.0))
        y1 = max(0, int(center_y - new_h / 2.0))
        x2 = min(src_w - 1, int(center_x + new_w / 2.0))
        y2 = min(src_h - 1, int(center_y + new_h / 2.0))

        if x1 >= x2 or y1 >= y2:
            raise RuntimeError("Invalid anti-spoofing face crop area")

        cropped = image[y1 : y2 + 1, x1 : x2 + 1]
        return cv2.resize(cropped, self.input_size[::-1])

    def _preprocess(self, image: np.ndarray, bbox_xyxy: Sequence[float]) -> np.ndarray:
        bbox_xywh = self._xyxy_to_xywh(bbox_xyxy)
        face = self._crop_face(image, bbox_xywh)

        face = face.astype(np.float32)
        face = np.transpose(face, (2, 0, 1))
        face = np.expand_dims(face, axis=0)

        return face

    def predict_frame(self, image_path: Path, bbox: Sequence[float]) -> Dict[str, Any]:
        if not ANTI_SPOOF_ENABLED:
            return {
                "label": "uncertain",
                "real_score": 0.5,
                "fake_score": 0.5,
                "raw_probs": [],
            }

        if self.session is None or not self._status.get("initialized"):
            raise RuntimeError(f"Anti-spoofing model is not initialized: {self._status.get('last_error')}")

        image = self._read_bgr_image(Path(image_path))
        input_tensor = self._preprocess(image, bbox)

        outputs = self.session.run(
            [self.output_name],
            {self.input_name: input_tensor},
        )

        probs = self._softmax(outputs[0])
        label_idx = int(np.argmax(probs, axis=1)[0])

        # MiniFASNet convention: class index 1 = real face, others = fake.
        real_idx = 1 if probs.shape[1] > 1 else 0

        real_score = float(probs[0, real_idx])
        fake_score = float(1.0 - real_score)

        label = "real" if label_idx == real_idx else "fake"

=======
        return exp / np.clip(np.sum(exp, axis=1, keepdims=True), 1e-8, None)

    @staticmethod
    def _read_rgb_image(image_path: Path) -> np.ndarray:
        if not image_path.exists():
            raise AppException(message=f"图像文件不存在: {image_path}", code=4001, status_code=400)
        try:
            return np.asarray(Image.open(image_path).convert("RGB"), dtype=np.uint8)
        except Exception as exc:
            raise AppException(message=f"读取反欺诈图像失败: {exc}", code=5006, status_code=500)

    @staticmethod
    def _scaled_square_crop(
        image_rgb: np.ndarray,
        bbox_xyxy: Sequence[float],
        scale: float,
    ) -> np.ndarray:
        height, width = image_rgb.shape[:2]
        x1, y1, x2, y2 = [float(value) for value in bbox_xyxy]
        face_width = max(x2 - x1, 1.0)
        face_height = max(y2 - y1, 1.0)
        center_x = (x1 + x2) / 2.0
        center_y = (y1 + y2) / 2.0
        side = max(face_width, face_height) * scale
        half = side / 2.0

        left = max(0, int(round(center_x - half)))
        top = max(0, int(round(center_y - half)))
        right = min(width, int(round(center_x + half)))
        bottom = min(height, int(round(center_y + half)))
        if right <= left or bottom <= top:
            raise AppException(message="反欺诈裁剪区域无效", code=5007, status_code=500)
        return image_rgb[top:bottom, left:right]

    def _ensure_session(self) -> None:
        if self._session is not None:
            return
        if not ANTI_SPOOF_ENABLED:
            self._status.update(
                {
                    "initialized": False,
                    "last_error": "anti spoof disabled by config",
                }
            )
            raise AppException(message="反欺诈模型已在配置中禁用", code=5010, status_code=500)
        if ort is None:
            self._status.update(
                {
                    "initialized": False,
                    "last_error": f"onnxruntime import failed: {_onnx_import_error}",
                }
            )
            raise AppException(message=f"导入 onnxruntime 失败: {_onnx_import_error}", code=5010, status_code=500)
        if not ANTI_SPOOF_MODEL_PATH.exists():
            self._status.update(
                {
                    "initialized": False,
                    "model_exists": False,
                    "last_error": f"model does not exist: {ANTI_SPOOF_MODEL_PATH}",
                }
            )
            raise AppException(message=f"反欺诈模型不存在: {ANTI_SPOOF_MODEL_PATH}", code=5010, status_code=500)
        try:
            session = ort.InferenceSession(str(ANTI_SPOOF_MODEL_PATH), providers=["CPUExecutionProvider"])
            input_meta = session.get_inputs()[0]
            output_meta = session.get_outputs()[0]
            input_shape = input_meta.shape
            self._input_size = (
                int(input_shape[3]) if len(input_shape) >= 4 and input_shape[3] else 80,
                int(input_shape[2]) if len(input_shape) >= 4 and input_shape[2] else 80,
            )
            self._session = session
            self._input_name = input_meta.name
            self._output_name = output_meta.name
            self._status.update(
                {
                    "initialized": True,
                    "model_exists": True,
                    "providers": list(session.get_providers()),
                    "last_error": None,
                    "input_name": self._input_name,
                    "output_name": self._output_name,
                    "input_size": {
                        "width": self._input_size[0],
                        "height": self._input_size[1],
                    },
                }
            )
        except Exception as exc:
            self._status.update(
                {
                    "initialized": False,
                    "last_error": str(exc),
                }
            )
            raise AppException(message=f"加载反欺诈模型失败: {exc}", code=5010, status_code=500)

    def _preprocess(self, image_path: Path, bbox: Sequence[float]) -> np.ndarray:
        rgb = self._read_rgb_image(image_path)
        crop = self._scaled_square_crop(rgb, bbox, ANTI_SPOOF_CROP_SCALE)
        resized = np.asarray(
            Image.fromarray(crop).resize(self._input_size, Image.BILINEAR),
            dtype=np.float32,
        )

        if ANTI_SPOOF_INPUT_COLOR.lower() == "bgr":
            resized = resized[:, :, ::-1]
        if ANTI_SPOOF_INPUT_RANGE.lower() == "norm_1":
            resized = resized / 255.0

        chw = np.transpose(resized, (2, 0, 1))
        return np.expand_dims(chw, axis=0).astype(np.float32)

    def predict_frame(self, image_path: Path, bbox: Sequence[float]) -> Dict[str, Any]:
        self._ensure_session()
        outputs = self._session.run(
            [self._output_name],
            {self._input_name: self._preprocess(image_path, bbox)},
        )
        probs = self._softmax(np.asarray(outputs[0], dtype=np.float32))
        real_idx = int(ANTI_SPOOF_REAL_CLASS_INDEX)
        real_score = float(probs[0, real_idx])
        fake_scores = [float(value) for idx, value in enumerate(probs[0].tolist()) if idx != real_idx]
        fake_score = float(sum(fake_scores))
        label_idx = int(np.argmax(probs, axis=1)[0])
        label = "real" if label_idx == real_idx else "fake"

        attack_type = "print_attack"
        print_score = 0.0
        replay_score = 0.0
        if probs.shape[1] >= 3:
            # For the current downloaded checkpoint, class-0 behaves like print/photo,
            # class-2 behaves like replay/screen on our validation sample.
            print_index = 0 if real_idx != 0 else 2
            replay_index = 2 if real_idx != 2 else 0
            print_score = float(probs[0, print_index])
            replay_score = float(probs[0, replay_index])
            attack_type = "replay_attack" if replay_score >= print_score else "print_attack"

>>>>>>> 98bf8e49 (update)
        return {
            "label": label,
            "real_score": round(real_score, 6),
            "fake_score": round(fake_score, 6),
<<<<<<< HEAD
            "raw_probs": [round(float(x), 6) for x in probs[0].tolist()],
        }

=======
            "print_score": round(print_score, 6),
            "replay_score": round(replay_score, 6),
            "attack_type": attack_type,
            "raw_probs": [round(float(x), 6) for x in probs[0].tolist()],
        }

    def _aggregate_scores(self, scores: np.ndarray) -> float:
        mode = str(ANTI_SPOOF_SCORE_AGGREGATION).lower()
        if mode == "median":
            return float(np.median(scores))
        return float(np.mean(scores))

>>>>>>> 98bf8e49 (update)
    def evaluate_sequence(
        self,
        image_paths: Sequence[Path],
        bboxes: Sequence[Sequence[float]],
    ) -> Dict[str, Any]:
        if not image_paths or not bboxes or len(image_paths) != len(bboxes):
<<<<<<< HEAD
            raise ValueError("Invalid liveness frame sequence")

        heuristic = self.heuristic_engine.evaluate_sequence(image_paths, bboxes)

        predictions = [
            self.predict_frame(Path(image_path), bbox)
            for image_path, bbox in zip(image_paths, bboxes)
        ]

        real_scores = [float(item["real_score"]) for item in predictions]

        model_score = float(np.mean(real_scores))
        heuristic_score = float(heuristic.get("score", 0.0))

        real_frame_count = sum(score >= self.threshold for score in real_scores)
        real_frame_ratio = real_frame_count / max(len(real_scores), 1)

        final_score = 0.80 * model_score + 0.20 * heuristic_score
        final_score = float(np.clip(final_score, 0.0, 1.0))

        result = (
            "real"
            if final_score >= self.threshold and real_frame_ratio >= 0.60
            else "fake"
        )

        confidence = abs(final_score - self.threshold) + 0.5
        confidence = float(np.clip(confidence, 0.5, 0.99))

        return {
            "result": result,
            "score": round(final_score, 6),
            "confidence": round(confidence, 6),
            "threshold": self.threshold,
            "mode": f"{ANTI_SPOOF_MODEL_NAME}_onnx+heuristic",
            "frame_count": len(image_paths),
=======
            raise AppException(message="被动活体输入序列无效", code=4224, status_code=422)

        heuristic = heuristic_liveness_engine.evaluate_sequence(image_paths, bboxes)
        predictions = [
            self.predict_frame(image_path, bbox)
            for image_path, bbox in zip(image_paths, bboxes)
        ]

        real_scores = np.asarray([item["real_score"] for item in predictions], dtype=np.float32)
        print_scores = np.asarray([item["print_score"] for item in predictions], dtype=np.float32)
        replay_scores = np.asarray([item["replay_score"] for item in predictions], dtype=np.float32)

        model_score = self._aggregate_scores(real_scores)
        heuristic_score = float(heuristic.get("score", 0.0))
        real_frame_count = int(np.sum(real_scores >= float(ANTI_SPOOF_THRESHOLD)))
        real_frame_ratio = float(real_frame_count / max(len(real_scores), 1))

        final_score = float(
            np.clip(
                float(ANTI_SPOOF_MODEL_WEIGHT) * model_score
                + float(ANTI_SPOOF_HEURISTIC_WEIGHT) * heuristic_score,
                0.0,
                1.0,
            )
        )
        threshold = float(ANTI_SPOOF_THRESHOLD)
        uncertain_floor = threshold - float(ANTI_SPOOF_UNCERTAIN_MARGIN)

        if final_score >= threshold and real_frame_ratio >= float(ANTI_SPOOF_REAL_FRAME_RATIO):
            result = "real"
            reason = "被动活体融合校验通过"
        elif final_score >= uncertain_floor:
            result = "uncertain"
            reason = "被动活体融合结果接近阈值，建议重试或启用随机动作增强"
        else:
            result = "fake"
            reason = "被动活体融合判定存在照片或屏幕重放风险"

        confidence = float(np.clip(abs(final_score - threshold) + 0.5, 0.5, 0.99))
        mean_print_score = float(np.mean(print_scores)) if len(print_scores) else 0.0
        mean_replay_score = float(np.mean(replay_scores)) if len(replay_scores) else 0.0
        attack_type = "replay_attack" if mean_replay_score >= mean_print_score else "print_attack"

        return {
            "result": result,
            "decision": "allow" if result == "real" else ("retry" if result == "uncertain" else "block"),
            "reason": reason,
            "score": round(final_score, 6),
            "confidence": round(confidence, 6),
            "threshold": threshold,
            "mode": "passive_anti_spoof_fused",
            "verification_mode": "passive_anti_spoof_fused",
            "frame_count": len(image_paths),
            "accepted_frame_count": len(image_paths),
            "rejected_frame_count": 0,
            "quality_insufficient": False,
            "attack_suspected": result == "fake",
            "passive_result": result,
            "passive_score": round(final_score, 6),
            "passive_confidence": round(confidence, 6),
            "passive_threshold": threshold,
            "passive_reason": reason,
            "passive_attack_type": attack_type,
>>>>>>> 98bf8e49 (update)
            "model_score": round(model_score, 6),
            "heuristic_score": round(heuristic_score, 6),
            "real_frame_count": real_frame_count,
            "real_frame_ratio": round(real_frame_ratio, 6),
<<<<<<< HEAD
            "model_predictions": predictions,
            "static_score": round(float(heuristic.get("static_score", heuristic_score)), 6),
            "temporal": heuristic.get("temporal", {}),
            "frame_features": heuristic.get("frame_features", []),
            "heuristic_detail": heuristic,
        }

    def evaluate(self, image_path: Path, bbox: Iterable[float]) -> Dict[str, Any]:
        return self.evaluate_sequence([Path(image_path)], [list(bbox)])


model_liveness_engine = ModelLivenessEngine()
=======
            "static_score": round(float(heuristic.get("static_score", 0.0)), 6),
            "temporal": heuristic.get("temporal", {}),
            "model_predictions": predictions,
            "spoof_result": result,
            "spoof_score": round(final_score, 6),
            "spoof_confidence": round(confidence, 6),
            "spoof_attack_type": attack_type,
            "spoof_model_name": f"{ANTI_SPOOF_MODEL_NAME}+heuristic",
            "spoof_reason": reason,
            "spoof_real_threshold": threshold,
            "spoof_fake_threshold": uncertain_floor,
            "frame_debug": [
                {
                    "index": index + 1,
                    "real_score": item["real_score"],
                    "fake_score": item["fake_score"],
                    "print_score": item["print_score"],
                    "replay_score": item["replay_score"],
                    "label": item["label"],
                    "raw_probs": item["raw_probs"],
                }
                for index, item in enumerate(predictions)
            ],
            "frame_features": heuristic.get("frame_features", []),
            "risk_indicators": [
                {
                    "type": attack_type,
                    "score": round(max(mean_print_score, mean_replay_score), 6),
                }
            ],
            "challenge_used": False,
            "challenge_required": False,
            "challenge_result": "skipped",
            "challenge_score": None,
            "challenge_threshold": None,
            "challenge_reason": None,
            "challenge_action": None,
            "challenge_action_label": None,
            "challenge_prompt": None,
            "challenge_details": None,
            "challenge_id": None,
        }

    def evaluate(self, image_path: Path, bbox: Iterable[float]) -> Dict[str, Any]:
        return self.evaluate_sequence([image_path], [list(bbox)])


passive_liveness_engine = PassiveLivenessEngine()
>>>>>>> 98bf8e49 (update)
