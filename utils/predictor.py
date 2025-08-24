import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pickle
import os

class Predictor:
    def __init__(self):
        self.model = self._create_demo_model()
        
    def _create_demo_model(self):
        """Creates a simple demo model for prediction"""
        try:
            # Create a simple demo model
            model = RandomForestClassifier(n_estimators=50, random_state=42)
            
            # Create realistic demo training data
            np.random.seed(42)
            n_samples = 1000
            
            # Features: home_avg_goals, away_avg_goals, home_form, away_form
            X = np.column_stack([
                np.random.uniform(0.5, 2.5, n_samples),  # home_avg_goals
                np.random.uniform(0.3, 2.0, n_samples),  # away_avg_goals
                np.random.uniform(0.2, 0.9, n_samples),  # home_form
                np.random.uniform(0.1, 0.8, n_samples)   # away_form
            ])
            
            # Generate realistic outcomes based on features
            home_win_prob = 0.4 + 0.2 * (X[:, 0] - X[:, 1]) + 0.3 * (X[:, 2] - X[:, 3])
            draw_prob = 0.3 - 0.1 * np.abs(X[:, 0] - X[:, 1])
            away_win_prob = 1 - home_win_prob - draw_prob
            
            # Create labels based on probabilities
            y = []
            for i in range(n_samples):
                outcomes = ['1', 'X', '2']
                probs = [home_win_prob[i], draw_prob[i], away_win_prob[i]]
                probs = np.maximum(probs, 0)  # Ensure non-negative
                probs = probs / np.sum(probs)  # Normalize
                y.append(np.random.choice(outcomes, p=probs))
            
            model.fit(X, y)
            return model
            
        except Exception as e:
            print(f"Error creating model: {e}")
            return None

    def predict(self, features_df):
        """Makes a prediction on a DataFrame of features."""
        if self.model is None:
            # Return demo predictions if model isn't loaded
            return self._demo_predictions()
            
        try:
            # Ensure we have the right features in the right order
            expected_features = ['home_avg_goals', 'away_avg_goals', 'home_form', 'away_form']
            
            # Create feature array in the correct order
            X_pred = np.zeros((1, 4))
            for i, feature in enumerate(expected_features):
                if feature in features_df.columns:
                    X_pred[0, i] = features_df[feature].iloc[0]
                else:
                    # Use reasonable defaults if features are missing
                    defaults = [1.5, 1.2, 0.6, 0.5]
                    X_pred[0, i] = defaults[i]
            
            # Model predicts probabilities for each class
            probabilities = self.model.predict_proba(X_pred)[0]
            class_labels = self.model.classes_
            
            prediction_dict = dict(zip(class_labels, probabilities))
            most_likely = max(prediction_dict, key=prediction_dict.get)
            
            return most_likely, prediction_dict
            
        except Exception as e:
            print(f"Prediction error: {e}")
            return self._demo_predictions()
    
    def _demo_predictions(self):
        """Fallback demo predictions"""
        demo_probs = np.random.dirichlet([3, 2, 2], size=1)[0]  # More realistic probabilities
        class_labels = ['1', 'X', '2']
        prediction_dict = dict(zip(class_labels, demo_probs))
        most_likely = max(prediction_dict, key=prediction_dict.get)
        return most_likely, prediction_dict
