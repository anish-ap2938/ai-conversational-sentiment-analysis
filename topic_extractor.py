# topic_extractor.py

import json
from pathlib import Path
from typing import List
from transformers import pipeline

def extract_topics(
    input_dir: Path,
    topics: List[str],
    out_dir: Path,
    threshold: float = 0.7
):
   
    classifier = pipeline(
        "zero-shot-classification",
        model="facebook/bart-large-mnli",
        multi_label=True
    )
    out_dir.mkdir(parents=True, exist_ok=True)

    for jf in sorted(input_dir.glob("*.json")):
        conv = json.loads(jf.read_text(encoding="utf-8"))
        cid  = conv["ref_conversation_id"]
        user = jf.stem.split("_")[0]

       
        buckets = {t: [] for t in topics}

        for m in conv["messages_list"]:
            
            if m["ref_user_id"] == 1:
                continue

            text = m["message"].strip()
            if not text:
                continue

            
            res = classifier(text, candidate_labels=topics)
            
            for label, score in zip(res["labels"], res["scores"]):
                if score >= threshold:
                    buckets[label].append({
                        "transaction_datetime_utc": m["transaction_datetime_utc"],
                        "message": text,
                        "score": round(score, 3)
                    })

        
        filtered = {t: hits for t, hits in buckets.items() if hits}

        out_path = out_dir / f"{user}_{cid}_topics.json"
        out_path.write_text(
            json.dumps(filtered, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        print(f"[TOPICS] → {out_path}")
