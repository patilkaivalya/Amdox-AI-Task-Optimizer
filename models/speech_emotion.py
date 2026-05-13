import sounddevice as sd
import soundfile as sf
import numpy as np
import librosa
import warnings
warnings.filterwarnings("ignore")
from transformers import pipeline

# Load HuggingFace speech emotion classifier
pipe = pipeline("audio-classification",
                model="ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition")

EMOTION_MAP = {
    'angry': 'stressed',
    'calm': 'neutral',
    'disgust': 'stressed',
    'fearful': 'stressed',
    'happy': 'happy',
    'sad': 'sad',
    'surprised': 'neutral',
    'neutral': 'neutral'
}

def record_audio(duration=5, sample_rate=16000):
    """Record audio from microphone and save to temp file."""
    recording = sd.rec(int(duration * sample_rate),
                       samplerate=sample_rate, channels=1, dtype='float32')
    sd.wait()
    sf.write('temp_audio.wav', recording, sample_rate)
    return 'temp_audio.wav'

def analyze_speech(file_path=None, duration=5):
    """Analyze speech emotion from file or by recording."""
    if file_path is None:
        file_path = record_audio(duration)
    try:
        result = pipe(file_path)
        # result is list of dicts with 'label' and 'score'
        top = result[0]
        emotion_label = top['label']
        confidence = top['score']
        mood = EMOTION_MAP.get(emotion_label, 'neutral')
        # stress: high for negative emotions
        stress = 0.8 if emotion_label in ['angry', 'fearful', 'sad', 'disgust'] else 0.3
        return mood, stress, confidence
    except Exception as e:
        return 'unknown', 0.0, 0.0