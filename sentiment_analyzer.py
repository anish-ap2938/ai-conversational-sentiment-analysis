# sentiment_analyzer.py
import json
from pathlib import Path
from transformers import pipeline

def analyze_sentiment(
    topic_dir: Path,
    out_dir: Path,
    *,
    min_score: float = 0.5,
    max_per_topic: int | None = 3
):
    
    analyzer = pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english"
    )
    out_dir.mkdir(parents=True, exist_ok=True)

    for tf in sorted(topic_dir.glob("*.json")):
        raw = json.loads(tf.read_text(encoding="utf-8"))
        user, cid, _ = tf.stem.split("_", 2)

        summary: dict[str, dict] = {}

        for topic, entries in raw.items():
            
            filtered = [e for e in entries if e.get("score", 0) >= min_score]
            if not filtered:
                continue 

           
            filtered.sort(key=lambda e: e["score"], reverse=True)

            
            if max_per_topic is not None:
                filtered = filtered[:max_per_topic]

            
            pos = neg = 0
            detailed = []
            for e in filtered:
                res = analyzer(e["message"])[0]
                lbl = res["label"]
                sc  = round(float(res["score"]), 3)
                if lbl == "POSITIVE":
                    pos += 1
                else:
                    neg += 1

                detailed.append({
                    "timestamp":      e["transaction_datetime_utc"],
                    "message":        e["message"],
                    "sentiment":      lbl,
                    "sentiment_score": sc,
                    "relevance_score": round(float(e["score"]), 3)
                })

            overall = "POSITIVE" if pos >= neg else "NEGATIVE"
            summary[topic] = {
                "overall_sentiment": overall,
                "positive_count":    pos,
                "negative_count":    neg,
                "messages":          detailed
            }

        if summary:
            out_path = out_dir / f"{user}_{cid}_topics_sentiment.json"
            out_path.write_text(
                json.dumps(summary, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            print(f"[SENTIMENT] → {out_path}")
        else:
            print(f"[SENTIMENT] → skipping {tf.name} (no topics above min_score)")
