import joblib
from sklearn.tree import DecisionTreeClassifier

# Simple dataset: [impact, vibration, distance]
X = [
    [12,1,8],  # accident
    [5,0,50],  # normal
    [14,1,6],  # accident
    [4,0,80]   # normal
]

y = [1,0,1,0]  # 1=Accident, 0=Normal

model = DecisionTreeClassifier()
model.fit(X, y)

# Save model
joblib.dump(model, 'accident_model.pkl')
print("Model trained and saved!")
