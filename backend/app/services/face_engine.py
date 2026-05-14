from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

import numpy as np
from PIL import Image, UnidentifiedImageError

from app.core.config import FACE_IMAGE_SIZE, FACE_MARGIN, FACE_MIN_SIZE
from app.core.exceptions import AppException

try:
    import torch
except Exception as exc:  # pragma: no cover
    torch = None
    _torch_import_error = exc
else:
    _torch_import_error = None

try:
    from facenet_pytorch import InceptionResnetV1, MTCNN
except Exception as exc:  # pragma: no cover
    InceptionResnetV1 = None
    MTCNN = None
    _facenet_import_error = exc
else:
    _facenet_import_error = None


class FaceEngine:
    def __init__(self) -> None:
        self._device = None
        self._mtcnn_single = None
        self._mtcnn_multi = None
        self._resnet = None
        self._status: Dict[str, Any] = {
            "initialized": False,
            "device": None,
            "detector": "MTCNN",
            "embedder": "InceptionResnetV1",
            "embedding_dim": 512,
            "last_error": None,
        }

    def get_status(self) -> Dict[str, Any]:
        return dict(self._status)

    def _ensure_dependencies(self) -> None:
        if torch is None:
            raise AppException(
                message=f"PyTorch 未正确安装: {_torch_import_error}",
                code=5001,
                status_code=500,
            )
        if MTCNN is None or InceptionResnetV1 is None:
            raise AppException(
                message=f"facenet-pytorch 未正确安装: {_facenet_import_error}",
                code=5002,
                status_code=500,
            )

    def _init_models(self) -> None:
        if (
            self._mtcnn_single is not None
            and self._mtcnn_multi is not None
            and self._resnet is not None
        ):
            return

        self._ensure_dependencies()

        try:
            self._device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

            self._mtcnn_single = MTCNN(
                image_size=FACE_IMAGE_SIZE,
                margin=FACE_MARGIN,
                min_face_size=FACE_MIN_SIZE,
                keep_all=False,
                post_process=True,
                device=self._device,
            )

            self._mtcnn_multi = MTCNN(
                image_size=FACE_IMAGE_SIZE,
                margin=FACE_MARGIN,
                min_face_size=FACE_MIN_SIZE,
                keep_all=True,
                post_process=True,
                device=self._device,
            )

            self._resnet = InceptionResnetV1(pretrained="vggface2").eval().to(self._device)

            self._status.update(
                {
                    "initialized": True,
                    "device": str(self._device),
                    "last_error": None,
                }
            )
        except Exception as exc:
            self._status.update(
                {
                    "initialized": False,
                    "device": None,
                    "last_error": str(exc),
                }
            )
            raise AppException(
                message=f"人脸识别模型初始化失败: {exc}",
                code=5003,
                status_code=500,
            )

    @staticmethod
    def _read_image(image_path: Path) -> Image.Image:
        if not image_path.exists():
            raise AppException(message="图片文件不存在", code=4001, status_code=400)

        try:
            image = Image.open(image_path).convert("RGB")
        except UnidentifiedImageError:
            raise AppException(message="无法识别图片格式", code=4002, status_code=400)
        except Exception as exc:
            raise AppException(message=f"图片读取失败: {exc}", code=4003, status_code=400)

        return image

    @staticmethod
    def _normalize_embedding(embedding: np.ndarray) -> np.ndarray:
        embedding = np.asarray(embedding, dtype=np.float32)
        norm = float(np.linalg.norm(embedding))
        if norm <= 1e-12:
            raise AppException(message="提取到的特征向量无效", code=5004, status_code=500)
        return embedding / norm

<<<<<<< HEAD
    def _detect_with_mtcnn(self, image: Image.Image, keep_all: bool) -> Dict[str, Any]:
        self._init_models()
        detector = self._mtcnn_multi if keep_all else self._mtcnn_single
        boxes, probs = detector.detect(image)
=======
    def _detect_with_mtcnn(
        self, image: Image.Image, keep_all: bool, include_landmarks: bool = False
    ) -> Dict[str, Any]:
        self._init_models()
        detector = self._mtcnn_multi if keep_all else self._mtcnn_single
        detect_result = detector.detect(image, landmarks=include_landmarks)
        if include_landmarks:
            boxes, probs, landmarks = detect_result
        else:
            boxes, probs = detect_result
            landmarks = None
>>>>>>> 98bf8e49 (update)

        if boxes is None or len(boxes) == 0:
            return {
                "count": 0,
                "boxes": [],
                "probs": [],
<<<<<<< HEAD
=======
                "landmarks": [],
>>>>>>> 98bf8e49 (update)
            }

        box_list: List[List[float]] = []
        prob_list: List[float] = []
<<<<<<< HEAD
=======
        landmark_list: List[List[List[float]]] = []
