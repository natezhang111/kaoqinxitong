# AGENTS.md

Guidance for AI coding agents working in this repository (B/S attendance system:
FastAPI backend + Vue 3 frontend, JSON file storage, face recognition + liveness +
emotion models).

## Project layout

```
Time_Attendance_prv/
├─ backend/          # FastAPI app (Python 3.10+)
│  ├─ app/{api,core,services,schemas,storage,utils}
│  ├─ data/{json,faces,features,uploads,reports,logs}
│  ├─ models/        # antispoof + emotion model weights (downloaded)
│  ├─ requirements.txt / environment.yml
│  └─ run.py         # uvicorn entrypoint
├─ frontend/         # Vue 3 + Element Plus + Vite
│  └─ src/{api,router,views,components,constants,utils}
├─ test/zy.csv       # sample CSV import data (NOT a test suite)
├─ README.md / 框架.md / 修改记录.md
```

## Build / run / verify commands

Run backend (from `backend/`):
```powershell
pip install -r requirements.txt          # or: conda env create -f environment.yml && conda activate attendance_cs
python run.py                              # serves http://127.0.0.1:8000 (docs at /docs)
```

Run frontend (from `frontend/`):
```powershell
npm install
npm run dev                                # http://127.0.0.1:5173 with /api proxy
npm run build                              # production build (use this to type-check)
npm run preview
```

Smoke-test backend without pytest (project has no test framework configured):
```powershell
# From backend/ directory
@'
import sys; sys.dont_write_bytecode = True
from fastapi.testclient import TestClient
from app.main import app
c = TestClient(app)
print(c.post("/api/v1/auth/login", json={"username":"teacher","password":"123456"}).status_code)
'@ | python -B -
```

Health checks: `GET /api/v1/system/health`, `GET /api/v1/system/model-status`.
Default credentials: `teacher/123456`; students log in with `student_no` (e.g. `20240001/123456`).

There is no linter, formatter, pytest, ESLint, or Prettier config. Do NOT introduce one
without being asked. When changing Python code, at minimum run the TestClient snippet
above; when changing frontend code, run `npm run build`.

## Architecture rules

Layering (enforce strictly, see `框架.md` for rationale):
```
api/ (routers) → services/ (business logic) → storage/repositories → json_store → data/json/*.json
```
- Routers in `app/api/*.py` only do param validation, auth, and response shaping.
- Put business logic in `app/services/*_service.py`, not in routers.
- Data access goes through `app.storage.repositories` (JSON-backed; `json_store.py` is
  list-of-dict with a threading `Lock`). Do not read/write `data/json/*.json` directly.
- Face/liveness/emotion model code lives in `services/face_engine.py`,
  `liveness_engine.py` (+ `heuristic_*`, `model_*` variants), `emotion_engine.py`.
  Keep model loading lazy; surface state via `app.core.config.MODEL_STATUS`.

Paths, thresholds, and JSON filenames are centralised in `app/core/config.py`. Add new
constants there rather than hardcoding. Call `ensure_json_files()` on startup only.

## Backend conventions

- Every module starts with `from __future__ import annotations`.
- Type hints everywhere: `Optional`, `List[Dict[str, Any]]`, etc. (not PEP 604 `|` unions
  in public signatures, to match existing style).
- Response envelope: always return via `app.utils.response.success_response(data=, message=)`
  / `error_response(...)`. Shape is `{code, message, data}`.
- Errors: raise `AppException(message, code, status_code)` from
  `app.core.exceptions`. Do not raise `HTTPException`. Message strings are Chinese
  (user-facing). 4xxx = client errors, 5xxx = server errors; follow existing numeric
  codes when extending (e.g. 4001 bad request, 4010 unauth, 4031 teacher required).
- Auth: use `Depends(get_current_user)`, `Depends(require_teacher)`,
  `Depends(require_student)` from `app/core/deps.py`. JWT is HS256, secret in
  `config.py` (do not commit real secrets; flag if asked).
- Audit logging: for any state-changing action call
  `audit_log_service.record(module=, action=, result=, message=, operator=, target_*=)`.
  Record both success and failure paths (see `api/auth.py` for the pattern).
- Timestamps: `datetime.now().strftime(DATETIME_FORMAT)` where
  `DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"`. Store as strings in JSON.
- Pydantic v2 (2.9). Schemas live in `app/schemas/`. Use `Field(..., description="...")`
  with Chinese descriptions.
- Routers: `APIRouter(prefix="/<resource>", tags=["<resource>"])`, registered in
  `app/main.py` under `API_PREFIX = "/api/v1"`.
- Imports: stdlib → third-party → `app.*`, each group separated by a blank line,
  absolute imports only.
- Naming: `snake_case` for funcs/vars/files, `PascalCase` for classes and Pydantic
  models, module-level singletons lowercase (`face_engine`, `audit_log_service`).
- File I/O: use `pathlib.Path` from `app.core.config`; never hardcode `data/...` paths.
- Soft delete over hard delete: prefer `is_active=False` for students/users to preserve
  history (see `框架.md` §三.2.6).

## Frontend conventions

- Vue 3 `<script setup>` SFCs, Composition API. One view per file in `src/views/`.
- Element Plus components (`el-*`) with `ElMessage`/`ElMessageBox` for feedback.
- API calls: thin wrappers in `src/api/*.js` over the shared `http` axios instance in
  `src/api/http.js` (auto-attaches `Bearer` from `localStorage.attendance_token`, auto
  redirects to `/login` on 401). Keep per-resource files; do not call axios directly.
- Routing: `src/router/index.js` with `beforeEach` that enforces teacher-only pages vs
  `/student-portal` for the student role. Add new routes to both the route table and
  (if teacher-only) the student redirect block.
- Local storage keys: `attendance_token`, `attendance_user` (JSON). Reuse these.
- Strings shown to users are Chinese (matches backend messages).
- Naming: views `PascalCase.vue`, api modules `camelCase.js`, routes kebab-case.
- 2-space indent, double-quoted strings, semicolons (see existing files).

## JSON store gotchas

- Every file in `data/json/` must be a JSON list. `json_store.JsonStore` expects
  `[...]`; corrupt / non-list files raise `ValueError`.
- `next_id()` is `max(id)+1`; safe under the instance lock but not across processes.
  Assume single-process uvicorn.
- Writes rewrite the whole file. Avoid chatty per-item updates in tight loops; prefer
  `bulk_insert` / read-modify-write-all.

## Safety and environment notes

- Windows + PowerShell is the primary dev environment. Prefer PowerShell-safe commands
  (`Invoke-RestMethod`, here-strings with `@'...'@`) when scripting.
- `__pycache__` may have write-permission quirks on Windows; this breaks `compileall`
  but not runtime. Do not set `PYTHONDONTWRITEBYTECODE` as a fix unless asked.
- Model downloads are handled by `download_antispoof_model.ps1` and
  `download_dan_model.py` (both gitignored). Do not commit weights under `models/`.
- `.gitignore` excludes `.vscode`, `docs`, `*.pptx`, the download scripts, and
  `框架.md`. Do not add these back.
- No Cursor rules (`.cursor/rules/`, `.cursorrules`) or Copilot instructions
  (`.github/copilot-instructions.md`) exist at the time of writing.
- Reply in the language of the task. Most in-repo prose (README, `框架.md`,
  `修改记录.md`, commit trail) is in Simplified Chinese; match that when editing
  those docs, and keep user-facing strings in code in Chinese.
