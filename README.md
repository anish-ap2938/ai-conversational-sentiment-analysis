# ai-conversational-sentiment-analysis
# Conversation-Belief Pipeline API

This repository provides both a command-line and REST API interface to process conversational data, extract topics, analyze sentiment, and generate overall sentiment reports. It leverages Hugging Face transformers for zero-shot topic classification and sentiment analysis, and FastAPI for serving the processing pipeline as HTTP endpoints.

---

## Features

* **Data Ingestion & Splitting**: Load raw conversation JSON files and split them by user.
* **Zero-Shot Topic Extraction**: Tag messages with user-defined topics using `facebook/bart-large-mnli`.
* **Sentiment Analysis**: Perform per-message sentiment classification with `distilbert-base-uncased-finetuned-sst-2-english`.
* **Reporting**: Aggregate sentiments per topic and generate summary reports.
* **REST API**: Expose each pipeline stage and a combined endpoint via FastAPI.

---

## Repository Structure

```
project-root/
├── app.py                # FastAPI application
├── data_ingest.py        # Load raw conversations
├── splitter.py           # Split by user
├── topic_extractor.py    # Zero-shot classification
├── sentiment_analyzer.py # Sentiment analysis
├── overall_summary.py    # Aggregate and report
├── run_pipeline.py       # CLI entry point
├── requirements.txt      # Python dependencies
└── Output/               # Default output directory structure
    ├── Data/
    ├── Topics/
    ├── Sentiment/
    └── Reports/
```

---

## Prerequisites

* Python 3.8 or later
* Git
* (Optional) [Hugging Face API key](https://huggingface.co/docs/hub/security-tokens) if rate limits are a concern

---

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-org/conversation-belief-pipeline.git
   cd conversation-belief-pipeline
   ```

2. **Create and activate a virtual environment**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\\Scripts\\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

---

## Command-Line Usage

The `run_pipeline.py` script runs the full pipeline from raw conversations to reports.

```bash
python run_pipeline.py \
  --input path/to/conversations.json \
  --output Output            \
  --topics "app_usability,physical_health,emotional_wellbeing" \
  --threshold 0.7
```

This will create subfolders under `Output/`:

* `Data/` — split JSON files per user
* `Topics/` — topic-tagged messages
* `Sentiment/` — per-topic sentiment
* `Reports/` — overall sentiment summary

---

## REST API

Start the FastAPI server:

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Endpoints

* **POST `/process/all`**: Runs the full pipeline on an uploaded JSON file.
* **POST `/split`**: Splits uploaded conversations by user.
* **POST `/topics`**: Extracts topics from already-split files.
* **POST `/sentiment`**: Performs sentiment analysis.
* **POST `/reports`**: Generates overall reports.

#### Example: Full Pipeline

```bash
curl -X POST "http://localhost:8000/process/all" \
  -F "file=@path/to/conversations.json" \
  -H "Accept: application/json"
```

Response:

```json
{
  "status": "success",
  "summaries": {
    "user1_123_topics_sentiment.json": { /* detailed sentiments */ },
    …
  },
  "reports": [
    "Reports/user1_123_overall.json",
    …
  ]
}
```

---

## Testing

* Use sample JSON files under `tests/data/` to validate each stage.
* Run unit tests (if provided):

  ```bash
  pytest tests/
  ```

---

## Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feature-name`)
3. Commit your changes (`git commit -m "Add feature"`)
4. Push to your branch (`git push origin feature-name`)
5. Open a Pull Request

---

## License

This project is provided under the MIT License.
