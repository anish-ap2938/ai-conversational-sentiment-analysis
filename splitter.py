# splitter.py

import json
from pathlib import Path
from collections import defaultdict

def split_by_user(convs: list, out_dir: Path):
    """
    For each conversation in `convs`, write out a file named
      {screen_name}_{ref_conversation_id}.json
    into `out_dir`.  If the same user+conversation_id is seen multiple
    times, we append _2, _3, ... so nothing ever gets overwritten.
    """
    out_dir.mkdir(parents=True, exist_ok=True)

    
    seen = defaultdict(int)

    for conv in convs:
        cid = conv["ref_conversation_id"]
       
        human = next(m for m in conv["messages_list"] if m["ref_user_id"] != 1)
        user = human["screen_name"]

        base = f"{user}_{cid}"
        seen[base] += 1
        count = seen[base]

        if count == 1:
            filename = f"{base}.json"
        else:
            filename = f"{base}_{count}.json"

        dest = out_dir / filename
        dest.write_text(json.dumps(conv, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[SPLIT] → {dest}")

