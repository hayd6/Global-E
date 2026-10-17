"""
src/models/pipeline_wrapper.py
Class Wrapper hợp nhất Imputer và mô hình Calibrated Model
để cho phép gọi .predict_proba() trực tiếp từ raw features DataFrame hoặc NumPy array.
"""

import numpy as np
import pandas as pd


class FullPipelineModel:
    def __init__(self, imputer, model, feature_cols):
        self.imputer = imputer
        self.model = model
        self.feature_cols = feature_cols
        self.classes_ = np.array([0, 1])

    def predict_proba(self, X):
        if isinstance(X, pd.DataFrame):
            X_arr = X[self.feature_cols].values
        else:
            X_arr = X
        X_imp = self.imputer.transform(X_arr)
        return self.model.predict_proba(X_imp)

    def predict(self, X):
        probs = self.predict_proba(X)[:, 1]
        return (probs >= 0.5).astype(int)
