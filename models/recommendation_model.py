import joblib
import numpy as np

# Load trained model (if exists)
try:
    model = joblib.load('models/recommendation_model.pkl')
except:
    model = None

TASK_POOL = {
    'happy': ['Creative Brainstorming', 'Team Collaboration', 'Client Presentation'],
    'focused': ['Data Analysis', 'Code Review', 'Report Writing'],
    'neutral': ['Email Management', 'Meeting Preparation', 'Documentation'],
    'sad': ['Light Reading', 'Training Videos', 'Routine Tasks'],
    'stressed': ['Low-priority Admin', 'Break/Wellness Activity', 'Reflection Notes'],
    'tired': ['Rest Break', 'Stretching Exercise', 'Non-critical Tasks']
}

def recommend_task(mood, stress_level, productivity_score=0.5, employee_id=None):
    """
    Recommend a task based on mood, stress, and productivity.
    If ML model available, use it; else rule-based fallback.
    """
    if model is not None:
        features = encode_features(mood, stress_level, productivity_score)
        task_type = model.predict([features])[0]
        return pick_from_pool(task_type)

    # Rule-based
    if stress_level >= 0.75:
        return np.random.choice(TASK_POOL['stressed'])
    if mood in ['sad', 'tired']:
        return np.random.choice(TASK_POOL['tired'] if mood == 'tired' else TASK_POOL['sad'])
    if mood == 'happy':
        return np.random.choice(TASK_POOL['happy'])
    if mood == 'focused':
        return np.random.choice(TASK_POOL['focused'])
    return np.random.choice(TASK_POOL['neutral'])

def encode_features(mood, stress, prod):
    mood_map = {'happy':0, 'neutral':1, 'sad':2, 'stressed':3, 'tired':4, 'focused':5}
    return [mood_map.get(mood, 1), stress, prod]

def pick_from_pool(task_type):
    return np.random.choice(TASK_POOL.get(task_type, TASK_POOL['neutral']))