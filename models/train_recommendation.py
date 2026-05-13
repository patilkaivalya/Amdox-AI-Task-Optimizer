import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# Generate synthetic training data for task recommendation
np.random.seed(42)
n = 1000
moods = ['happy', 'neutral', 'sad', 'stressed', 'tired', 'focused']
task_types = ['creative', 'analytical', 'light', 'break', 'routine', 'collaborative']

data = {
    'mood': np.random.choice(moods, n),
    'stress_level': np.random.uniform(0,1,n),
    'productivity_score': np.random.uniform(0,1,n),
}
df = pd.DataFrame(data)

# Rule-based task assignment to create targets
def assign_task(row):
    if row['stress_level'] > 0.7: return 'break'
    if row['mood'] == 'happy': return np.random.choice(['creative','collaborative'])
    if row['mood'] == 'focused': return 'analytical'
    if row['mood'] in ['sad','tired']: return 'light'
    if row['mood'] == 'stressed': return 'break'
    return 'routine'

df['task'] = df.apply(assign_task, axis=1)

# Encoding
mood_map = {'happy':0, 'neutral':1, 'sad':2, 'stressed':3, 'tired':4, 'focused':5}
df['mood_code'] = df['mood'].map(mood_map)
X = df[['mood_code', 'stress_level', 'productivity_score']]
y = df['task']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))

joblib.dump(clf, 'models/recommendation_model.pkl')
print("Model saved as recommendation_model.pkl")