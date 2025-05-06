import os

import gdown
import joblib
import pandas as pd
from dotenv import load_dotenv
from flasgger import Swagger
from flask import Flask, jsonify, request
from libml import preprocessing as libml
from pandas import DataFrame
from sklearn.feature_extraction.text import CountVectorizer

load_dotenv()

app = Flask(__name__)
swagger = Swagger(app)

MODEL_DIR = "/models"


def download_and_load_model(google_drive_url, download_path, model_filename):
    """
    Download a model from Google Drive and load it using joblib.

    :param google_drive_url: URL of the Google Drive file to download
    :param download_path: Path to save the downloaded model file
    :param model_filename: Name of the file to save the model as (e.g. 'model.pkl')
    :return: Loaded model object
    """
    os.makedirs(download_path, exist_ok=True)
    model_filepath = os.path.join(download_path, model_filename)

    if not os.path.exists(model_filepath):
        print(f"File not found locally. Downloading: {model_filename}")
        gdown.download(google_drive_url, model_filepath, quiet=False, fuzzy=True)
    else:
        print(f"File already exists: {model_filepath}, skipping download.")

    model = joblib.load(model_filepath)
    return model


# URLs for both models
cv_url = os.getenv(
    "CV_URI",
    "https://drive.google.com/file/d/14bCZu2mMU_90ngZLDXyQh9fQCbqDW0E-/view?usp=sharing",
)
model_url = os.getenv(
    "MODEL_RESOURCE_URI",
    "https://drive.google.com/file/d/1F6i--L50pVm7p0dcApGIhepC7CovC3La/view?usp=sharing",
)

# Download and load the models
cv = download_and_load_model(cv_url, download_path=MODEL_DIR, model_filename="cv.pkl")
model = download_and_load_model(
    model_url, download_path=MODEL_DIR, model_filename="model.pkl"
)


@app.route("/predict", methods=["POST"])
def predict():
    """
    Predict the sentiment of a review.
    ---
    consumes:
      - application/json
    parameters:
      - in: body
        name: input_data
        required: true
        schema:
          type: object
          required:
            - text
          properties:
            text:
              type: string
              example: "This product was amazing, I loved it!"
    responses:
      200:
        description: The result of the sentiment prediction.
        schema:
          type: object
          properties:
            prediction:
              type: integer
              example: 1
    """
    data = request.get_json()
    review_text = data.get("text", "")
    print([review_text])
    review_df = pd.DataFrame({"Review": [review_text]})
    review_vector, _ = libml._preprocess(review_df, cv)
    prediction = model.predict(review_vector)[0]
    return jsonify({"prediction": round(prediction)})


@app.route("/version", methods=["GET"])
def version():
    """
    Return the version of the model
    ---
    responses:
      200:
        description: The version of the model.
        schema:
          type: object
          properties:
            version:
              type: string
    """
    return jsonify({"version": "v1.0"})


if __name__ == "__main__":
    debug = os.getenv("DEBUG", True)
    port = os.getenv("PORT", 5001)
    app.run(host="0.0.0.0", port=port, debug=debug)
