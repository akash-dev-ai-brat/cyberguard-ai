import os
import json
import joblib
import time
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

def train_and_evaluate(X_train, y_train, X_test, y_test, models_dir="models"):
    os.makedirs(models_dir, exist_ok=True)
    
    results = {}
    
    # 1. Random Forest
    print("Training Random Forest...")
    rf = RandomForestClassifier(n_estimators=100, max_depth=20, class_weight='balanced', n_jobs=-1, random_state=42)
    start_time = time.time()
    rf.fit(X_train, y_train)
    rf_time = time.time() - start_time
    
    rf_preds = rf.predict(X_test)
    rf_probs = rf.predict_proba(X_test)
    
    results['Random Forest'] = {
        'Accuracy': float(accuracy_score(y_test, rf_preds)),
        'Precision': float(precision_score(y_test, rf_preds, average='weighted', zero_division=0)),
        'Recall': float(recall_score(y_test, rf_preds, average='weighted', zero_division=0)),
        'F1 Score': float(f1_score(y_test, rf_preds, average='weighted', zero_division=0)),
        'ROC-AUC': float(roc_auc_score(y_test, rf_probs, multi_class='ovr')),
        'Training Time (s)': rf_time
    }
    print(f"Random Forest evaluated. Acc: {results['Random Forest']['Accuracy']:.4f}")
    
    # 2. XGBoost
    print("Training XGBoost...")
    xgb = XGBClassifier(n_estimators=200, max_depth=8, learning_rate=0.1, eval_metric='mlogloss', random_state=42, use_label_encoder=False)
    
    start_time = time.time()
    xgb.fit(X_train, y_train)
    xgb_time = time.time() - start_time
    
    xgb_preds = xgb.predict(X_test)
    xgb_probs = xgb.predict_proba(X_test)
    
    results['XGBoost'] = {
        'Accuracy': float(accuracy_score(y_test, xgb_preds)),
        'Precision': float(precision_score(y_test, xgb_preds, average='weighted', zero_division=0)),
        'Recall': float(recall_score(y_test, xgb_preds, average='weighted', zero_division=0)),
        'F1 Score': float(f1_score(y_test, xgb_preds, average='weighted', zero_division=0)),
        'ROC-AUC': float(roc_auc_score(y_test, xgb_probs, multi_class='ovr')),
        'Training Time (s)': xgb_time
    }
    print(f"XGBoost evaluated. Acc: {results['XGBoost']['Accuracy']:.4f}")
    
    # Save metrics
    with open(os.path.join(models_dir, 'metrics.json'), 'w') as f:
        json.dump(results, f, indent=4)
        
    # Save the best model (XGBoost)
    joblib.dump(xgb, os.path.join(models_dir, 'best_model.pkl'))
    print("Models and metrics saved.")
    
    return xgb, results
