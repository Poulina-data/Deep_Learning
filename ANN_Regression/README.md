# Boston Median House Price Prediction

A production-grade Artificial Neural Network (ANN) regression web application and REST API built with Flask. The application uses a trained deep learning model to predict the median value of owner-occupied homes based on 13 socioeconomic and environmental features from the Boston Housing dataset.

---

## 1. Project Description

This application provides an enterprise-quality AI analytics interface and an automated prediction service. Given 13 property and neighborhood attributes, the application performs standardized feature scaling, passes the normalized tensor through a multi-layer deep neural network, and returns a continuous median house price prediction in real time.

---

## 2. Problem Statement

Real estate valuation depends on complex, non-linear relationships among crime rates, tax burdens, school quality, industrial zoning, and environmental pollution. Traditional linear regression often fails to capture these intricate interactions. This project employs a multi-layer perceptron (ANN regression) trained on historical housing data to estimate continuous home values with high accuracy.

---

## 3. Model Architecture

The regression model is built with Keras / TensorFlow as a feed-forward Sequential Artificial Neural Network:

- **Input Layer:** 13 numerical inputs
- **Dense Layer 1:** 64 neurons, ReLU activation
- **Dense Layer 2:** 32 neurons, ReLU activation
- **Dense Layer 3:** 16 neurons, ReLU activation
- **Output Layer:** 1 neuron (linear continuous output, no activation)
- **Optimizer:** Adam
- **Loss Function:** Mean Squared Error (MSE)
- **Evaluation Metric:** Mean Absolute Error (MAE)

Preprocessing is handled by a pre-fitted `StandardScaler` (`scaler.pkl`), strictly applying `.transform()` during inference without refitting.

---

## 4. Input Features

The model expects exactly 13 features in this sequence:

| # | Code | Feature Label | Type | Description |
|---|------|---------------|------|-------------|
| 1 | `CRIM` | Per Capita Crime Rate | Continuous | Per capita crime rate by town |
| 2 | `ZN` | Residential Land Zoned | Continuous | Proportion of residential land zoned for lots > 25,000 sq.ft. |
| 3 | `INDUS` | Non-Retail Business Land | Continuous | Proportion of non-retail business acres per town |
| 4 | `CHAS` | Charles River Indicator | Binary (0/1) | 1 if tract bounds Charles River; 0 otherwise |
| 5 | `NOX` | Nitric Oxide Concentration | Continuous | Nitric oxides concentration (parts per 10 million) |
| 6 | `RM` | Average Number of Rooms | Continuous | Average number of rooms per dwelling |
| 7 | `AGE` | Owner-Occupied Units Age | Continuous | Proportion of owner-occupied units built prior to 1940 |
| 8 | `DIS` | Distance to Employment Centers | Continuous | Weighted distances to five Boston employment centers |
| 9 | `RAD` | Highway Accessibility Index | Integer | Index of accessibility to radial highways |
| 10 | `TAX` | Property Tax Rate | Continuous | Full-value property-tax rate per $10,000 |
| 11 | `PTRATIO` | Pupil-Teacher Ratio | Continuous | Pupil-teacher ratio by town |
| 12 | `B` | Black Population Index | Continuous | 1000(Bk - 0.63)^2 where Bk is the proportion of Black residents |
| 13 | `LSTAT` | Lower Status Population % | Continuous | Percentage of lower status of the population |

---

## 5. Project Structure

