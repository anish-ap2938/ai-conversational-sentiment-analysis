import json
import tempfile
import traceback
from pathlib import Path

from fastapi import FastAPI, HTTPException, UploadFile, File

from data_ingest import load_conversations
from splitter import split_by_user
from topic_extractor import extract_topics
from sentiment_analyzer import analyze_sentiment
from overall_summary import generate_overall_sentiments  # newly added

BASE          = Path("Output")
DATA_DIR      = BASE / "Data"
TOPICS_DIR    = BASE / "Topics"
SENTIMENT_DIR = BASE / "Sentiment"
REPORTS_DIR   = BASE / "Reports"   # newly added

CANDIDATE_TOPICS = [
    "app_usability",
    "technical_support",
    "physical_health",
    "emotional_wellbeing",
    "family_relationships",
    "social_support",
    "virtual_socializing",
    "hobbies_and_interests",
    "fitness_and_motivation",
    "mindfulness_and_gratitude",
    "life_purpose"
]

app = FastAPI(title="Conversation-Belief Pipeline API")

def main_pipeline(input_path: str):
    # 1) load + split
    convs = load_conversations(input_path)
    split_by_user(convs, DATA_DIR)

    # 2) multi-label topic extraction 
    extract_topics(DATA_DIR, CANDIDATE_TOPICS, TOPICS_DIR, threshold=0.7)

    # 3) per-message sentiment + aggregation
    analyze_sentiment(TOPICS_DIR, SENTIMENT_DIR)

    # 4) generate lean overall‐sentiment reports
    generate_overall_sentiments(SENTIMENT_DIR, REPORTS_DIR)

    # 5) collect and return full sentiment summaries
    out = {}
    for f in sorted(SENTIMENT_DIR.glob("*.json")):
        out[f.name] = json.loads(f.read_text(encoding="utf-8"))
    return out

@app.post("/process/all")
async def process_all(file: UploadFile = File(...)):
    raw = await file.read()
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
        tmp.write(raw)
        tmp_path = tmp.name

    try:
        summaries = main_pipeline(tmp_path)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(400, str(e))

    return {
        "status": "success",
        "summaries": summaries,
        "reports": [str(p.relative_to(BASE)) for p in REPORTS_DIR.glob("*.json")]
    }

@app.post("/split")
async def api_split(file: UploadFile = File(...)):
    raw = await file.read()
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
        tmp.write(raw)
        tmp_path = tmp.name

    convs = load_conversations(tmp_path)
    split_by_user(convs, DATA_DIR)
    return {
        "data_files": [str(p.relative_to(BASE)) for p in DATA_DIR.glob("*.json")]
    }

@app.post("/topics")
async def api_topics():
    extract_topics(DATA_DIR, CANDIDATE_TOPICS, TOPICS_DIR, threshold=0.7)
    return {
        "topic_files": [str(p.relative_to(BASE)) for p in TOPICS_DIR.glob("*.json")]
    }

@app.post("/sentiment")
async def api_sentiment():
    analyze_sentiment(TOPICS_DIR, SENTIMENT_DIR)
    return {
        "sentiment_files": [str(p.relative_to(BASE)) for p in SENTIMENT_DIR.glob("*.json")]
    }

@app.post("/reports")
async def api_reports():
    # regenerate Reports folder
    generate_overall_sentiments(SENTIMENT_DIR, REPORTS_DIR)
    return {
        "report_files": [str(p.relative_to(BASE)) for p in REPORTS_DIR.glob("*.json")]
    }
