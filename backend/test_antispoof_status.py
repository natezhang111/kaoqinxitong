import json
from app.services.model_liveness_engine import model_liveness_engine

status = model_liveness_engine.get_status()
print(json.dumps(status, ensure_ascii=False, indent=2))

if not status.get("initialized"):
    raise SystemExit("Anti-spoofing model was not initialized. Check last_error.")
