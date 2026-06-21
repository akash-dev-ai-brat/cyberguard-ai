import os
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, create_model
from typing import List, Dict, Any

app = FastAPI(title="CyberGuard AI API", version="1.0.0")

# Load models and preprocessors on startup
class MLStore:
    model = None
    preprocessor = None
    explainer = None
    target_encoding = {'Normal': 0, 'DoS': 1, 'Probe': 2, 'R2L': 3, 'U2R': 4}
    reverse_target_encoding = {v: k for k, v in target_encoding.items()}
    columns = [
        'duration', 'protocol_type', 'service', 'flag', 'src_bytes',
        'dst_bytes', 'land', 'wrong_fragment', 'urgent', 'hot',
        'num_failed_logins', 'logged_in', 'num_compromised', 'root_shell',
        'su_attempted', 'num_root', 'num_file_creations', 'num_shells',
        'num_access_files', 'num_outbound_cmds', 'is_host_login',
        'is_guest_login', 'count', 'srv_count', 'serror_rate',
        'srv_serror_rate', 'rerror_rate', 'srv_rerror_rate', 'same_srv_rate',
        'diff_srv_rate', 'srv_diff_host_rate', 'dst_host_count',
        'dst_host_srv_count', 'dst_host_same_srv_rate', 'dst_host_diff_srv_rate',
        'dst_host_same_src_port_rate', 'dst_host_srv_diff_host_rate',
        'dst_host_serror_rate', 'dst_host_srv_serror_rate', 'dst_host_rerror_rate',
        'dst_host_srv_rerror_rate'
    ]

ml_store = MLStore()

@app.on_event("startup")
def load_assets():
    models_dir = "models"
    try:
        from src.preprocessor import Preprocessor
        preprocessor = Preprocessor()
        preprocessor.load(directory=models_dir)
        ml_store.preprocessor = preprocessor
        
        ml_store.model = joblib.load(os.path.join(models_dir, 'best_model.pkl'))
        ml_store.explainer = joblib.load(os.path.join(models_dir, 'shap_explainer.pkl'))
        print("Models loaded successfully.")
    except Exception as e:
        print(f"Error loading models: {e}")

# Create dynamic Pydantic model for input based on COLUMNS
# For simplicity, using Dict in endpoint, but let's define a schema if needed.
class PredictRequest(BaseModel):
    data: Dict[str, Any]

@app.get("/")
def root():
    return {"message": "Welcome to CyberGuard AI API. Use /predict to classify network traffic."}

@app.get("/health")
def health_check():
    status = "healthy" if ml_store.model is not None else "models_not_loaded"
    return {"status": status}

@app.get("/classes")
def get_classes():
    return {
        "classes": list(ml_store.target_encoding.keys()),
        "descriptions": {
            "Normal": "Normal background traffic.",
            "DoS": "Denial of Service attack (e.g. syn flood).",
            "Probe": "Surveillance and other probing (e.g. port scanning).",
            "R2L": "Unauthorized access from a remote machine (e.g. password guessing).",
            "U2R": "Unauthorized access to local superuser privileges (e.g. buffer overflow)."
        }
    }

@app.post("/predict")
def predict(request: PredictRequest):
    if not ml_store.model:
        raise HTTPException(status_code=503, detail="Models are not loaded.")
        
    try:
        # Convert to DataFrame
        df = pd.DataFrame([request.data])
        
        # Ensure all columns are present
        for col in ml_store.columns:
            if col not in df.columns:
                df[col] = 0 # Default filling, but ideally client should send all
                
        # Reorder to match training
        df = df[ml_store.columns]
        
        # Preprocess
        X_scaled = ml_store.preprocessor.transform(df)
        
        # Predict
        probs = ml_store.model.predict_proba(X_scaled)[0]
        pred_idx = int(ml_store.model.predict(X_scaled)[0])
        pred_class = ml_store.reverse_target_encoding[pred_idx]
        confidence = float(probs[pred_idx])
        
        # Class probabilities mapping
        class_probs = {ml_store.reverse_target_encoding[i]: float(p) for i, p in enumerate(probs)}
        
        # SHAP
        shap_values = ml_store.explainer.shap_values(X_scaled)
        
        # SHAP returns a list of arrays for multiclass or a 3D array
        # Let's extract values for the predicted class
        if isinstance(shap_values, list):
            sv = shap_values[pred_idx][0]
        elif len(shap_values.shape) == 3:
            sv = shap_values[0, :, pred_idx]
        else:
            # Binary or other format fallback
            sv = shap_values[0]
            
        feature_contributions = []
        for feature, sv_val in zip(ml_store.columns, sv):
            feature_contributions.append({"feature": feature, "contribution": float(sv_val)})
            
        # Sort by absolute contribution magnitude
        feature_contributions.sort(key=lambda x: abs(x["contribution"]), reverse=True)
        
        return {
            "prediction": pred_class,
            "confidence": confidence,
            "probabilities": class_probs,
            "top_features": feature_contributions[:5] # Top 5 SHAP features
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
