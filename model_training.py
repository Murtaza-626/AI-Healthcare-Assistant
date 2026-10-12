import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score, top_k_accuracy_score
from xgboost import XGBClassifier
import joblib
import os
import json

# 3. Load datasets
train_df = pd.read_csv('Training.csv')
test_df = pd.read_csv('Testing.csv')

# Clean column headers of accidental spaces
train_df.columns = train_df.columns.str.strip()
test_df.columns = test_df.columns.str.strip()

# Drop unnamed/empty trailing columns if present
train_df = train_df.loc[:, ~train_df.columns.str.contains('^Unnamed')]
test_df = test_df.loc[:, ~test_df.columns.str.contains('^Unnamed')]

# Deduplicate training samples to prevent data leakage
train_df = train_df.drop_duplicates()

# 4. Feature and Target Separation
TARGET_COL = 'prognosis'
X_train = train_df.drop(columns=[TARGET_COL])
y_train_raw = train_df[TARGET_COL]

X_test = test_df.drop(columns=[TARGET_COL])
y_test_raw = test_df[TARGET_COL]

# Preserving exact feature column ordering for API ingestion
feature_names = list(X_train.columns)

# 5. Label Encoding
label_encoder = LabelEncoder()
y_train = label_encoder.fit_transform(y_train_raw)
y_test = label_encoder.transform(y_test_raw)


model = XGBClassifier(
    n_estimators=100,
    max_depth=5,
    learning_rate=0.1,
    objective='multi:softprob',
    eval_metric='mlogloss',
    random_state=42
)
model.fit(X_train, y_train)

# 7. Model Evaluation
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)

acc = accuracy_score(y_test, y_pred)
top3_acc = top_k_accuracy_score(y_test, y_proba, k=3)

print(f"Test Accuracy:       {acc * 100:.2f}%")
print(f"Top-3 Test Accuracy: {top3_acc * 100:.2f}%")
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

# 1. Setting the output directory to an 'artifacts' folder 
OUTPUT_DIR = 'artifacts'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 2. Saving the model and label encoder locally
joblib.dump(model, os.path.join(OUTPUT_DIR, 'disease_model.pkl'))
joblib.dump(label_encoder, os.path.join(OUTPUT_DIR, 'label_encoder.pkl'))


# 3. Save the symptom feature names locally as a JSON file
with open(os.path.join(OUTPUT_DIR, 'symptom_features.json'), 'w') as f:
    json.dump(feature_names, f)

print(f"\nArtifacts successfully serialized and saved to local folder: {os.path.abspath(OUTPUT_DIR)}")