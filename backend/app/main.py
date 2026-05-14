<<<<<<< HEAD
from __future__ import annotations

from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.attendance import router as attendance_router
from app.api.audit_logs import router as audit_logs_router
from app.api.auth import router as auth_router
from app.api.emotions import router as emotions_router
from app.api.group_photos import router as group_photos_router
from app.api.security_tests import router as security_tests_router
from app.api.statistics import router as statistics_router
from app.api.students import ensure_student_accounts_for_all_students
from app.api.students import router as students_router
from app.api.system import router as system_router
from app.api.users import router as users_router
from app.core.config import API_PREFIX, APP_NAME, APP_VERSION, ensure_json_files
from app.core.exceptions import register_exception_handlers
from app.core.security import get_password_hash
from app.storage.repositories import users_repo


def initialize_default_users() -> None:
    users = users_repo.list_all()
    if users:
        return

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    default_users = [
        {
            "username": "teacher",
            "password_hash": get_password_hash("123456"),
            "role": "teacher",
            "student_id": None,
            "is_active": True,
            "created_at": now,
        },
        {
            "username": "student1",
            "password_hash": get_password_hash("123456"),
            "role": "student",
            "student_id": None,
            "is_active": True,
            "created_at": now,
        },
    ]

    for user in default_users:
        users_repo.create(user)


@asynccontextmanager
async def lifespan(app: FastAPI):
    ensure_json_files()
    initialize_default_users()
    ensure_student_accounts_for_all_students()
    yield


app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    lifespan=lifespan,
    debug=True,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)

app.include_router(auth_router, prefix=API_PREFIX)
app.include_router(system_router, prefix=API_PREFIX)
app.include_router(students_router, prefix=API_PREFIX)
app.include_router(attendance_router, prefix=API_PREFIX)
app.include_router(emotions_router, prefix=API_PREFIX)
app.include_router(security_tests_router, prefix=API_PREFIX)
app.include_router(group_photos_router, prefix=API_PREFIX)
app.include_router(statistics_router, prefix=API_PREFIX)
app.include_router(users_router, prefix=API_PREFIX)
app.include_router(audit_logs_router, prefix=API_PREFIX)


@app.get("/")
async def root():
    return {
        "message": f"{APP_NAME} is running",
        "docs": "/docs",
        "api_prefix": API_PREFIX,
        "version": APP_VERSION,
    }
=======
from __future__ import annotations

from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.attendance import router as attendance_router
from app.api.audit_logs import router as audit_logs_router
from app.api.auth import router as auth_router
from app.api.emotions import router as emotions_router
from app.api.group_photos import router as group_photos_router
from app.api.liveness import router as liveness_router
from app.api.security_tests import router as security_tests_router
from app.api.statistics import router as statistics_router
from app.api.students import ensure_student_accounts_for_all_students
from app.api.students import router as students_router
from app.api.system import router as system_router
from app.api.users import router as users_router
from app.core.config import (
    API_PREFIX,
    APP_NAME,
    APP_VERSION,
    DATA_DIR,
    ensure_json_files,
)
from app.core.exceptions import register_exception_handlers
from app.core.security import get_password_hash
from app.storage.repositories import users_repo


def initialize_default_users() -> None:
    users = users_repo.list_all()
    if users:
        return

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    default_users = [
        {
            "username": "teacher",
            "password_hash": get_password_hash("123456"),
            "role": "teacher",
            "student_id": None,
            "is_active": True,
            "created_at": now,
        },
        {
            "username": "student1",
            "password_hash": get_password_hash("123456"),
            "role": "student",
            "student_id": None,
            "is_active": True,
            "created_at": now,
        },
    ]

    for user in default_users:
        users_repo.create(user)


@asynccontextmanager
async def lifespan(app: FastAPI):
    ensure_json_files()
    initialize_default_users()
    ensure_student_accounts_for_all_students()
    yield


app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    lifespan=lifespan,
    debug=True,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)

app.mount("/uploads", StaticFiles(directory=DATA_DIR / "uploads"), name="uploads")
app.mount("/faces", StaticFiles(directory=DATA_DIR / "faces"), name="faces")

app.include_router(auth_router, prefix=API_PREFIX)
app.include_router(system_router, prefix=API_PREFIX)
app.include_router(students_router, prefix=API_PREFIX)
app.include_router(attendance_router, prefix=API_PREFIX)
app.include_router(liveness_router, prefix=API_PREFIX)
app.include_router(emotions_router, prefix=API_PREFIX)
app.include_router(security_tests_router, prefix=API_PREFIX)
app.include_router(group_photos_router, prefix=API_PREFIX)
app.include_router(statistics_router, prefix=API_PREFIX)
app.include_router(users_router, prefix=API_PREFIX)
app.include_router(audit_logs_router, prefix=API_PREFIX)


@app.get("/")
async def root():
    return {
        "message": f"{APP_NAME} is running",
        "docs": "/docs",
        "api_prefix": API_PREFIX,
        "version": APP_VERSION,
    }
>>>>>>> 98bf8e49 (update)
