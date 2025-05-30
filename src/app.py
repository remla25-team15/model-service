import os
import urllib.parse
import urllib.request

import joblib
import pandas as pd
from dotenv import load_dotenv
from flasgger import Swagger
from flask import Flask, jsonify, request
from libml import preprocessing as libml
from pandas import DataFrame
from sklearn.feature_extraction.text import CountVectorizer
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

load_dotenv()

MODEL_DIR = "/models"

MODEL_VERSION = os.getenv("MODEL_VERSION", "v1.1.0")

RESOURCE_BASE_URL = os.getenv(
    "RESOURCE_BASE_URL",
    "https://github.com/remla25-team15/model-training/releases/download/",
)

app = Flask(__name__)
swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Sentiment Analysis API",
        "description": "API for predicting sentiment of text reviews",
        "version": MODEL_VERSION,
    },
    "basePath": "/model",
    "schemes": ["http"],
    "consumes": ["application/json"],
    "produces": ["application/json"],
}
swagger = Swagger(app, template=swagger_template)


def download_and_load_model(resource_url, download_path, model_filename):
    """
    Download a model from the given URL and load it using joblib.

    :param resource_url: URL of the file to download
    :param download_path: Path to save the downloaded model file
    :param model_filename: Name of the file to save the model as (e.g. 'model.pkl')
    :return: Loaded model object
    """
    os.makedirs(download_path, exist_ok=True)
    model_filepath = os.path.join(download_path, model_filename)

    if not os.path.exists(model_filepath):
        print(
            f"File {model_filepath} not found locally. Downloading: {model_filename} from {resource_url}"
        )
        urllib.request.urlretrieve(resource_url, model_filepath)
    else:
        print(f"File already exists: {model_filepath}, skipping download.")

    return joblib.load(model_filepath)


CV_FILE_NAME = os.getenv("CV_FILE_NAME", "c1_BoW_Sentiment_Model.pkl")
MODEL_FILE_NAME = os.getenv("MODEL_FILE_NAME", "c2_Classifier_Sentiment_Model.pkl")

# Build URLs for both models
cv_url = urllib.parse.urljoin(RESOURCE_BASE_URL, f"{MODEL_VERSION}/{CV_FILE_NAME}")

model_url = urllib.parse.urljoin(
    RESOURCE_BASE_URL, f"{MODEL_VERSION}/{MODEL_FILE_NAME}"
)

# Download and load the models
cv = download_and_load_model(
    cv_url,
    download_path=os.path.join(MODEL_DIR, MODEL_VERSION),
    model_filename="cv.pkl",
)
model = download_and_load_model(
    model_url,
    download_path=os.path.join(MODEL_DIR, MODEL_VERSION),
    model_filename="model.pkl",
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
    return jsonify({"version": f"{MODEL_VERSION}"})


if __name__ == "__main__":
    debug = os.getenv("DEBUG", True)
    port = int(os.getenv("PORT", 5001))

    application = DispatcherMiddleware(Flask("dummy"), {"/model": app})
    run_simple("0.0.0.0", port, application, use_reloader=True, use_debugger=True)
    # app.run(host="0.0.0.0", port=port, debug=debug)
