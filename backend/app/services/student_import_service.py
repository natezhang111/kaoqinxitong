from __future__ import annotations

import csv
import io
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, Optional
from uuid import uuid4

from app.core.config import ALLOWED_IMAGE_SUFFIXES, FACE_EMBEDDING_EXT, FACES_DIR, FEATURES_DIR
from app.core.exceptions import AppException
from app.services.face_engine import face_engine
from app.storage.repositories import students_repo

DEFAULT_STUDENT_PASSWORD = "123456"


class StudentImportService:
    @staticmethod
    def now_str() -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def build_feature_filename(student_no: str) -> str:
        return f"{student_no}{FACE_EMBEDDING_EXT}"

    @classmethod
    def build_feature_relpath(cls, student_no: str) -> str:
        return f"features/{cls.build_feature_filename(student_no)}"

    @staticmethod
    def build_face_relpath(filename: str) -> str:
        return f"faces/{filename}"

    @staticmethod
    def normalize_bool(value: str | bool | None, default: bool = True) -> bool:
        if value is None:
            return default
        if isinstance(value, bool):
            return value

        text = str(value).strip().lower()
        if text in {"true", "1", "yes", "y", "on"}:
            return True
        if text in {"false", "0", "no", "n", "off"}:
            return False
        return default

    @staticmethod
    def validate_image_filename(filename: Optional[str]) -> str:
        if not filename:
            raise AppException(message="上传图片缺少文件名", code=4001, status_code=400)

        suffix = Path(filename).suffix.lower()
        if suffix not in ALLOWED_IMAGE_SUFFIXES:
            raise AppException(
                message=f"不支持的图片格式，仅支持: {sorted(ALLOWED_IMAGE_SUFFIXES)}",
                code=4002,
                status_code=400,
            )
        return suffix

    @staticmethod
    def validate_csv_filename(filename: Optional[str]) -> None:
        if not filename or not filename.lower().endswith(".csv"):
            raise AppException(message="仅支持上传 CSV 文件", code=4005, status_code=400)

    @staticmethod
    def validate_zip_filename(filename: Optional[str]) -> None:
        if not filename or not filename.lower().endswith(".zip"):
            raise AppException(message="照片压缩包必须是 ZIP 文件", code=4012, status_code=400)

    @classmethod
    def parse_csv_rows(cls, content_bytes: bytes) -> list[dict[str, str]]:
        if not content_bytes:
            raise AppException(message="CSV 文件内容为空", code=4006, status_code=400)

        try:
            text = content_bytes.decode("utf-8-sig")
        except UnicodeDecodeError:
            raise AppException(message="CSV 文件编码需为 UTF-8", code=4007, status_code=400)

        reader = csv.DictReader(io.StringIO(text))
        required_columns = {"student_no", "name", "class_name"}
        if reader.fieldnames is None:
            raise AppException(message="CSV 缺少表头", code=4008, status_code=400)

        fieldnames = {name.strip() for name in reader.fieldnames if name}
        if not required_columns.issubset(fieldnames):
            raise AppException(
                message="CSV 表头必须包含: student_no,name,class_name",
                code=4009,
                status_code=400,
            )

        return list(reader)

    @classmethod
    def parse_photo_zip(
        cls,
        photos_zip_bytes: Optional[bytes],
        photos_zip_filename: Optional[str],
    ) -> dict[str, Any]:
        if photos_zip_bytes is None and photos_zip_filename is None:
            return {
                "photos_zip_provided": False,
                "photo_entries": {},
                "duplicate_photo_keys": {},
                "duplicate_photo_files": [],
            }

        cls.validate_zip_filename(photos_zip_filename)
        if not photos_zip_bytes:
            raise AppException(message="照片 ZIP 文件内容为空", code=4013, status_code=400)

        try:
            archive = zipfile.ZipFile(io.BytesIO(photos_zip_bytes))
        except zipfile.BadZipFile:
            raise AppException(message="照片压缩包不是有效的 ZIP 文件", code=4014, status_code=400)

        photo_entries: dict[str, dict[str, Any]] = {}
        duplicate_photo_keys: dict[str, list[str]] = {}

        with archive:
            for info in archive.infolist():
                if info.is_dir():
                    continue

                filename = Path(info.filename).name
                if not filename:
                    continue

                suffix = Path(filename).suffix.lower()
                if suffix not in ALLOWED_IMAGE_SUFFIXES:
                    continue

                student_no = Path(filename).stem.strip()
                if not student_no:
                    continue

                content = archive.read(info)
                if not content:
                    continue

                if student_no in duplicate_photo_keys:
                    duplicate_photo_keys[student_no].append(filename)
                    continue

                if student_no in photo_entries:
                    duplicate_photo_keys[student_no] = [
                        photo_entries[student_no]["filename"],
                        filename,
                    ]
                    photo_entries.pop(student_no, None)
                    continue

                photo_entries[student_no] = {
                    "filename": filename,
                    "bytes": content,
                }

        if photos_zip_bytes is not None and not photo_entries and not duplicate_photo_keys:
            raise AppException(
                message="照片 ZIP 中未找到可用图片，请确认图片格式及文件名",
                code=4015,
                status_code=400,
            )

        duplicate_photo_files = [
            {"student_no": key, "filenames": filenames}
            for key, filenames in sorted(duplicate_photo_keys.items())
        ]
        return {
            "photos_zip_provided": True,
            "photo_entries": photo_entries,
            "duplicate_photo_keys": duplicate_photo_keys,
            "duplicate_photo_files": duplicate_photo_files,
        }

    @classmethod
    def import_student_photo(
        cls,
        *,
        student: Dict[str, Any],
        original_filename: str,
        file_bytes: bytes,
    ) -> Dict[str, Any]:
        suffix = cls.validate_image_filename(original_filename)
        student_no = str(student["student_no"])
        unique_name = f"{student_no}_{uuid4().hex}{suffix}"
        image_save_path = FACES_DIR / unique_name
        feature_save_path = FEATURES_DIR / cls.build_feature_filename(student_no)

        image_save_path.write_bytes(file_bytes)

        try:
            result = face_engine.extract_single_face_embedding(image_save_path)
            face_engine.save_embedding(result["embedding"], feature_save_path)
        except Exception:
            if image_save_path.exists():
                image_save_path.unlink(missing_ok=True)
            if feature_save_path.exists():
                feature_save_path.unlink(missing_ok=True)
            raise

        face_relpath = cls.build_face_relpath(unique_name)
        feature_relpath = cls.build_feature_relpath(student_no)
        updated = students_repo.update(
            int(student["id"]),
            {
                "face_image_path": face_relpath,
                "face_feature_path": feature_relpath,
                "feature_status": "ready",
            },
        )
        if updated is None:
            raise AppException(message="保存学生照片信息失败", code=5003, status_code=500)

        return {
            "student": updated,
            "face_image_path": face_relpath,
            "face_feature_path": feature_relpath,
            "feature_status": "ready",
            "embedding_dim": result["embedding_dim"],
            "det_score": result["det_score"],
            "bbox": result["bbox"],
        }

    @classmethod
    def import_students(
        cls,
        *,
        csv_bytes: bytes,
        csv_filename: Optional[str],
        photos_zip_bytes: Optional[bytes],
        photos_zip_filename: Optional[str],
        ensure_student_account: Callable[..., Dict[str, Any]],
        serialize_student: Callable[[Dict[str, Any]], Dict[str, Any]],
    ) -> Dict[str, Any]:
        cls.validate_csv_filename(csv_filename)
        rows = cls.parse_csv_rows(csv_bytes)
        photo_bundle = cls.parse_photo_zip(photos_zip_bytes, photos_zip_filename)
        photos_zip_provided = bool(photo_bundle["photos_zip_provided"])
        photo_entries = photo_bundle["photo_entries"]
        duplicate_photo_keys = photo_bundle["duplicate_photo_keys"]
        consumed_photo_student_nos: set[str] = set()

        created = []
        skipped = []
        photo_missing = []
        photo_failed = []
        photo_bound_count = 0

        for idx, row in enumerate(rows, start=2):
            student_no = str(row.get("student_no", "")).strip()
            name = str(row.get("name", "")).strip()
            class_name = str(row.get("class_name", "")).strip()
            is_active = cls.normalize_bool(row.get("is_active"), default=True)

            if not student_no or not name or not class_name:
                skipped.append(
                    {
                        "row": idx,
                        "reason": "student_no、name、class_name 不能为空",
                    }
                )
                continue

            existing = students_repo.get_by_student_no(student_no)
            if existing is not None:
                skipped.append(
                    {
                        "row": idx,
                        "student_no": student_no,
                        "reason": "学号已存在，已跳过",
                    }
                )
                continue

            student = None
            try:
                student = students_repo.create(
                    {
                        "student_no": student_no,
                        "name": name,
                        "class_name": class_name,
                        "is_active": is_active,
                        "face_image_path": None,
                        "face_feature_path": cls.build_feature_relpath(student_no),
                        "feature_status": "pending",
                        "created_at": cls.now_str(),
                    }
                )
                ensure_student_account(student)
            except AppException as exc:
                if student is not None:
                    students_repo.delete(int(student["id"]))
                skipped.append(
                    {
                        "row": idx,
                        "student_no": student_no,
                        "reason": exc.message,
                    }
                )
                continue
            except Exception as exc:
                if student is not None:
                    students_repo.delete(int(student["id"]))
                skipped.append(
                    {
                        "row": idx,
                        "student_no": student_no,
                        "reason": str(exc),
                    }
                )
                continue

            current_student = student
            photo_status = "pending"
            photo_message = "未提供照片 ZIP，学生档案已创建"

            if not photos_zip_provided:
                pass
            elif student_no in duplicate_photo_keys:
                updated = students_repo.update(
                    int(student["id"]),
                    {
                        "face_image_path": None,
                        "feature_status": "failed",
                    },
                )
                current_student = updated or student
                photo_status = "failed"
                photo_message = f"ZIP 中存在多个同学号照片文件: {', '.join(duplicate_photo_keys[student_no])}"
                photo_failed.append(
                    {
                        "row": idx,
                        "student_no": student_no,
                        "reason": photo_message,
                    }
                )
            elif student_no in photo_entries:
                photo_entry = photo_entries[student_no]
                consumed_photo_student_nos.add(student_no)
                try:
                    photo_result = cls.import_student_photo(
                        student=current_student,
                        original_filename=photo_entry["filename"],
                        file_bytes=photo_entry["bytes"],
                    )
                    current_student = photo_result["student"]
                    photo_status = "ready"
                    photo_message = "照片导入并完成人脸特征提取"
                    photo_bound_count += 1
                except AppException as exc:
                    updated = students_repo.update(
                        int(student["id"]),
                        {
                            "face_image_path": None,
                            "feature_status": "failed",
                        },
                    )
                    current_student = updated or student
                    photo_status = "failed"
                    photo_message = exc.message
                    photo_failed.append(
                        {
                            "row": idx,
                            "student_no": student_no,
                            "filename": photo_entry["filename"],
                            "reason": exc.message,
                        }
                    )
                except Exception as exc:
                    updated = students_repo.update(
                        int(student["id"]),
                        {
                            "face_image_path": None,
                            "feature_status": "failed",
                        },
                    )
                    current_student = updated or student
                    photo_status = "failed"
                    photo_message = str(exc)
                    photo_failed.append(
                        {
                            "row": idx,
                            "student_no": student_no,
                            "filename": photo_entry["filename"],
                            "reason": str(exc),
                        }
                    )
            else:
                photo_status = "missing"
                photo_message = "未在 ZIP 中找到与学号同名的照片文件"
                photo_missing.append(
                    {
                        "row": idx,
                        "student_no": student_no,
                        "reason": photo_message,
                    }
                )

            created_item = serialize_student(current_student)
            created_item["photo_import_status"] = photo_status
            created_item["photo_import_message"] = photo_message
            created.append(created_item)

        unmatched_photos = [
            {
                "student_no": student_no,
                "filename": photo_entry["filename"],
            }
            for student_no, photo_entry in sorted(photo_entries.items())
            if student_no not in consumed_photo_student_nos
        ]

        return {
            "created_count": len(created),
            "skipped_count": len(skipped),
            "photo_bound_count": photo_bound_count,
            "photo_missing_count": len(photo_missing),
            "photo_failed_count": len(photo_failed),
            "unmatched_photo_count": len(unmatched_photos),
            "duplicate_photo_count": len(photo_bundle["duplicate_photo_files"]),
            "default_password": DEFAULT_STUDENT_PASSWORD,
            "created": created,
            "skipped": skipped,
            "photo_missing": photo_missing,
            "photo_failed": photo_failed,
            "unmatched_photos": unmatched_photos,
            "duplicate_photos": photo_bundle["duplicate_photo_files"],
        }


student_import_service = StudentImportService()
