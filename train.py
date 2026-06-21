import os
from src.data_loader import load_data
from src.preprocessor import Preprocessor
from src.trainer import train_and_evaluate
from src.explainer import build_and_save_explainer

def main():
    print("--- Starting CyberGuard AI Training Pipeline ---")
    
    # 1. Load Data
    print("\n1. Loading Data...")
    X_train, y_train, X_test, y_test = load_data()
    print(f"Loaded {len(X_train)} training records and {len(X_test)} testing records.")
    
    # 2. Preprocess
    print("\n2. Preprocessing Data...")
    preprocessor = Preprocessor()
    X_train_resampled, y_train_resampled = preprocessor.fit_transform(X_train, y_train)
    X_test_scaled = preprocessor.transform(X_test)
    
    # Save preprocessor
    preprocessor.save(directory="models")
    print("Preprocessing completed and preprocessor saved.")
    
    # 3. Train Models
    print("\n3. Training Models...")
    best_model, metrics = train_and_evaluate(X_train_resampled, y_train_resampled, X_test_scaled, y_test, models_dir="models")
    print("Training completed. Best model is XGBoost.")
    
    # 4. Explainability
    print("\n4. Generating SHAP Explainability...")
    # Convert resampled training data to DataFrame for feature names if needed
    import pandas as pd
    X_train_df = pd.DataFrame(X_train_resampled, columns=X_train.columns)
    build_and_save_explainer(best_model, X_train_df, models_dir="models", assets_dir="assets")
    
    print("\n--- Pipeline Completed Successfully ---")

if __name__ == "__main__":
    main()
