import pandas as pd
import numpy as np
import math

class Predictor:
    def __init__(self):
        # No external dependencies needed
        pass
        
    def _calculate_poisson_probability(self, k, lam):
        """Calculate Poisson probability for k events with rate lam"""
        return (lam ** k) * math.exp(-lam) / math.factorial(k)

    def predict(self, features_df):
        """Makes a prediction using a simple Poisson model (no sklearn needed)"""
        try:
            # Get features or use defaults
            home_avg_goals = features_df.get('home_avg_goals', 1.5)
            away_avg_goals = features_df.get('away_avg_goals', 1.2)
            home_form = features_df.get('home_form', 0.6)
            away_form = features_df.get('away_form', 0.5)
            
            # Adjust averages based on form
            home_attack = home_avg_goals * (0.8 + 0.4 * home_form)
            away_attack = away_avg_goals * (0.8 + 0.4 * away_form)
            home_defense = away_avg_goals * (1.2 - 0.4 * home_form)  # Inverse relationship
            away_defense = home_avg_goals * (1.2 - 0.4 * away_form)
            
            # Calculate expected goals using Poisson distribution
            home_expected = (home_attack + away_defense) / 2
            away_expected = (away_attack + home_defense) / 2
            
            # Calculate probabilities for different scorelines
            max_goals = 5
            home_win_prob = 0
            draw_prob = 0
            away_win_prob = 0
            
            for i in range(max_goals + 1):  # home goals
                for j in range(max_goals + 1):  # away goals
                    prob = (self._calculate_poisson_probability(i, home_expected) * 
                           self._calculate_poisson_probability(j, away_expected))
                    
                    if i > j:
                        home_win_prob += prob
                    elif i == j:
                        draw_prob += prob
                    else:
                        away_win_prob += prob
            
            # Normalize probabilities (should sum to approximately 1)
            total = home_win_prob + draw_prob + away_win_prob
            home_win_prob /= total
            draw_prob /= total
            away_win_prob /= total
            
            # Create prediction dictionary
            prediction_dict = {
                '1': home_win_prob,
                'X': draw_prob,
                '2': away_win_prob
            }
            
            # Find most likely outcome
            most_likely = max(prediction_dict, key=prediction_dict.get)
            
            return most_likely, prediction_dict
            
        except Exception as e:
            # Fallback to demo predictions if anything goes wrong
            print(f"Prediction error: {e}")
            return self._demo_predictions()
    
    def _demo_predictions(self):
        """Fallback demo predictions"""
        # Simple probabilities that always work
        demo_probs = np.array([0.45, 0.30, 0.25])  # Home, Draw, Away
        demo_probs = demo_probs / np.sum(demo_probs)  # Ensure they sum to 1
        
        class_labels = ['1', 'X', '2']
        prediction_dict = dict(zip(class_labels, demo_probs))
        most_likely = max(prediction_dict, key=prediction_dict.get)
        return most_likely, prediction_dict
