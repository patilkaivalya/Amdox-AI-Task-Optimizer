# models/facial_emotion.py
import cv2
import numpy as np
from PIL import Image
from transformers import pipeline

# Map model labels → project mood categories
EMOTION_TO_MOOD = {
    'happy': 'happy',
    'sad': 'sad',
    'angry': 'stressed',
    'fear': 'stressed',
    'surprise': 'neutral',
    'neutral': 'neutral',
    'disgust': 'stressed'
}

# Load the pipeline once (it downloads the model on first run)
face_emotion_pipeline = pipeline(
    "image-classification",
    model="trpakov/vit-face-expression",
    top_k=1
)

def analyze_face(frame_bgr):
    """
    Detect emotion from a BGR frame (numpy array).
    Returns (mood, stress, confidence).
    """
    if frame_bgr is None:
        return 'unknown', 0.0, 0.0

    # Convert BGR (OpenCV) to RGB (PIL)
    frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(frame_rgb)

    try:
        result = face_emotion_pipeline(pil_image)
        # result is a list, e.g. [{'label': 'happy', 'score': 0.987}]
        label = result[0]['label']
        confidence = result[0]['score']

        mood = EMOTION_TO_MOOD.get(label, 'neutral')

        # Estimate stress based on emotion
        if label in ['angry', 'fear', 'sad', 'disgust']:
            stress = 0.8
        elif label == 'neutral':
            stress = 0.4
        else:
            stress = 0.2

        return mood, stress, confidence
    except Exception as e:
        print(f"Facial analysis error: {e}")
        return 'unknown', 0.0, 0.0