# model-service

Model-service exposes a REST API that predicts the sentiment of restaurant reviews using a pre-trained machine learning model. It uses Flask, Flasgger for Swagger UI, and integrates preprocessing from the [`libml`](https://github.com/remla25-team15/lib-ml) library.

---

## Environment Configuration

The service supports environment variables for flexible deployments:

| Variable     | Default      | Description                                        |
|--------------|--------------|----------------------------------------------------|
| `DEBUG`      | `true`       | Run Flask in debug mode                           |
| `PORT`       | `5001`       | Port the service listens on                       |
| `FLASK_ENV`  | `production` | Flask environment (`production` or `development`) |

---

## Setup Instructions

### 1. Launch a Bash session in the container

```bash
docker run -it --rm -v ./:/app/model-service/ python:3.12.9-slim bash
```

### 2. Run the model from inside the container

```bash
docker run -it --rm -p 8080:5001 model-service
```

---

## API Usage

### Endpoint: `POST /predict`

#### Example Request

```json
{
  "text": "This restaurant was excellent and the staff was very friendly."
}
```

#### Example Response

```json
{
  "prediction": 1
}
```

---

## Model Artifacts

At runtime, the service downloads and loads two files from Google Drive:

* `model.pkl`: Trained classifier
* `cv.pkl`: CountVectorizer used during training

---

## Service Details

* Preprocessing logic is sourced from the shared [`libml`](https://github.com/remla25-team15/lib-ml) repository.
* Dockerized builds are intended to be released via GitHub Actions (`release.yml`).
* The service includes a Swagger UI at `/apidocs` when accessed in the browser.

---

## Testing

To test the service manually with `curl`:

```bash
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "Very slow service but the food was great"}'
```
