# model.py
# Train a Random Forest model to detect phishing URLs

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib  # for saving the trained model

# ── Step 1: Load the dataset ─────────────────────────────
df = pd.read_csv('dataset.csv')
print("Dataset loaded! Shape:", df.shape)

# ── Step 2: Separate features (X) and label (y) ──────────
# X = all columns EXCEPT 'label'  (the inputs)
# y = only the 'label' column     (the answer we want to predict)
X = df.drop('label', axis=1)
y = df['label']

print("\nFeatures (X):", list(X.columns))
print("Label (y): label (0 = safe, 1 = phishing)")

# ── Step 3: Split into training and testing sets ─────────
# 80% data to train the model, 20% to test how well it learned
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"\nTraining samples: {len(X_train)}")
print(f"Testing samples: {len(X_test)}")

# ── Step 4: Create and train the Random Forest model ─────
# n_estimators = number of "trees" in the forest
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

print("\nModel trained successfully!")

# ── Step 5: Test the model ────────────────────────────────
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print(f"\nAccuracy on test data: {accuracy * 100:.2f}%")

# ── Step 6: Show which features matter most ──────────────
importance = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print("\nFeature Importance (which clues matter most):")
print(importance)

# ── Step 7: Save the trained model to a file ──────────────
joblib.dump(model, 'phishing_model.pkl')
print("\nModel saved as 'phishing_model.pkl'")