import pandas as pd
import re
import pickle

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Load dataset
columns = ["target", "id", "date", "flag", "user", "text"]

df = pd.read_csv(
    "data/tweets.csv",
    encoding="latin-1",
    names=columns
)

# Keep only sentiment and text
df = df[["target", "text"]]

# Convert labels
df["target"] = df["target"].replace(4, 1)

# Use smaller sample for faster training
df = df.sample(n=50000, random_state=42)

# Clean text
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\\S+", "", text)
    text = re.sub(r"@\\w+", "", text)
    text = re.sub(r"[^a-zA-Z ]", "", text)
    return text

df["text"] = df["text"].apply(clean_text)

# Features and labels
X = df["text"]
y = df["target"]

# TF-IDF
vectorizer = TfidfVectorizer(max_features=5000)

X = vectorizer.fit_transform(X)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

# Train model
model = LogisticRegression()

model.fit(X_train, y_train)

# Predict
predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("Accuracy:", accuracy)

# Save model
pickle.dump(model, open("models/model.pkl", "wb"))
pickle.dump(vectorizer, open("models/vectorizer.pkl", "wb"))

print("Model saved successfully!")