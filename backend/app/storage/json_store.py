<<<<<<< HEAD
from __future__ import annotations

import json
from pathlib import Path
from threading import Lock
from typing import Any, Dict, List, Optional


class JsonStore:
    """
    Lightweight JSON file store for list-based records.
    Each file must contain a JSON list.
    """

    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path
        self._lock = Lock()
        self._ensure_file()

    def _ensure_file(self) -> None:
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self.file_path.write_text("[]", encoding="utf-8")

    def read_all(self) -> List[Dict[str, Any]]:
        with self._lock:
            raw = self.file_path.read_text(encoding="utf-8").strip()
            if not raw:
                return []
            data = json.loads(raw)
            if not isinstance(data, list):
                raise ValueError(f"{self.file_path} must contain a JSON list.")
            return data

    def write_all(self, records: List[Dict[str, Any]]) -> None:
        with self._lock:
            self.file_path.write_text(
                json.dumps(records, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

    def next_id(self) -> int:
        records = self.read_all()
        if not records:
            return 1
        return max(int(item.get("id", 0)) for item in records) + 1

    def insert(self, record: Dict[str, Any]) -> Dict[str, Any]:
        records = self.read_all()
        if "id" not in record:
            record["id"] = self.next_id()
        records.append(record)
        self.write_all(records)
        return record

    def bulk_insert(self, new_records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        records = self.read_all()
        next_id = self.next_id()
        inserted_records: List[Dict[str, Any]] = []
        for item in new_records:
            item_copy = dict(item)
            if "id" not in item_copy:
                item_copy["id"] = next_id
                next_id += 1
            inserted_records.append(item_copy)
        records.extend(inserted_records)
        self.write_all(records)
        return inserted_records

    def find_by_id(self, record_id: int) -> Optional[Dict[str, Any]]:
        records = self.read_all()
        for item in records:
            if int(item.get("id", 0)) == record_id:
                return item
        return None

    def find_one(self, **conditions: Any) -> Optional[Dict[str, Any]]:
        records = self.read_all()
        for item in records:
            if all(item.get(key) == value for key, value in conditions.items()):
                return item
        return None

    def filter(self, **conditions: Any) -> List[Dict[str, Any]]:
        records = self.read_all()
        result = []
        for item in records:
            matched = True
            for key, value in conditions.items():
                if item.get(key) != value:
                    matched = False
                    break
            if matched:
                result.append(item)
        return result

    def update_by_id(
        self, record_id: int, updates: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        records = self.read_all()
        updated_record: Optional[Dict[str, Any]] = None

        for idx, item in enumerate(records):
            if int(item.get("id", 0)) == record_id:
                records[idx] = {**item, **updates, "id": record_id}
                updated_record = records[idx]
                break

        if updated_record is not None:
            self.write_all(records)

        return updated_record

    def delete_by_id(self, record_id: int) -> bool:
        records = self.read_all()
        new_records = [item for item in records if int(item.get("id", 0)) != record_id]
        if len(new_records) == len(records):
            return False
        self.write_all(new_records)
        return True
=======
from __future__ import annotations

import json
from pathlib import Path
from threading import Lock
from typing import Any, Dict, List, Optional


class JsonStore:
    """
    Lightweight JSON file store for list-based records.
    Each file must contain a JSON list.
    """

    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path
        self._lock = Lock()
        self._ensure_file()

    def _ensure_file(self) -> None:
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self.file_path.write_text("[]", encoding="utf-8")

    def read_all(self) -> List[Dict[str, Any]]:
        with self._lock:
            raw = self.file_path.read_text(encoding="utf-8").strip()
            if not raw:
                return []
            data = json.loads(raw)
            if not isinstance(data, list):
                raise ValueError(f"{self.file_path} must contain a JSON list.")
            return data

    def write_all(self, records: List[Dict[str, Any]]) -> None:
        with self._lock:
            self.file_path.write_text(
                json.dumps(records, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

    def next_id(self) -> int:
        records = self.read_all()
        if not records:
            return 1
        return max(int(item.get("id", 0)) for item in records) + 1

    def insert(self, record: Dict[str, Any]) -> Dict[str, Any]:
        records = self.read_all()
        if "id" not in record:
            record["id"] = self.next_id()
        records.append(record)
        self.write_all(records)
        return record

    def bulk_insert(self, new_records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        records = self.read_all()
        next_id = self.next_id()
        inserted_records: List[Dict[str, Any]] = []
        for item in new_records:
            item_copy = dict(item)
            if "id" not in item_copy:
                item_copy["id"] = next_id
                next_id += 1
            inserted_records.append(item_copy)
        records.extend(inserted_records)
        self.write_all(records)
        return inserted_records

    def find_by_id(self, record_id: int) -> Optional[Dict[str, Any]]:
        records = self.read_all()
        for item in records:
            if int(item.get("id", 0)) == record_id:
                return item
        return None

    def find_one(self, **conditions: Any) -> Optional[Dict[str, Any]]:
        records = self.read_all()
        for item in records:
            if all(item.get(key) == value for key, value in conditions.items()):
                return item
        return None

    def filter(self, **conditions: Any) -> List[Dict[str, Any]]:
        records = self.read_all()
        result = []
        for item in records:
            matched = True
            for key, value in conditions.items():
                if item.get(key) != value:
                    matched = False
                    break
            if matched:
                result.append(item)
        return result

    def update_by_id(
        self, record_id: int, updates: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        records = self.read_all()
        updated_record: Optional[Dict[str, Any]] = None

        for idx, item in enumerate(records):
            if int(item.get("id", 0)) == record_id:
                records[idx] = {**item, **updates, "id": record_id}
                updated_record = records[idx]
                break

        if updated_record is not None:
            self.write_all(records)

        return updated_record

    def delete_by_id(self, record_id: int) -> bool:
        records = self.read_all()
        new_records = [item for item in records if int(item.get("id", 0)) != record_id]
        if len(new_records) == len(records):
            return False
        self.write_all(new_records)
        return True
>>>>>>> 98bf8e49 (update)
