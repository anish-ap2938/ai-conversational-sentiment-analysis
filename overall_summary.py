# overall_summary.py

import json
from pathlib import Path
from typing import Dict

def generate_overall_sentiments(
    topic_sentiment_dir: Path,
    out_dir: Path,
):
    """
    For each <user>_<cid>_topics_sentiment.json in topic_sentiment_dir,
    produces <user>_<cid>_overall.json in out_dir with the shape:
      {
        "<topic1>": "<overall_sentiment>",
        "<topic2>": "<overall_sentiment>",
        ...
      }
    """
    
    out_dir.mkdir(parents=True, exist_ok=True)

   
    for tf in sorted(topic_sentiment_dir.glob("*_topics_sentiment.json")):
        
        data: Dict[str, Dict] = json.loads(tf.read_text(encoding="utf-8"))
       
        user_cid = tf.stem.replace("_topics_sentiment", "")

       
        summary: Dict[str, str] = {
            topic: details["overall_sentiment"]
            for topic, details in data.items()
        }

        
        out_path = out_dir / f"{user_cid}_overall.json"
        out_path.write_text(
            json.dumps(summary, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        print(f"[REPORT] → {out_path}")
