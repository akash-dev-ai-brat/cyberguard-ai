import os
import shap
import joblib
import matplotlib.pyplot as plt
import numpy as np

def build_and_save_explainer(model, X_train, models_dir="models", assets_dir="assets"):
    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(assets_dir, exist_ok=True)
    
    print("Building SHAP TreeExplainer...")
    # Use a background dataset for explainer if needed, but TreeExplainer works fine without for XGBoost
    explainer = shap.TreeExplainer(model)
    
    joblib.dump(explainer, os.path.join(models_dir, 'shap_explainer.pkl'))
    
    print("Generating SHAP summary plot on a sample of training data...")
    # Take a sample to compute SHAP values quickly for the summary plot
    X_sample = X_train.sample(n=min(1000, len(X_train)), random_state=42)
    shap_values = explainer.shap_values(X_sample)
    
    # Check shape of shap_values, for multiclass XGBoost it might be a list of arrays or an array of shape (n_samples, n_features, n_classes)
    # shap.summary_plot can handle it
    
    plt.figure(figsize=(10, 8))
    # If shap_values is a list (one for each class), shap will color them automatically in summary_plot
    shap.summary_plot(shap_values, X_sample, plot_type="bar", show=False)
    
    plt.tight_layout()
    plt.savefig(os.path.join(assets_dir, 'shap_summary.png'))
    plt.close()
    
    print("Explainer and summary plot saved.")
    return explainer
