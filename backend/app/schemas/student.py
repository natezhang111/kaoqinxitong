<<<<<<< HEAD
# from __future__ import annotations

# from pydantic import BaseModel, Field
# from typing import Optional


# class StudentBase(BaseModel):
#     student_no: str = Field(..., min_length=1, max_length=20, example="20240001")
#     name: str = Field(..., min_length=1, max_length=64, example="张三")
#     class_name: str = Field(..., min_length=1, max_length=64, example="信安1班")
#     is_active: bool = True


# class StudentCreate(StudentBase):
#     pass


# class StudentUpdate(StudentBase):
#     name: Optional[str] = None
#     class_name: Optional[str] = None
#     is_active: Optional[bool] = None


# class StudentInDB(StudentBase):
#     id: int
#     face_image_path: str  # 存储人脸图片的路径
#     face_feature_path: str  # 存储提取的人脸特征的路径
#     created_at: str


# class StudentResponse(StudentInDB):
#     pass
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class StudentCreate(BaseModel):
    student_no: str = Field(..., min_length=1, max_length=32, description="学号")
    name: str = Field(..., min_length=1, max_length=64, description="姓名")
    class_name: str = Field(..., min_length=1, max_length=64, description="班级")
    is_active: bool = Field(default=True, description="是否启用")


class StudentUpdate(BaseModel):
    name: Optional[str] = Field(
        default=None, min_length=1, max_length=64, description="姓名"
    )
    class_name: Optional[str] = Field(
        default=None, min_length=1, max_length=64, description="班级"
    )
    is_active: Optional[bool] = Field(default=None, description="是否启用")


class StudentResponse(BaseModel):
    id: int
    student_no: str
    name: str
    class_name: str
    is_active: bool
    face_image_path: Optional[str] = None
    face_feature_path: Optional[str] = None
    feature_status: str = "pending"
    created_at: str


class StudentImportItem(BaseModel):
    student_no: str
    name: str
    class_name: str
    is_active: bool = True


class FaceUploadResponse(BaseModel):
    student_id: int
    student_no: str
    face_image_path: str
    face_feature_path: str
    feature_status: str
=======
# from __future__ import annotations

# from pydantic import BaseModel, Field
# from typing import Optional


# class StudentBase(BaseModel):
#     student_no: str = Field(..., min_length=1, max_length=20, example="20240001")
#     name: str = Field(..., min_length=1, max_length=64, example="张三")
#     class_name: str = Field(..., min_length=1, max_length=64, example="信安1班")
#     is_active: bool = True


# class StudentCreate(StudentBase):
#     pass


# class StudentUpdate(StudentBase):
#     name: Optional[str] = None
#     class_name: Optional[str] = None
#     is_active: Optional[bool] = None


# class StudentInDB(StudentBase):
#     id: int
#     face_image_path: str  # 存储人脸图片的路径
#     face_feature_path: str  # 存储提取的人脸特征的路径
#     created_at: str


# class StudentResponse(StudentInDB):
#     pass
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class StudentCreate(BaseModel):
    student_no: str = Field(..., min_length=1, max_length=32, description="学号")
    name: str = Field(..., min_length=1, max_length=64, description="姓名")
    class_name: str = Field(..., min_length=1, max_length=64, description="班级")
    is_active: bool = Field(default=True, description="是否启用")


class StudentUpdate(BaseModel):
    name: Optional[str] = Field(
        default=None, min_length=1, max_length=64, description="姓名"
    )
    class_name: Optional[str] = Field(
        default=None, min_length=1, max_length=64, description="班级"
    )
    is_active: Optional[bool] = Field(default=None, description="是否启用")


class StudentResponse(BaseModel):
    id: int
    student_no: str
    name: str
    class_name: str
    is_active: bool
    face_image_path: Optional[str] = None
    face_feature_path: Optional[str] = None
    feature_status: str = "pending"
    created_at: str


class StudentImportItem(BaseModel):
    student_no: str
    name: str
    class_name: str
    is_active: bool = True


class FaceUploadResponse(BaseModel):
    student_id: int
    student_no: str
    face_image_path: str
    face_feature_path: str
    feature_status: str
>>>>>>> 98bf8e49 (update)
