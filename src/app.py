import pandas as pd
from flask import Flask, request, jsonify
import joblib
import gdown
from libml import preprocessing as libml
from flasgger import Swagger
from pandas import DataFrame
from sklearn.feature_extraction.text import CountVectorizer

app = Flask(__name__)
swagger = Swagger(app)


def download_and_load_model(google_drive_url, download_path, model_filename):
    """
    Download a model from Google Drive and load it using joblib.

    :param google_drive_url: URL of the Google Drive file to download
    :param download_path: Path to save the downloaded model file
    :param model_filename: Name of the file to save the model as (e.g. 'model.pkl')
    :return: Loaded model object
    """
    # Download the model file directly from Google Drive
    downloaded_file = gdown.download(google_drive_url, f"{download_path}/{model_filename}", quiet=False, fuzzy=True)
    print(f"Downloaded file: {downloaded_file}")

    # Load the model using joblib
    model = joblib.load(f"{download_path}/{model_filename}")

    return model


# URLs for both models
cv_url = "https://drive.google.com/file/d/14bCZu2mMU_90ngZLDXyQh9fQCbqDW0E-/view?usp=sharing"
model_url = "https://drive.google.com/file/d/1F6i--L50pVm7p0dcApGIhepC7CovC3La/view?usp=sharing"

# Download and load the models
cv = download_and_load_model(cv_url, download_path="../output", model_filename="cv.pkl")
model = download_and_load_model(model_url, download_path="../output", model_filename="model.pkl")




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
            - review
          properties:
            review:
              type: string
              example: "This product was amazing, I loved it!"
    responses:
      200:
        description: The result of the sentiment prediction.
        schema:
          type: object
          properties:
            sentiment:
              type: integer
              example: 1
    """
    data = request.get_json()
    review_text = data.get("review", "")
    print([review_text])
    review_df = pd.DataFrame({"Review": [review_text]})
    review_vector, _ = libml._preprocess(review_df, cv)
    prediction = model.predict(review_vector)[0]
    return jsonify({"sentiment": int(prediction)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)