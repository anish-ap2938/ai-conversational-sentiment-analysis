import json
from pathlib import Path
from typing import List, Union

def load_conversations(input_path: Union[str, Path]) -> List[dict]:
    p = Path(input_path)
    convs = []
    if p.is_file():
        data = json.loads(p.read_text(encoding="utf-8"))
        convs = data if isinstance(data, list) else [data]
    elif p.is_dir():
        for f in sorted(p.glob("*.json")):
            data = json.loads(f.read_text(encoding="utf-8"))
            convs.extend(data if isinstance(data, list) else [data])
    else:
        raise FileNotFoundError(f"{input_path} not found")
    return convs