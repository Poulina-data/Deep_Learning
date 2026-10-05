# CIFAR Vision: CIFAR-10 Image Classification Web App

A production-grade Flask web application for classifying images using a trained CIFAR-10 Artificial Neural Network (ANN).

![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.x-green.svg)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.10%2B-orange.svg)
![Architecture](https://img.shields.io/badge/Model-ANN%20(Dense)-purple.svg)

---

## 1. Overview

**CIFAR Vision** provides a modern, responsive, and secure inference interface for an existing trained CIFAR-10 neural network model. The application adheres to strict software design principles with an Application Factory pattern, Blueprint modularity, robust image validation, graceful error handling, and test coverage.

### Key Capabilities
- **Drag & Drop Upload:** Accepts PNG, JPG, JPEG, and WEBP formats up to 5 MB.
- **Immediate Live Preview:** Previews user images with resolution and file metadata before classification.
- **One-Click Quick Test Gallery:** 10 authentic CIFAR-10 sample test images embedded directly in the dashboard for instant evaluation.
- **Top Predictions & Probabilities:** Dynamic visual progress bars depicting the top 3 predicted classes with percentage confidence.
- **Seamless Session Reset:** Clear button resets UI state without requiring a browser refresh.
- **Robust Security:** MIME/Pillow validation, max payload enforcement, secure filename handling, and no stack trace leaks.

---

## 2. Model Architecture

The application strictly utilizes the exact trained CIFAR-10 Artificial Neural Network (ANN) specified in `CIFAR10_classification.ipynb`:

```python
model = Sequential([
    Flatten(input_shape=(32, 32, 3)),
    Dense(512, activation="relu"),
    Dense(256, activation="relu"),
    Dense(10, activation="softmax")
])
```

- **Input Dimension:** `(batch_size, 32, 32, 3)`
- **Hidden Layers:** Dense (512 units, ReLU) $\rightarrow$ Dense (256 units, ReLU)
- **Output:** Dense (10 units, Softmax probabilities)
- **Preprocessing Pipeline:**
  $$\text{RGB Image} \longrightarrow \text{Resize to } 32\times32 \longrightarrow \text{float32} \longrightarrow \frac{X}{255.0} \longrightarrow \text{Tensor } (1, 32, 32, 3)$$

> **Important Note:** This is an **ANN** (Fully Connected Network), not a Convolutional Neural Network (CNN). Model weights are loaded once at server startup and cached as a singleton for fast sub-50ms inference.

---

## 3. CIFAR-10 Classes

Predictions correspond to the 10 standard CIFAR-10 labels:

| Index | Label | Icon |
|:---:|:---|:---:|
| `0` | airplane | ✈️ |
| `1` | automobile | 🚗 |
| `2` | bird | 🐦 |
| `3` | cat | 🐱 |
| `4` | deer | 🦌 |
| `5` | dog | 🐶 |
| `6` | frog | 🐸 |
| `7` | horse | 🐴 |
| `8` | ship | 🚢 |
| `9` | truck | 🚚 |

---

## 4. Project Structure

```text
cifar_webapp/
├── app/
│   ├── __init__.py           # Application factory & error handlers
│   ├── routes.py             # Blueprint routes (/, /predict, /clear, /health)
│   ├── config.py             # Config classes & environment variable loaders
│   ├── services/
│   │   ├── __init__.py
│   │   └── predictor.py      # Model loading, validation & inference service
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── image_utils.py    # Pillow preprocessing & array conversion
│   │   └── validators.py     # File validation & size bounds
│   ├── templates/
│   │   ├── base.html         # Base layout with ambient dark theme
│   │   ├── index.html        # Main interactive AI dashboard
│   │   └── error.html        # Friendly error view
│   └── static/
│       ├── css/style.css     # Design system, glassmorphism, responsive grid
│       ├── js/app.js         # Client async fetch, drag-drop, preview & clear
│       └── images/
│           ├── favicon.svg   # Custom SVG icon
│           └── samples/      # 10 test CIFAR-10 images
├── models/
│   ├── cifar10_model.h5      # Trained ANN model (H5 format)
│   └── cifar10_model.keras   # Trained ANN model (Keras format)
├── uploads/
│   └── .gitkeep              # Temporary upload directory
├── tests/
│   ├── __init__.py
│   ├── test_image_utils.py   # Preprocessing & validator unit tests
│   ├── test_predictor.py     # Inference & model shape tests
│   └── test_routes.py        # Flask API integration tests
├── .env                      # Local configuration
├── .env.example              # Example environment template
├── .gitignore
├── requirements.txt          # Python dependencies
├── config.py                 # Root configuration proxy
├── run.py                    # Local development runner
├── wsgi.py                   # Production WSGI entry point
├── Dockerfile                # Container definition
├── .dockerignore
└── README.md
```

---

## 5. Installation & Setup

### Prerequisites
- Python 3.10+
- pip

### 1. Clone & Navigate
```bash
cd cifar_webapp
```

### 2. Create Virtual Environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
cp .env.example .env
```

---

## 6. Running Locally

Start the development server with live reload:

```bash
python run.py
```

The application will start at:
👉 **http://127.0.0.1:5000**

---

## 7. API Endpoints

### `GET /`
Renders the interactive AI dashboard.

### `GET /health`
Returns JSON status of the server and model:
```json
{
  "model_online": true,
  "model_path": "cifar10_model.h5",
  "service": "CIFAR-10 ANN Classifier",
  "status": "healthy"
}
```

### `POST /predict`
Performs classification on an uploaded image or sample image.

**Request Options:**
1. **Multipart Form-Data:**
   - Field `file`: Image file (`.png`, `.jpg`, `.jpeg`, `.webp`, $\le 5$ MB).
2. **JSON Payload:**
   ```json
   { "sample_name": "cat_sample.png" }
   ```

**Successful Response (200 OK):**
```json
{
  "success": true,
  "prediction": {
    "class_index": 3,
    "class_name": "cat",
    "confidence": 87.42,
    "inference_time_ms": 12.3,
    "input_shape": "32 × 32 × 3",
    "model_type": "CIFAR-10 ANN",
    "top_predictions": [
      { "class_index": 3, "class_name": "cat", "confidence": 87.42 },
      { "class_index": 5, "class_name": "dog", "confidence": 6.21 },
      { "class_index": 4, "class_name": "deer", "confidence": 2.83 }
    ],
    "probabilities": {
      "airplane": 0.0012,
      "automobile": 0.0024,
      "cat": 0.8742
    }
  }
}
```

### `POST /clear`
Resets the interface and session state:
```json
{
  "message": "Application state reset successfully.",
  "success": true
}
```

---

## 8. Running Automated Tests

Run the complete test suite with `pytest`:

```bash
pytest -v
```

This verifies:
- Validation logic on valid and corrupted images
- Preprocessing dimensions and normalization $(0-1)$
- Strict model shape verification $(32, 32, 3) \rightarrow 10$
- API route status codes and JSON response schemas

---

## 9. Docker Deployment

### Build the Image
```bash
docker build -t cifar-vision-app .
```

### Run the Container
```bash
docker run -d -p 8000:8000 --name cifar_app cifar-vision-app
```
Access at `http://localhost:8000`.

---

## 10. Limitations

- **ANN Architecture:** The model uses fully connected Dense layers rather than spatial Convolutional filters (CNN). Its classification accuracy on the CIFAR-10 test set is approximately $46\%-50\%$.
- **32×32 Image Resolution:** High-resolution photographs will be resized to $32\times32$, which leads to pixel downsampling. Real-world photographs with complex backgrounds may yield unexpected predictions.
