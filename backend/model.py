# model.py — Train on real 11,054 URL dataset

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# ── Step 1: Load real dataset ─────────────────────────────
df = pd.read_csv('phishing.csv')
print(f"Dataset loaded! Shape: {df.shape}")

# ── Step 2: Prepare features and label ───────────────────
# Drop 'Index' column (not useful)
# 'class' = -1 (phishing), 1 (legitimate)
X = df.drop(['Index', 'class'], axis=1)
y = df['class']

print(f"Features: {list(X.columns)}")
print(f"Phishing: {(y == -1).sum()}, Legitimate: {(y == 1).sum()}")

# ── Step 3: Train/Test split ──────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"\nTraining samples: {len(X_train)}")
print(f"Testing samples : {len(X_test)}")

# ── Step 4: Train Random Forest ───────────────────────────
model = RandomForestClassifier(
    n_estimators=200,      # 200 trees — more = better accuracy
    max_depth=None,        # Let trees grow fully
    min_samples_split=2,
    random_state=42,
    n_jobs=-1              # Use all CPU cores
)

print("\nTraining model... (may take 30-60 seconds)")
model.fit(X_train, y_train)
print("Training complete!")

# ── Step 5: Test accuracy ─────────────────────────────────
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print(f"\n{'='*45}")
print(f"ACCURACY: {accuracy * 100:.2f}%")
print(f"{'='*45}")
print("\nDetailed Report:")
print(classification_report(y_test, predictions,
      target_names=['Phishing', 'Legitimate']))

# ── Step 6: Feature importance ────────────────────────────
importance = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print("\nTop 10 Most Important Features:")
print(importance.head(10).to_string(index=False))

# ── Step 7: Save model ────────────────────────────────────
joblib.dump(model, 'phishing_model.pkl')
joblib.dump(list(X.columns), 'model_features.pkl')  # Save feature names too!
print("\nModel saved as 'phishing_model.pkl'")
print("Features saved as 'model_features.pkl'")