```
boston-house-price-app/
├── app.py                      # Application entry point
├── config.py                   # Environment-driven configuration
├── requirements.txt            # Production dependencies
├── README.md                   # Project documentation
├── .gitignore                  # Git ignore rules
├── .env.example                # Sample environment variables
├── Procfile                    # Gunicorn production server command
│
├── model/                      # Model artifacts directory
│   ├── boston_house_model.h5   # Trained Keras ANN model
│   └── scaler.pkl              # Fitted scikit-learn StandardScaler
│
├── app/                        # Application package
│   ├── __init__.py             # Flask application factory
│   ├── routes/                 # Blueprint route modules
│   │   ├── __init__.py
│   │   ├── main_routes.py      # GET / and GET /health
│   │   └── prediction_routes.py# POST /predict API
│   ├── services/               # Business and ML logic
│   │   ├── __init__.py
│   │   └── prediction_service.py # Model and scaler lifecycle singleton
│   ├── utils/                  # Helper utilities
│   │   ├── __init__.py
│   │   ├── validators.py       # Payload and bounds validation
│   │   └── error_handlers.py   # Global error handling (HTML & JSON)
│   └── constants/              # Feature definitions & ordering
│       ├── __init__.py
│       └── features.py         # Canonical feature order & metadata
│
├── templates/                  # Jinja2 HTML templates
│   ├── base.html               # Base layout, typography, header, footer
│   ├── index.html              # Interactive two-column dashboard
│   └── error.html              # Custom HTTP error page
│
├── static/                     # Static assets
│   ├── css/
│   │   └── style.css           # Premium enterprise dark-theme stylesheet
│   ├── js/
│   │   └── app.js              # Vanilla JS frontend controller
│   └── assets/                 # Icons & vector assets
│       └── icons/
│           └── house.svg
│
└── tests/                      # Automated test suite
    ├── __init__.py
    ├── test_prediction.py      # Unit tests for model service
    ├── test_routes.py          # Integration tests for HTTP endpoints
    └── test_validation.py      # Validation logic tests
```

---

## 6. Installation & Setup

### Prerequisites
- Python 3.9+ or Python 3.10+
- `pip` package manager

### 1. Clone or Navigate to the Project Directory
```bash
cd boston-house-price-app
```

### 2. Set Up a Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Verify Model Artifacts Placement
Ensure that `boston_house_model.h5` and `scaler.pkl` are present in the `model/` directory:
```
model/
  boston_house_model.h5
  scaler.pkl
```

---

## 7. Running Locally

### Development Server
```bash
python app.py
```
Open your browser and navigate to:
```
http://localhost:5000
```

---

## 8. REST API Endpoints

### Health Check
**Endpoint:** `GET /health`  
**Description:** Verifies service health and confirms the model is loaded in memory.

**Response (200 OK):**
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

---

### House Price Prediction
**Endpoint:** `POST /predict`  
**Headers:** `Content-Type: application/json`

**Sample Request Body:**
```json
{
  "CRIM": 0.02,
  "ZN": 18,
  "INDUS": 2.5,
  "CHAS": 0,
  "NOX": 0.45,
  "RM": 6.5,
  "AGE": 65,
  "DIS": 4.5,
  "RAD": 1,
  "TAX": 300,
  "PTRATIO": 15,
  "B": 390,
  "LSTAT": 5
}
```

**Sample Success Response (200 OK):**
```json
{
  "success": true,
  "prediction": 27.7292
}
```

**Sample Error Response (400 Bad Request):**
```json
{
  "success": false,
  "error": "Missing required features: LSTAT."
}
```

---

## 9. Running Tests

Execute the automated test suite with `pytest`:

```bash
pytest tests/ -v
```

All tests for routes, validation rules, model inference, and error handling will run.

---

## 10. Production Deployment

For production environments, run using Gunicorn:

```bash
gunicorn app:app --bind 0.0.0.0:5000 --workers 4 --timeout 120
```

On PaaS platforms (Heroku, Render, Railway, AWS Elastic Beanstalk), the included `Procfile` is automatically detected:
```
web: gunicorn app:app
```

---

## 11. Limitations & Ethics

- The Boston Housing dataset was collected in the 1970s; predictions reflect historical relationships rather than modern real-estate market pricing.
- The feature `B` incorporates historical demographic indexing from the original dataset; production applications for actual valuation should consider contemporary, unbiased data standards.
- Predictions represent continuous statistical estimations and should not be used as official real-estate appraisals.
