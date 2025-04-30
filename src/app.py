from flask import Flask, request, jsonify
import joblib
from libml.preprocessing import get_vectorizer

app = Flask(__name__)
model = joblib.load("model.joblib")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    review = data.get("review", "")
    prediction = model.predict([review])[0]
    return jsonify({"sentiment": int(prediction)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)