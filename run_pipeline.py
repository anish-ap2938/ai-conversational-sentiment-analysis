# run_pipeline.py

import argparse
import json
from pathlib import Path

from data_ingest import load_conversations
from splitter import split_by_user
from topic_extractor import extract_topics
from sentiment_analyzer import analyze_sentiment
from overall_summary import generate_overall_sentiments

def main():
    p = argparse.ArgumentParser(description="Full conversation→topics→sentiment pipeline")
    p.add_argument(
        "-i", "--input",
        required=True,
        help="Path to raw JSON file or directory of JSON files"
    )
    p.add_argument(
        "-o", "--output",
        default="Output",
        help="Base output directory (will create subfolders under here)"
    )
    p.add_argument(
        "-t", "--topics",
        required=True,
        help="Comma-separated list of candidate topics"
    )
    p.add_argument(
        "--threshold",
        type=float,
        default=0.7,
        help="Zero-shot confidence threshold for topic hits (default: 0.7)"
    )
    args = p.parse_args()

    base_dir      = Path(args.output)
    data_dir      = base_dir / "Data"
    topics_dir    = base_dir / "Topics"
    sentiment_dir = base_dir / "Sentiment"
    overall_dir   = base_dir / "Reports"

   
    topics = [t.strip() for t in args.topics.split(",") if t.strip()]

    
    print("1) Loading raw conversations…")
    convs = load_conversations(args.input)

   
    print("2) Splitting by user…")
    split_by_user(convs, data_dir)

    
    print(f"3) Extracting topics (threshold={args.threshold})…")
    extract_topics(data_dir, topics, topics_dir, threshold=args.threshold)

  
    print("4) Analyzing sentiment…")
    analyze_sentiment(topics_dir, sentiment_dir)

   
    print("5) Generating overall‐sentiment reports…")
    generate_overall_sentiments(sentiment_dir, overall_dir)

    print("✅ Done.")

if __name__ == "__main__":
    main()
