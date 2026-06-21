import os
import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from imblearn.over_sampling import SMOTE

class Preprocessor:
    def __init__(self):
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.categorical_cols = ['protocol_type', 'service', 'flag']
        self.numerical_cols = []
        
    def fit_transform(self, X_train, y_train):
        X = X_train.copy()
        
        # Identify numerical columns
        self.numerical_cols = [col for col in X.columns if col not in self.categorical_cols]
        
        # Label Encoding for categorical features
        for col in self.categorical_cols:
            le = LabelEncoder()
            # We fit on the column, but we also need to handle unseen labels later.
            # LabelEncoder doesn't handle unseen labels natively, so we map them later
            # For fit, we just learn the known ones
            X[col] = le.fit_transform(X[col].astype(str))
            self.label_encoders[col] = le
            
        # Standard Scaling
        X[self.numerical_cols] = self.scaler.fit_transform(X[self.numerical_cols])
        
        # SMOTE balancing
        print("Applying SMOTE...")
        smote = SMOTE(random_state=42)
        X_resampled, y_resampled = smote.fit_resample(X, y_train)
        print("SMOTE completed.")
        
        return X_resampled, y_resampled
        
    def transform(self, X_test):
        X = X_test.copy()
        
        for col in self.categorical_cols:
            le = self.label_encoders[col]
            # Handle unseen labels by assigning them to a known value or replacing with mode
            # Here we just use a default fallback to 0 or we handle unknown values safely
            known_classes = set(le.classes_)
            X[col] = X[col].map(lambda s: s if s in known_classes else le.classes_[0])
            X[col] = le.transform(X[col].astype(str))
            
        X[self.numerical_cols] = self.scaler.transform(X[self.numerical_cols])
        return X

    def save(self, directory="models"):
        os.makedirs(directory, exist_ok=True)
        joblib.dump(self.label_encoders, os.path.join(directory, 'label_encoders.pkl'))
        joblib.dump(self.scaler, os.path.join(directory, 'scaler.pkl'))
        joblib.dump(self.categorical_cols, os.path.join(directory, 'cat_cols.pkl'))
        joblib.dump(self.numerical_cols, os.path.join(directory, 'num_cols.pkl'))
        
    def load(self, directory="models"):
        self.label_encoders = joblib.load(os.path.join(directory, 'label_encoders.pkl'))
        self.scaler = joblib.load(os.path.join(directory, 'scaler.pkl'))
        self.categorical_cols = joblib.load(os.path.join(directory, 'cat_cols.pkl'))
        self.numerical_cols = joblib.load(os.path.join(directory, 'num_cols.pkl'))
