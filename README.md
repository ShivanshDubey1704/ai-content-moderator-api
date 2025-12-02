# 🛡️ AI Content Moderator API

An intelligent content moderation API that uses NLP to detect toxic content, spam, and analyze sentiment in real-time.

## Features

- **Toxicity Detection**: Identifies harmful and offensive language
- **Spam Detection**: Recognizes spam patterns and promotional content
- **Sentiment Analysis**: Analyzes emotional tone (positive/negative/neutral)
- **Safety Scoring**: Provides overall content safety score
- **Automated Recommendations**: Suggests approve/review/reject actions

## Installation

```bash
pip install -r requirements.txt
python -m textblob.download_corpora
```

## Usage

```bash
python app.py
```

## API Endpoints

### POST /moderate
Analyze and moderate content

**Request:**
```json
{
  "text": "Your content here"
}
```

**Response:**
```json
{
  "text": "Your content here",
  "safe": true,
  "safety_score": 85.5,
  "toxicity": {
    "is_toxic": false,
    "toxicity_score": 0,
    "toxic_words_found": []
  },
  "spam": {
    "is_spam": false,
    "spam_score": 0,
    "patterns_matched": 0
  },
  "sentiment": {
    "sentiment": "positive",
    "polarity": 0.5,
    "subjectivity": 0.6
  },
  "recommendation": "approve"
}
```

## Tech Stack

- Flask
- TextBlob (NLP)
- Python 3.8+

## Author

Shivansh Dubey
