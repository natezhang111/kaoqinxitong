from __future__ import annotations

<<<<<<< HEAD
from pathlib import Path
from typing import Any, Dict, Optional, Sequence

import numpy as np
from PIL import Image, UnidentifiedImageError

from app.core.exceptions import AppException
=======
import math
import pickle
from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Sequence

import numpy as np
from PIL import Image, ImageOps, UnidentifiedImageError

from app.core.config import (
    EMOTION_DAN_CHECKPOINT,
    EMOTION_DAN_IMAGE_SIZE,
    EMOTION_DAN_LABELS,
    EMOTION_DAN_NUM_HEAD,
    EMOTION_FALLBACK_ENABLED,
    EMOTION_MODEL_NAME,
)
from app.core.exceptions import AppException
from app.models.dan import DAN, sanitize_state_dict

try:
    import torch
    from torchvision import transforms
except Exception as exc:  # pragma: no cover
    torch = None
    transforms = None
    _torchvision_import_error = exc
else:
    _torchvision_import_error = None
>>>>>>> 98bf8e49 (update)


class EmotionEngine:
    def __init__(self) -> None:
<<<<<<< HEAD
        self._status: Dict[str, Any] = {
            "initialized": True,
            "mode": "heuristic_face_texture",
            "labels": ["happy", "neutral", "serious", "tired", "excited"],
            "last_error": None,
        }

    def get_status(self) -> Dict[str, Any]:
=======
        self._device = None
        self._model = None
        self._transform = None
        self._status: Dict[str, Any] = {
            "initialized": False,
            "mode": EMOTION_MODEL_NAME,
            "labels": list(EMOTION_DAN_LABELS),
            "num_classes": len(EMOTION_DAN_LABELS),
            "checkpoint_path": str(EMOTION_DAN_CHECKPOINT),
            "checkpoint_exists": False,
            "checkpoint_size": 0,
            "device": None,
            "fallback_enabled": EMOTION_FALLBACK_ENABLED,
            "last_error": None,
        }
        self._refresh_checkpoint_status()

    def _refresh_checkpoint_status(self) -> None:
        exists = EMOTION_DAN_CHECKPOINT.exists()
        self._status["checkpoint_exists"] = exists
        self._status["checkpoint_size"] = EMOTION_DAN_CHECKPOINT.stat().st_size if exists else 0

    def get_status(self) -> Dict[str, Any]:
        self._refresh_checkpoint_status()
>>>>>>> 98bf8e49 (update)
        return dict(self._status)

    @staticmethod
    def _read_image(image_path: Path) -> Image.Image:
        if not image_path.exists():
<<<<<<< HEAD
            raise AppException(message="图片文件不存在", code=4001, status_code=400)
=======
            raise AppException(message="image file does not exist", code=4001, status_code=400)
>>>>>>> 98bf8e49 (update)

        try:
            return Image.open(image_path).convert("RGB")
        except UnidentifiedImageError:
<<<<<<< HEAD
            raise AppException(message="无法识别图片格式", code=4002, status_code=400)
        except Exception as exc:
            raise AppException(message=f"图片读取失败: {exc}", code=4003, status_code=400)

    @staticmethod
    def _crop_face(image: Image.Image, bbox: Optional[Sequence[float]]) -> Image.Image:
        if not bbox:
            return image

        width, height = image.size
        x1, y1, x2, y2 = [float(value) for value in bbox]
        padding_x = max((x2 - x1) * 0.08, 4.0)
        padding_y = max((y2 - y1) * 0.08, 4.0)

        left = max(int(x1 - padding_x), 0)
        top = max(int(y1 - padding_y), 0)
        right = min(int(x2 + padding_x), width)
        bottom = min(int(y2 + padding_y), height)

        if right <= left or bottom <= top:
            return image
        return image.crop((left, top, right, bottom))
