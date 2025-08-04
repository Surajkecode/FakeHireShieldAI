import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.utils import resample
from sklearn.pipeline import Pipeline
import joblib

# 1. Load CSV
df = pd.read_csv("fake_job_postings.csv")  # change filename if different

# 2. Drop missing values in key text fields
df.dropna(subset=["description", "requirements", "benefits"], inplace=True)

# 3. Combine text features
df["text"] = df["title"].fillna('') + " " + df["description"] + " " + df["requirements"] + " " + df["benefits"]

# 4. Keep only needed columns
df = df[["text", "fraudulent"]]

# 5. Upsample minority class (fraudulent = 1)
df_majority = df[df.fraudulent == 0]
df_minority = df[df.fraudulent == 1]

df_minority_upsampled = resample(
    df_minority,
    replace=True,
    n_samples=len(df_majority),
    random_state=42
)

df_balanced = pd.concat([df_majority, df_minority_upsampled])

# 6. Split dataset
X = df_balanced["text"]
y = df_balanced["fraudulent"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 7. Define pipeline
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(stop_words='english', max_features=5000)),
    ("clf", RandomForestClassifier(n_estimators=100, random_state=42))
])

# 8. Train model
pipeline.fit(X_train, y_train)

# 9. Evaluate
y_pred = pipeline.predict(X_test)

print("Classification Report:")
print(classification_report(y_test, y_pred))

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# 10. Save model
joblib.dump(pipeline, "job_fraud_detector.pkl")
print("Model saved as job_fraud_detector.pkl")
