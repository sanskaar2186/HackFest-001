# Machine Learning Models

This directory contains all machine learning models, preprocessing scripts, and model utilities used in the project.

## Directory Structure

```
ml_models/
├── trained/        # Saved trained models
├── preprocessing/  # Data preprocessing scripts
├── utils/         # Helper functions and utilities
└── training/      # Model training scripts
```

## Models Overview

- **Model 1**: Description of what this model does
- **Model 2**: Description of what this model does

## Training

To train a model:

```bash
python training/train_model.py --data-path ../data/dataset.csv --model-name model1
```

## Inference

To run inference:

```python
from ml_models.utils import load_model
from ml_models.preprocessing import preprocess_data

# Load the model
model = load_model('model1')

# Preprocess your data
processed_data = preprocess_data(raw_data)

# Get predictions
predictions = model.predict(processed_data)
```

## Model Performance

| Model Name | Accuracy | F1 Score | Last Updated |
|------------|----------|-----------|--------------|
| Model 1    | 0.85     | 0.83      | 2025-08-14  |
| Model 2    | 0.92     | 0.90      | 2025-08-14  |

## Dependencies

Required packages:
- scikit-learn==1.3.0
- tensorflow==2.13.0
- torch==2.0.1
- pandas==2.0.3
- numpy==1.24.3

Install dependencies:
```bash
pip install -r requirements.txt
```

## Data Requirements

- Input data format specifications
- Required features/columns
- Data preprocessing steps

## Model Deployment

Instructions for deploying models in production:

1. Export model:
```bash
python utils/export_model.py --model-path trained/model1 --format onnx
```

2. Deploy using FastAPI endpoint:
```python
from fastapi import FastAPI
from ml_models.utils import load_production_model

app = FastAPI()
model = load_production_model()

@app.post("/predict")
async def predict(data: dict):
    return {"prediction": model.predict(data)}
```

## Contributing

When adding new models:
1. Create a new directory under `training/`
2. Add model documentation
3. Include training and evaluation scripts
4. Update this README with model details

## Monitoring

Model performance monitoring and retraining guidelines:
- Monitor prediction accuracy weekly
- Retrain models monthly with new data
- Log all predictions for analysis