=======
            raise AppException(message="unsupported image format", code=4002, status_code=400)
        except Exception as exc:
            raise AppException(message=f"failed to read image: {exc}", code=4003, status_code=400)

    @staticmethod
    def _clamp_crop_box(
        width: int,
        height: int,
        left: float,
        top: float,
        right: float,
        bottom: float,
    ) -> tuple[int, int, int, int]:
        x1 = max(0, int(math.floor(left)))
        y1 = max(0, int(math.floor(top)))
        x2 = min(width, int(math.ceil(right)))
        y2 = min(height, int(math.ceil(bottom)))
        if x2 <= x1 or y2 <= y1:
            return 0, 0, width, height
        return x1, y1, x2, y2

    @staticmethod
    def _rotate_points(
        points: Sequence[Sequence[float]],
        *,
        center_x: float,
        center_y: float,
        angle_degrees: float,
    ) -> list[list[float]]:
        rad = math.radians(angle_degrees)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        output: list[list[float]] = []
        for x, y in points:
            dx = float(x) - center_x
            dy = float(y) - center_y
            rx = center_x + dx * cos_a - dy * sin_a
            ry = center_y + dx * sin_a + dy * cos_a
            output.append([rx, ry])
        return output

    def _prepare_face(
        self,
        image: Image.Image,
        bbox: Optional[Sequence[float]],
        landmarks: Optional[Sequence[Sequence[float]]],
    ) -> Image.Image:
        image = ImageOps.exif_transpose(image)
        width, height = image.size

        if landmarks and len(landmarks) >= 2:
            points = [[float(x), float(y)] for x, y in landmarks[:5]]
            left_eye = points[0]
            right_eye = points[1]
            eye_center_x = (left_eye[0] + right_eye[0]) / 2.0
            eye_center_y = (left_eye[1] + right_eye[1]) / 2.0
            angle = math.degrees(
                math.atan2(right_eye[1] - left_eye[1], right_eye[0] - left_eye[0] + 1e-6)
            )
            rotated = image.rotate(-angle, resample=Image.BILINEAR, center=(eye_center_x, eye_center_y))
            rotated_points = self._rotate_points(
                points,
                center_x=eye_center_x,
                center_y=eye_center_y,
                angle_degrees=-angle,
            )

            xs = [item[0] for item in rotated_points]
            ys = [item[1] for item in rotated_points]
            eye_distance = max(
                math.hypot(right_eye[0] - left_eye[0], right_eye[1] - left_eye[1]),
                1.0,
            )
            if bbox and len(bbox) == 4:
                face_width = max(float(bbox[2]) - float(bbox[0]), eye_distance * 2.0)
                face_height = max(float(bbox[3]) - float(bbox[1]), eye_distance * 2.2)
            else:
                face_width = max(max(xs) - min(xs), eye_distance * 2.0)
                face_height = max(max(ys) - min(ys), eye_distance * 2.2)

            pad_x = max(face_width * 0.22, eye_distance * 0.45)
            pad_top = max(face_height * 0.38, eye_distance * 0.75)
            pad_bottom = max(face_height * 0.26, eye_distance * 0.55)
            crop_box = self._clamp_crop_box(
                width,
                height,
                min(xs) - pad_x,
                min(ys) - pad_top,
                max(xs) + pad_x,
                max(ys) + pad_bottom,
            )
            return rotated.crop(crop_box)

        if bbox and len(bbox) == 4:
            x1, y1, x2, y2 = [float(value) for value in bbox]
            padding_x = max((x2 - x1) * 0.18, 8.0)
            padding_y = max((y2 - y1) * 0.18, 8.0)
            crop_box = self._clamp_crop_box(
                width,
                height,
                x1 - padding_x,
                y1 - padding_y,
                x2 + padding_x,
                y2 + padding_y,
            )
            return image.crop(crop_box)

        return image
>>>>>>> 98bf8e49 (update)

    @staticmethod
    def _confidence(distance: float) -> float:
        return round(min(max(0.55 + distance * 2.2, 0.55), 0.98), 6)

