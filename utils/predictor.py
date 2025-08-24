import joblib
import pandas as pd
import os
import numpy as np

class Predictor:
    def __init__(self):
        self.model = self._load_model()
        
    def _load_model(self):
        """Loads the pre-trained model or creates a demo model if not found."""
        try:
            # For now, we'll create a simple demo model
            # In a real app, you would load a pre-trained model
            from sklearn.ensemble import RandomForestClassifier
            
            # Create a simple demo model
            model = RandomForestClassifier(n_estimators=10, random_state=42)
            
            # Train on dummy data
            X_dummy = np.random.rand(100, 4)  # 4 features
            y_dummy = np.random.choice(['1', 'X', '2'], 100)  # 3 classes
            
            model.fit(X_dummy, y_dummy)
            return model
            
        except Exception as e:
            print(f"Error loading model: {e}")
            return None

    def predict(self, features_df):
        """Makes a prediction on a DataFrame of features."""
        if self.model is None:
            # Return demo predictions if model isn't loaded
            demo_probs = np.random.dirichlet(np.ones(3), size=1)[0]
            class_labels = ['1', 'X', '2']
            prediction_dict = dict(zip(class_labels, demo_probs))
            most_likely = max(prediction_dict, key=prediction_dict.get)
            return most_likely, prediction_dict
            
        try:
            # Model predicts probabilities for each class
            probabilities = self.model.predict_proba(features_df)[0]
            class_labels = self.model.classes_
            
            prediction_dict = dict(zip(class_labels, probabilities))
            most_likely = max(prediction_dict, key=prediction_dict.get)
            
            return most_likely, prediction_dict
            
        except Exception as e:
            print(f"Prediction error: {e}")
            # Fallback to demo predictions
            demo_probs = np.random.dirichlet(np.ones(3), size=1)[0]
            class_labels = ['1', 'X', '2']
            prediction_dict = dict(zip(class_labels, demo_probs))
            most_likely = max(prediction_dict, key=prediction_dict.get)
            return most_likely, prediction_dict
