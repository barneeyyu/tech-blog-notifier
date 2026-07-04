import json
import pytest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from state import load_state, save_state

def test_load_state_returns_dict(tmp_path):
    state_file = tmp_path / "state.json"
    state_file.write_text(json.dumps({"netflix": ["id1"]}))
    result = load_state(str(state_file))
    assert result == {"netflix": ["id1"]}

def test_load_state_missing_file_returns_empty(tmp_path):
    result = load_state(str(tmp_path / "missing.json"))
    assert result == {}

def test_save_state_writes_json(tmp_path):
    state_file = tmp_path / "state.json"
    save_state({"uber": ["id2"]}, str(state_file))
    content = json.loads(state_file.read_text())
    assert content == {"uber": ["id2"]}