<<<<<<< HEAD
=======
    @staticmethod
    def _summarize_keys(keys: Sequence[str], *, limit: int = 8) -> str:
        if not keys:
            return "[]"
        normalized = [str(item) for item in keys]
        head = normalized[:limit]
        suffix = "" if len(normalized) <= limit else f", ... ({len(normalized)} total)"
        return "[" + ", ".join(head) + suffix + "]"

    @staticmethod
    def _detect_invalid_checkpoint(path: Path) -> Optional[str]:
        if not path.exists():
            return f"checkpoint file does not exist: {path}"

        file_size = path.stat().st_size
        if file_size <= 0:
            return f"checkpoint file is empty: {path}"

        if file_size < 16 * 1024:
            try:
                preview = path.read_text(encoding="utf-8", errors="ignore")[:1024].lower()
            except Exception:
                preview = ""
            if "<html" in preview or "google drive" in preview or "download anyway" in preview:
                return (
                    "checkpoint file is an HTML download page instead of a real .pth model file"
                )
            return f"checkpoint file is suspiciously small ({file_size} bytes)"

        try:
            with path.open("rb") as handle:
                header = handle.read(16)
        except Exception as exc:
            return f"failed to inspect checkpoint header: {exc}"

        if header.startswith(b"<!DOCTYPE html") or header.startswith(b"<html"):
            return "checkpoint file is HTML instead of a PyTorch checkpoint"
        return None

    @staticmethod
    def _torch_load_checkpoint(path: Path, device: Any) -> Any:
        try:
            return torch.load(str(path), map_location=device, weights_only=False)
        except TypeError:
            return torch.load(str(path), map_location=device)

    @staticmethod
    def _extract_state_dict(checkpoint: Any) -> Mapping[str, Any]:
        if isinstance(checkpoint, Mapping):
            candidates = (
                "model_state_dict",
                "state_dict",
                "model",
                "net",
                "params",
                "weights",
            )
            for key in candidates:
                candidate = checkpoint.get(key)
                if isinstance(candidate, Mapping):
                    return candidate

            tensor_like_values = sum(1 for value in checkpoint.values() if hasattr(value, "shape"))
            if tensor_like_values >= max(1, len(checkpoint) // 2):
                return checkpoint

            raise AppException(
                message=(
                    "unsupported DAN checkpoint structure; top-level keys="
                    f"{EmotionEngine._summarize_keys(list(checkpoint.keys()))}"
                ),
                code=5013,
                status_code=500,
            )

        raise AppException(
            message=f"unsupported DAN checkpoint object type: {type(checkpoint).__name__}",
            code=5013,
            status_code=500,
        )

    def _heuristic_predict(self, face: Image.Image) -> Dict[str, Any]:
        arr = np.asarray(face, dtype=np.float32) / 255.0
        if arr.size == 0:
            raise AppException(message="empty face crop for emotion analysis", code=5009, status_code=500)

        gray = 0.299 * arr[..., 0] + 0.587 * arr[..., 1] + 0.114 * arr[..., 2]
        brightness = float(np.mean(gray))
        contrast = float(np.std(gray))
        chroma = np.max(arr, axis=2) - np.min(arr, axis=2)
        saturation = float(np.mean(chroma))
        warmth = float(np.mean(arr[..., 0] - arr[..., 2]))

        half = max(gray.shape[0] // 2, 1)
        upper_mean = float(np.mean(gray[:half, :]))
        lower_mean = float(np.mean(gray[half:, :]))
        lower_delta = lower_mean - upper_mean

        if brightness < 0.34 and contrast < 0.18:
            emotion = "tired"
            score = self._confidence(max(0.34 - brightness, 0.18 - contrast))
        elif lower_delta > 0.045 and contrast > 0.16:
            emotion = "happy"
            score = self._confidence(max(lower_delta - 0.045, contrast - 0.16))
        elif contrast > 0.24 and saturation > 0.20:
            emotion = "excited"
            score = self._confidence(max(contrast - 0.24, saturation - 0.20))
        elif saturation < 0.10 or lower_delta < -0.015 or warmth < -0.01:
            emotion = "serious"
            score = self._confidence(max(0.10 - saturation, -lower_delta - 0.015, -warmth - 0.01))
        else:
            emotion = "neutral"
            score = round(
                min(
                    max(
                        0.62
                        + (0.12 - abs(lower_delta)) * 0.8
                        + (0.20 - abs(contrast - 0.18)) * 0.4,
                        0.58,
                    ),
                    0.92,
                ),
                6,
            )

        return {
            "emotion": emotion,
            "score": score,
            "mode": "heuristic_face_texture_fallback",
            "topk": [{"emotion": emotion, "score": score}],
            "probabilities": {emotion: score},
            "metrics": {
                "brightness": round(brightness, 6),
                "contrast": round(contrast, 6),
                "saturation": round(saturation, 6),
                "warmth": round(warmth, 6),
                "lower_delta": round(lower_delta, 6),
            },
        }

    def _ensure_model(self) -> None:
        if self._model is not None and self._transform is not None:
            return

        if torch is None or transforms is None:
            self._status.update(
                {
                    "initialized": False,
                    "device": None,
                    "last_error": f"PyTorch / torchvision import failed: {_torchvision_import_error}",
                }
            )
            raise AppException(
                message=f"PyTorch / torchvision import failed: {_torchvision_import_error}",
                code=5011,
                status_code=500,
            )

        self._refresh_checkpoint_status()
        if not EMOTION_DAN_CHECKPOINT.exists():
            self._status.update(
                {
                    "initialized": False,
                    "device": None,
                    "last_error": f"checkpoint file does not exist: {EMOTION_DAN_CHECKPOINT}",
                }
            )
            raise AppException(
                message=f"DAN checkpoint does not exist: {EMOTION_DAN_CHECKPOINT}",
                code=5012,
                status_code=500,
            )

        try:
            invalid_reason = self._detect_invalid_checkpoint(EMOTION_DAN_CHECKPOINT)
            if invalid_reason:
                self._status.update(
                    {
                        "initialized": False,
                        "device": None,
                        "last_error": invalid_reason,
                    }
                )
                raise AppException(
                    message=f"invalid DAN checkpoint: {invalid_reason}",
                    code=5013,
                    status_code=500,
                )

            self._device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
            model = DAN(
                num_class=len(EMOTION_DAN_LABELS),
                num_head=EMOTION_DAN_NUM_HEAD,
                pretrained=False,
            )

            try:
                checkpoint = self._torch_load_checkpoint(EMOTION_DAN_CHECKPOINT, self._device)
            except pickle.UnpicklingError as exc:
                raise AppException(
                    message=f"failed to unpickle DAN checkpoint: {exc}",
                    code=5013,
                    status_code=500,
                ) from exc

            raw_state_dict = self._extract_state_dict(checkpoint)
            state_dict = sanitize_state_dict(raw_state_dict)
            incompatible = model.load_state_dict(state_dict, strict=False)
            if incompatible.missing_keys or incompatible.unexpected_keys:
                raise AppException(
                    message=(
                        "DAN checkpoint does not match model architecture; "
                        f"missing_keys={self._summarize_keys(incompatible.missing_keys)}, "
                        f"unexpected_keys={self._summarize_keys(incompatible.unexpected_keys)}"
                    ),
                    code=5013,
                    status_code=500,
                )

            model.eval().to(self._device)
            self._model = model
            self._transform = transforms.Compose(
                [
                    transforms.Resize((EMOTION_DAN_IMAGE_SIZE, EMOTION_DAN_IMAGE_SIZE)),
                    transforms.ToTensor(),
                    transforms.Normalize(
                        mean=[0.485, 0.456, 0.406],
                        std=[0.229, 0.224, 0.225],
                    ),
                ]
            )
            self._status.update(
                {
                    "initialized": True,
                    "device": str(self._device),
                    "last_error": None,
                }
            )
        except AppException:
            self._status.update({"initialized": False, "device": None})
            raise
        except Exception as exc:
            self._status.update(
                {
                    "initialized": False,
                    "device": None,
                    "last_error": str(exc),
                }
            )
            raise AppException(message=f"failed to load DAN model: {exc}", code=5013, status_code=500)

    def _predict_with_dan(self, face: Image.Image) -> Dict[str, Any]:
        self._ensure_model()
        if self._model is None or self._transform is None or torch is None:
            raise AppException(message="DAN model is not initialized", code=5014, status_code=500)

        tensor = self._transform(face).unsqueeze(0).to(self._device)
        with torch.no_grad():
            logits, _, _ = self._model(tensor)
            probabilities = torch.softmax(logits, dim=1).detach().cpu().numpy()[0]

        top_indices = np.argsort(probabilities)[::-1][:3]
        topk = [
            {
                "emotion": EMOTION_DAN_LABELS[int(index)],
                "score": round(float(probabilities[int(index)]), 6),
            }
            for index in top_indices
        ]
        best_index = int(np.argmax(probabilities))
        best_score = round(float(probabilities[best_index]), 6)
        return {
            "emotion": EMOTION_DAN_LABELS[best_index],
            "score": best_score,
            "mode": EMOTION_MODEL_NAME,
            "topk": topk,
            "probabilities": {
                label: round(float(probabilities[index]), 6)
                for index, label in enumerate(EMOTION_DAN_LABELS)
            },
            "metrics": {
                "input_size": EMOTION_DAN_IMAGE_SIZE,
                "top1_index": best_index,
            },
        }

>>>>>>> 98bf8e49 (update)
    def analyze_face(
        self,
        image_path: Path,
        bbox: Optional[Sequence[float]] = None,
<<<<<<< HEAD
    ) -> Dict[str, Any]:
        try:
            image = self._read_image(image_path)
            face = self._crop_face(image, bbox)
            arr = np.asarray(face, dtype=np.float32) / 255.0
            if arr.size == 0:
                raise AppException(message="情绪分析区域为空", code=5009, status_code=500)

            gray = 0.299 * arr[..., 0] + 0.587 * arr[..., 1] + 0.114 * arr[..., 2]
            brightness = float(np.mean(gray))
            contrast = float(np.std(gray))
            chroma = np.max(arr, axis=2) - np.min(arr, axis=2)
            saturation = float(np.mean(chroma))
            warmth = float(np.mean(arr[..., 0] - arr[..., 2]))

            half = max(gray.shape[0] // 2, 1)
            upper_mean = float(np.mean(gray[:half, :]))
            lower_mean = float(np.mean(gray[half:, :]))
            lower_delta = lower_mean - upper_mean

            if brightness < 0.34 and contrast < 0.18:
                emotion = "tired"
                score = self._confidence(max(0.34 - brightness, 0.18 - contrast))
            elif lower_delta > 0.045 and contrast > 0.16:
                emotion = "happy"
                score = self._confidence(max(lower_delta - 0.045, contrast - 0.16))
            elif contrast > 0.24 and saturation > 0.20:
                emotion = "excited"
                score = self._confidence(max(contrast - 0.24, saturation - 0.20))
            elif saturation < 0.10 or lower_delta < -0.015 or warmth < -0.01:
                emotion = "serious"
                score = self._confidence(
                    max(0.10 - saturation, -lower_delta - 0.015, -warmth - 0.01)
                )
            else:
                emotion = "neutral"
                score = round(
                    min(
                        max(
                            0.62
                            + (0.12 - abs(lower_delta)) * 0.8
                            + (0.20 - abs(contrast - 0.18)) * 0.4,
                            0.58,
                        ),
                        0.92,
                    ),
                    6,
                )

            return {
                "emotion": emotion,
                "score": score,
                "mode": self._status["mode"],
                "metrics": {
                    "brightness": round(brightness, 6),
                    "contrast": round(contrast, 6),
                    "saturation": round(saturation, 6),
                    "warmth": round(warmth, 6),
                    "lower_delta": round(lower_delta, 6),
                },
            }
=======
        landmarks: Optional[Sequence[Sequence[float]]] = None,
    ) -> Dict[str, Any]:
        try:
            image = self._read_image(image_path)
            face = self._prepare_face(image, bbox, landmarks)
            try:
                return self._predict_with_dan(face)
            except Exception as dan_exc:
                self._status["last_error"] = str(dan_exc)
                if not EMOTION_FALLBACK_ENABLED:
                    if isinstance(dan_exc, AppException):
                        raise dan_exc
                    raise AppException(
                        message=f"emotion inference failed: {dan_exc}",
                        code=5010,
                        status_code=500,
                    )

                fallback = self._heuristic_predict(face)
                fallback["fallback_from"] = EMOTION_MODEL_NAME
                fallback["fallback_reason"] = str(dan_exc)
                return fallback
>>>>>>> 98bf8e49 (update)
        except AppException as exc:
            self._status["last_error"] = str(exc.message)
            raise
        except Exception as exc:
            self._status["last_error"] = str(exc)
            raise AppException(
<<<<<<< HEAD
                message=f"情绪识别失败: {exc}",
=======
                message=f"emotion inference failed: {exc}",
>>>>>>> 98bf8e49 (update)
                code=5010,
                status_code=500,
            )


emotion_engine = EmotionEngine()
