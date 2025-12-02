from flask import Flask, request, jsonify
from flask_cors import CORS
import re
from textblob import TextBlob
import os

app = Flask(__name__)
CORS(app)

# Toxic words database (expandable)
TOXIC_WORDS = {
    'hate', 'kill', 'stupid', 'idiot', 'dumb', 'trash', 'garbage',
    'worst', 'terrible', 'awful', 'disgusting', 'pathetic'
}

SPAM_PATTERNS = [
    r'(click here|buy now|limited offer|act now)',
    r'(\$\$\$|💰|🤑)',
    r'(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+){3,}'
]

class ContentModerator:
    def __init__(self):
        self.toxic_words = TOXIC_WORDS
        self.spam_patterns = SPAM_PATTERNS
    
    def analyze_toxicity(self, text):
        """Analyze text for toxic content"""
        text_lower = text.lower()
        toxic_found = [word for word in self.toxic_words if word in text_lower]
        toxicity_score = len(toxic_found) / max(len(text.split()), 1)
        
        return {
            'is_toxic': len(toxic_found) > 0,
            'toxicity_score': min(toxicity_score * 100, 100),
            'toxic_words_found': toxic_found
        }
    
    def analyze_spam(self, text):
        """Detect spam patterns"""
        spam_matches = []
        for pattern in self.spam_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                spam_matches.append(pattern)
        
        return {
            'is_spam': len(spam_matches) > 0,
            'spam_score': min(len(spam_matches) * 30, 100),
            'patterns_matched': len(spam_matches)
        }
    
    def analyze_sentiment(self, text):
        """Analyze sentiment polarity"""
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        
        if polarity > 0.1:
            sentiment = 'positive'
        elif polarity < -0.1:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        return {
            'sentiment': sentiment,
            'polarity': polarity,
            'subjectivity': blob.sentiment.subjectivity
        }
    
    def moderate(self, text):
        """Complete moderation analysis"""
        if not text or len(text.strip()) == 0:
            return {'error': 'Empty text provided'}
        
        toxicity = self.analyze_toxicity(text)
        spam = self.analyze_spam(text)
        sentiment = self.analyze_sentiment(text)
        
        # Overall safety score
        safety_score = 100 - (toxicity['toxicity_score'] * 0.6 + spam['spam_score'] * 0.4)
        
        return {
            'text': text,
            'safe': safety_score > 70,
            'safety_score': round(safety_score, 2),
            'toxicity': toxicity,
            'spam': spam,
            'sentiment': sentiment,
            'recommendation': 'approve' if safety_score > 70 else 'review' if safety_score > 40 else 'reject'
        }

moderator = ContentModerator()

@app.route('/')
def home():
    return jsonify({
        'service': 'AI Content Moderator API',
        'version': '1.0.0',
        'endpoints': {
            '/moderate': 'POST - Moderate content',
            '/health': 'GET - Health check'
        }
    })

@app.route('/moderate', methods=['POST'])
def moderate_content():
    """Moderate content endpoint"""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'Missing text field'}), 400
        
        result = moderator.moderate(data['text'])
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'content-moderator'}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
