print("App started")

from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

model = pickle.load(open("models/model.pkl", "rb"))
vectorizer = pickle.load(open("models/vectorizer.pkl", "rb"))


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    tweet = request.form["tweet"]
    transformed = vectorizer.transform([tweet])

    probs = model.predict_proba(transformed)[0]

    positive = probs[1] * 100
    negative = probs[0] * 100

    confidence = max(positive, negative)

    # ✅ FIX: Neutral is derived safely (NO NEGATIVE / NO ZERO BUG)
    neutral = 100 - (positive + negative)

    if neutral < 0:
        neutral = 0

    # 🎯 Sentiment logic (stable)
    if confidence < 55:
        result = "Neutral 😐"
        color = "#ffb300"
    elif positive > negative:
        result = "Positive 😊"
        color = "#00c853"
    else:
        result = "Negative 😞"
        color = "#ff5252"

    # rounding
    positive = round(positive, 2)
    negative = round(negative, 2)
    neutral = round(neutral, 2)
    confidence = round(confidence, 2)

    return render_template(
        "index.html",
        tweet=tweet,
        prediction=result,
        confidence=confidence,
        positive=positive,
        negative=negative,
        neutral=neutral,
        color=color
    )


if __name__ == "__main__":
    app.run(debug=True)