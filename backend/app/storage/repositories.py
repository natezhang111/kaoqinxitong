<<<<<<< HEAD
# from __future__ import annotations

# from typing import Any, Dict, List, Optional

# from app.core.config import (
#     ACTIVITIES_JSON,
#     ACTIVITY_FACE_RESULTS_JSON,
#     ATTENDANCE_JSON,
#     EMOTION_RECORDS_JSON,
#     EVALUATION_RECORDS_JSON,
#     SECURITY_TEST_RECORDS_JSON,
#     STUDENTS_JSON,
#     USERS_JSON,
# )
# from app.storage.json_store import JsonStore


# class BaseRepository:
#     def __init__(self, store: JsonStore) -> None:
#         self.store = store

#     def list_all(self) -> List[Dict[str, Any]]:
#         return self.store.read_all()

#     def get_by_id(self, record_id: int) -> Optional[Dict[str, Any]]:
#         return self.store.find_by_id(record_id)

#     def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
#         return self.store.insert(data)

#     def update(
#         self, record_id: int, updates: Dict[str, Any]
#     ) -> Optional[Dict[str, Any]]:
#         return self.store.update_by_id(record_id, updates)

#     def delete(self, record_id: int) -> bool:
#         return self.store.delete_by_id(record_id)


# class UserRepository(BaseRepository):
#     def get_by_username(self, username: str) -> Optional[Dict[str, Any]]:
#         return self.store.find_one(username=username)

#     def list_active_users(self) -> List[Dict[str, Any]]:
#         return self.store.filter(is_active=True)


# class StudentRepository(BaseRepository):
#     def get_by_student_no(self, student_no: str) -> Optional[Dict[str, Any]]:
#         return self.store.find_one(student_no=student_no)

#     def list_active_students(self) -> List[Dict[str, Any]]:
#         return self.store.filter(is_active=True)


# users_repo = UserRepository(JsonStore(USERS_JSON))
# students_repo = StudentRepository(JsonStore(STUDENTS_JSON))
# attendance_repo = BaseRepository(JsonStore(ATTENDANCE_JSON))
# activities_repo = BaseRepository(JsonStore(ACTIVITIES_JSON))
# activity_face_results_repo = BaseRepository(JsonStore(ACTIVITY_FACE_RESULTS_JSON))
# emotion_records_repo = BaseRepository(JsonStore(EMOTION_RECORDS_JSON))
# security_test_records_repo = BaseRepository(JsonStore(SECURITY_TEST_RECORDS_JSON))
# evaluation_records_repo = BaseRepository(JsonStore(EVALUATION_RECORDS_JSON))
from __future__ import annotations

from typing import Any, Dict, List, Optional

=======
# from __future__ import annotations

# from typing import Any, Dict, List, Optional

# from app.core.config import (
#     ACTIVITIES_JSON,
#     ACTIVITY_FACE_RESULTS_JSON,
#     ATTENDANCE_JSON,
#     EMOTION_RECORDS_JSON,
#     EVALUATION_RECORDS_JSON,
#     SECURITY_TEST_RECORDS_JSON,
#     STUDENTS_JSON,
#     USERS_JSON,
# )
# from app.storage.json_store import JsonStore


# class BaseRepository:
#     def __init__(self, store: JsonStore) -> None:
#         self.store = store

#     def list_all(self) -> List[Dict[str, Any]]:
#         return self.store.read_all()

#     def get_by_id(self, record_id: int) -> Optional[Dict[str, Any]]:
#         return self.store.find_by_id(record_id)

#     def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
#         return self.store.insert(data)

#     def update(
#         self, record_id: int, updates: Dict[str, Any]
#     ) -> Optional[Dict[str, Any]]:
#         return self.store.update_by_id(record_id, updates)

#     def delete(self, record_id: int) -> bool:
#         return self.store.delete_by_id(record_id)


# class UserRepository(BaseRepository):
#     def get_by_username(self, username: str) -> Optional[Dict[str, Any]]:
#         return self.store.find_one(username=username)

#     def list_active_users(self) -> List[Dict[str, Any]]:
#         return self.store.filter(is_active=True)


# class StudentRepository(BaseRepository):
#     def get_by_student_no(self, student_no: str) -> Optional[Dict[str, Any]]:
#         return self.store.find_one(student_no=student_no)

#     def list_active_students(self) -> List[Dict[str, Any]]:
#         return self.store.filter(is_active=True)


# users_repo = UserRepository(JsonStore(USERS_JSON))
# students_repo = StudentRepository(JsonStore(STUDENTS_JSON))
# attendance_repo = BaseRepository(JsonStore(ATTENDANCE_JSON))
# activities_repo = BaseRepository(JsonStore(ACTIVITIES_JSON))
# activity_face_results_repo = BaseRepository(JsonStore(ACTIVITY_FACE_RESULTS_JSON))
# emotion_records_repo = BaseRepository(JsonStore(EMOTION_RECORDS_JSON))
# security_test_records_repo = BaseRepository(JsonStore(SECURITY_TEST_RECORDS_JSON))
# evaluation_records_repo = BaseRepository(JsonStore(EVALUATION_RECORDS_JSON))
from __future__ import annotations

from typing import Any, Dict, List, Optional

>>>>>>> 98bf8e49 (update)
from app.core.config import (
    ACTIVITIES_JSON,
    ACTIVITY_FACE_RESULTS_JSON,
    AUDIT_LOGS_JSON,
    ATTENDANCE_JSON,
    EMOTION_RECORDS_JSON,
    EVALUATION_RECORDS_JSON,
<<<<<<< HEAD
    SECURITY_TEST_RECORDS_JSON,
    STUDENTS_JSON,
    USERS_JSON,
)
from app.storage.json_store import JsonStore