>>>>>>> 98bf8e49 (update)
        for index, box in enumerate(boxes):
            box_list.append([float(x) for x in box.tolist()])
            prob = probs[index] if probs is not None else None
            prob_list.append(float(prob) if prob is not None else 0.0)
<<<<<<< HEAD
=======
            if landmarks is not None:
                landmark = landmarks[index]
                landmark_list.append([[float(x), float(y)] for x, y in landmark.tolist()])
>>>>>>> 98bf8e49 (update)

        return {
            "count": len(box_list),
            "boxes": box_list,
            "probs": prob_list,
<<<<<<< HEAD
=======
            "landmarks": landmark_list,
>>>>>>> 98bf8e49 (update)
        }

    def detect_faces(self, image_path: Path) -> Dict[str, Any]:
        image = self._read_image(image_path)
        return self._detect_with_mtcnn(image, keep_all=True)

    def extract_single_face_embedding(self, image_path: Path) -> Dict[str, Any]:
        self._init_models()
        image = self._read_image(image_path)
<<<<<<< HEAD
        detection = self._detect_with_mtcnn(image, keep_all=True)
=======
        detection = self._detect_with_mtcnn(image, keep_all=True, include_landmarks=True)
>>>>>>> 98bf8e49 (update)
        count = detection["count"]

        if count == 0:
            raise AppException(message="图片中未检测到人脸", code=4004, status_code=400)

        if count > 1:
            raise AppException(
                message="图片中检测到多张人脸，请上传仅包含一名学生的人脸照片",
                code=4005,
                status_code=400,
            )

        face_tensor = self._mtcnn_single(image)
        if face_tensor is None:
            raise AppException(message="人脸裁剪失败", code=5005, status_code=500)

        with torch.no_grad():
            embedding_tensor = self._resnet(face_tensor.unsqueeze(0).to(self._device))

        embedding = embedding_tensor.squeeze(0).detach().cpu().numpy().astype(np.float32)
        embedding = self._normalize_embedding(embedding)

        return {
            "embedding": embedding,
            "embedding_dim": int(embedding.shape[0]),
            "bbox": detection["boxes"][0],
            "det_score": detection["probs"][0],
<<<<<<< HEAD
=======
            "landmarks": detection["landmarks"][0] if detection["landmarks"] else None,
>>>>>>> 98bf8e49 (update)
        }

    def extract_multiple_face_embeddings(self, image_path: Path) -> Dict[str, Any]:
        self._init_models()
        image = self._read_image(image_path)
<<<<<<< HEAD
        detection = self._detect_with_mtcnn(image, keep_all=True)
=======
        detection = self._detect_with_mtcnn(image, keep_all=True, include_landmarks=True)
>>>>>>> 98bf8e49 (update)

        if detection["count"] == 0:
            return {
                "count": 0,
                "faces": [],
            }

        face_tensors = self._mtcnn_multi(image)
        if face_tensors is None or len(face_tensors) == 0:
            return {
                "count": 0,
                "faces": [],
            }

        with torch.no_grad():
            embedding_tensors = self._resnet(face_tensors.to(self._device))

        faces: List[Dict[str, Any]] = []
        for index in range(len(face_tensors)):
            embedding = embedding_tensors[index].detach().cpu().numpy().astype(np.float32)
            faces.append(
                {
                    "embedding": self._normalize_embedding(embedding),
                    "embedding_dim": int(embedding.shape[0]),
                    "bbox": detection["boxes"][index],
                    "det_score": detection["probs"][index],
<<<<<<< HEAD
=======
                    "landmarks": detection["landmarks"][index] if detection["landmarks"] else None,
>>>>>>> 98bf8e49 (update)
                }
            )

        return {
            "count": len(faces),
            "faces": faces,
        }

    @staticmethod
    def save_embedding(embedding: np.ndarray, feature_path: Path) -> None:
        feature_path.parent.mkdir(parents=True, exist_ok=True)
        np.save(str(feature_path), embedding.astype(np.float32))

    @staticmethod
    def load_embedding(feature_path: Path) -> np.ndarray:
        if not feature_path.exists():
            raise AppException(message="特征文件不存在", code=4041, status_code=404)
        return np.asarray(np.load(str(feature_path)), dtype=np.float32)

    @staticmethod
    def cosine_similarity(embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        emb1 = np.asarray(embedding1, dtype=np.float32)
        emb2 = np.asarray(embedding2, dtype=np.float32)
        norm1 = float(np.linalg.norm(emb1))
        norm2 = float(np.linalg.norm(emb2))
        if norm1 <= 1e-12 or norm2 <= 1e-12:
            return 0.0
        return float(np.dot(emb1, emb2) / (norm1 * norm2))


face_engine = FaceEngine()
