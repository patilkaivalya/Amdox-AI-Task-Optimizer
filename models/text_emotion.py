from transformers import pipeline
import nltk
nltk.download('punkt', quiet=True)

# Use a robust sentiment model
sentiment_pipeline = pipeline("sentiment-analysis",
                              model="distilbert-base-uncased-finetuned-sst-2-english",
                              return_all_scores=True)

MOOD_MAP = {
    'POSITIVE': 'happy',
    'NEGATIVE': 'sad',
    'NEUTRAL': 'neutral'
}

def analyze_text(text):
    """Return predicted mood and confidence."""
    if not text.strip():
        return 'neutral', 0.0
    results = sentiment_pipeline(text[:512])[0]  # truncate long texts
    # results: list of {'label': 'POSITIVE', 'score': ...}, etc.
    # Find highest score
    best = max(results, key=lambda x: x['score'])
    label = best['label']
    mood = MOOD_MAP.get(label, 'neutral')
    # For stress estimation: negative sentiment => higher stress
    stress = 0.8 if label == 'NEGATIVE' else 0.3 if label == 'NEUTRAL' else 0.1
    return mood, stress, best['score']