class BaseRepository:
    def __init__(self, store: JsonStore) -> None:
        self.store = store

    def list_all(self) -> List[Dict[str, Any]]:
        return self.store.read_all()

    def get_by_id(self, record_id: int) -> Optional[Dict[str, Any]]:
        return self.store.find_by_id(record_id)

=======
    SECURITY_TEST_RECORDS_JSON,
    STUDENTS_JSON,
    USERS_JSON,
)
from app.storage.json_store import JsonStore


class BaseRepository:
    def __init__(self, store: JsonStore) -> None:
        self.store = store

    def list_all(self) -> List[Dict[str, Any]]:
        return self.store.read_all()

    def get_by_id(self, record_id: int) -> Optional[Dict[str, Any]]:
        return self.store.find_by_id(record_id)

>>>>>>> 98bf8e49 (update)
    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self.store.insert(data)

    def bulk_create(self, data_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return self.store.bulk_insert(data_list)
<<<<<<< HEAD

    def update(
        self, record_id: int, updates: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        return self.store.update_by_id(record_id, updates)

    def delete(self, record_id: int) -> bool:
        return self.store.delete_by_id(record_id)


=======

    def update(
        self, record_id: int, updates: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        return self.store.update_by_id(record_id, updates)

    def delete(self, record_id: int) -> bool:
        return self.store.delete_by_id(record_id)


>>>>>>> 98bf8e49 (update)
class UserRepository(BaseRepository):
    def get_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        return self.store.find_one(username=username)

    def list_active_users(self) -> List[Dict[str, Any]]:
        return self.store.filter(is_active=True)

    def query_users(
        self,
        keyword: Optional[str] = None,
        role: Optional[str] = None,
        is_active: Optional[bool] = None,
    ) -> List[Dict[str, Any]]:
        users = self.store.read_all()
        result: List[Dict[str, Any]] = []
        keyword_lower = keyword.strip().lower() if keyword else None

        for item in users:
            if role is not None and item.get("role") != role:
                continue

            if is_active is not None and bool(item.get("is_active", True)) != is_active:
                continue

            if keyword_lower:
                username = str(item.get("username", "")).lower()
                if keyword_lower not in username:
                    continue

            result.append(item)

        return result
<<<<<<< HEAD


class StudentRepository(BaseRepository):
    def get_by_student_no(self, student_no: str) -> Optional[Dict[str, Any]]:
        return self.store.find_one(student_no=student_no)

    def list_active_students(self) -> List[Dict[str, Any]]:
        return self.store.filter(is_active=True)

    def query_students(
        self,
        keyword: Optional[str] = None,
        class_name: Optional[str] = None,
        is_active: Optional[bool] = None,
    ) -> List[Dict[str, Any]]:
        students = self.store.read_all()
        result: List[Dict[str, Any]] = []

        keyword_lower = keyword.strip().lower() if keyword else None

        for item in students:
            if class_name is not None and item.get("class_name") != class_name:
                continue

            if is_active is not None and bool(item.get("is_active", True)) != is_active:
                continue

            if keyword_lower:
                student_no = str(item.get("student_no", "")).lower()
                name = str(item.get("name", "")).lower()
                if keyword_lower not in student_no and keyword_lower not in name:
                    continue

            result.append(item)

        return result


users_repo = UserRepository(JsonStore(USERS_JSON))
students_repo = StudentRepository(JsonStore(STUDENTS_JSON))
attendance_repo = BaseRepository(JsonStore(ATTENDANCE_JSON))
activities_repo = BaseRepository(JsonStore(ACTIVITIES_JSON))
activity_face_results_repo = BaseRepository(JsonStore(ACTIVITY_FACE_RESULTS_JSON))
emotion_records_repo = BaseRepository(JsonStore(EMOTION_RECORDS_JSON))
security_test_records_repo = BaseRepository(JsonStore(SECURITY_TEST_RECORDS_JSON))
=======


class StudentRepository(BaseRepository):
    def get_by_student_no(self, student_no: str) -> Optional[Dict[str, Any]]:
        return self.store.find_one(student_no=student_no)

    def list_active_students(self) -> List[Dict[str, Any]]:
        return self.store.filter(is_active=True)

    def query_students(
        self,
        keyword: Optional[str] = None,
        class_name: Optional[str] = None,
        is_active: Optional[bool] = None,
    ) -> List[Dict[str, Any]]:
        students = self.store.read_all()
        result: List[Dict[str, Any]] = []

        keyword_lower = keyword.strip().lower() if keyword else None

        for item in students:
            if class_name is not None and item.get("class_name") != class_name:
                continue

            if is_active is not None and bool(item.get("is_active", True)) != is_active:
                continue

            if keyword_lower:
                student_no = str(item.get("student_no", "")).lower()
                name = str(item.get("name", "")).lower()
                if keyword_lower not in student_no and keyword_lower not in name:
                    continue

            result.append(item)

        return result


users_repo = UserRepository(JsonStore(USERS_JSON))
students_repo = StudentRepository(JsonStore(STUDENTS_JSON))
attendance_repo = BaseRepository(JsonStore(ATTENDANCE_JSON))
activities_repo = BaseRepository(JsonStore(ACTIVITIES_JSON))
activity_face_results_repo = BaseRepository(JsonStore(ACTIVITY_FACE_RESULTS_JSON))
emotion_records_repo = BaseRepository(JsonStore(EMOTION_RECORDS_JSON))
security_test_records_repo = BaseRepository(JsonStore(SECURITY_TEST_RECORDS_JSON))
>>>>>>> 98bf8e49 (update)
evaluation_records_repo = BaseRepository(JsonStore(EVALUATION_RECORDS_JSON))
audit_logs_repo = BaseRepository(JsonStore(AUDIT_LOGS_JSON))
