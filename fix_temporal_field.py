from pathlib import Path

path = Path("backend/app/services/model_liveness_engine.py")
text = path.read_text(encoding="utf-8")

old = '''            "model_predictions": predictions,
            "heuristic_detail": heuristic,
'''

new = '''            "model_predictions": predictions,
            "static_score": round(float(heuristic.get("static_score", heuristic_score)), 6),
            "temporal": heuristic.get("temporal", {}),
            "frame_features": heuristic.get("frame_features", []),
            "heuristic_detail": heuristic,
'''

if old not in text:
    raise SystemExit("没有找到需要替换的位置，可能代码已经改过。请手动检查 model_liveness_engine.py")

text = text.replace(old, new)
path.write_text(text, encoding="utf-8")

print("已修复 model_liveness_engine.py：补充 temporal/static_score/frame_features 顶层字段")
