import json
from pathlib import Path

def load_state(path: str) -> dict:
    p = Path(path)
    if not p.exists():
        return {}
    return json.loads(p.read_text())

def save_state(state: dict, path: str) -> None:
    Path(path).write_text(json.dumps(state, indent=2, ensure_ascii=False))
