# utils/predictor.py
import joblib
import pandas as pd
import os

# Define the path to your trained model
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'xgb_model.pkl')

class Predictor:
    def __init__(self):
        # Load the pre-trained model when this class is instantiated
        try:
            self.model = joblib.load(MODEL_PATH)
        except FileNotFoundError:
            print(f"Error: Model not found at {MODEL_PATH}. Please train the model first.")
            self.model = None

    def predict(self, features_df):
        """Makes a prediction on a DataFrame of features."""
        if self.model is None:
            return "Model not loaded.", {}
            
        # Model predicts probabilities for each class [Draw, Home Win, Away Win]
        probabilities = self.model.predict_proba(features_df)[0]
        
        # Get the class labels from the model
        class_labels = self.model.classes_  # e.g., ['1', '2', 'X']

        # Create a dictionary of outcomes and their probabilities
        prediction_dict = dict(zip(class_labels, probabilities))
        
        # Get the most likely outcome
        most_likely = max(prediction_dict, key=prediction_dict.get)
        
        return most_likely, prediction_dict
