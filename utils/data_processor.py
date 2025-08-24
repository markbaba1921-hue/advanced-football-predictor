import pandas as pd
import numpy as np

class DataProcessor:
    @staticmethod
    def create_features(fixtures_data):
        """
        Processes raw fixtures data into a DataFrame of features (X) and targets (y).
        """
        data_list = []
        for fixture in fixtures_data:
            home_team = fixture['teams']['home']['name']
            away_team = fixture['teams']['away']['name']
            goals_home = fixture['goals']['home']
            goals_away = fixture['goals']['away']

            # Determine the target outcome (1: Home Win, X: Draw, 2: Away Win)
            if goals_home > goals_away:
                result = '1'
            elif goals_home < goals_away:
                result = '2'
            else:
                result = 'X'

            # Simplified features for demonstration
            home_team_avg_goals = np.random.uniform(1.2, 2.1)
            away_team_avg_goals = np.random.uniform(0.8, 1.9)
            home_team_form = np.random.uniform(0.4, 0.9)
            away_team_form = np.random.uniform(0.3, 0.8)

            data_list.append({
                'home_team': home_team,
                'away_team': away_team,
                'home_avg_goals': home_team_avg_goals,
                'away_avg_goals': away_team_avg_goals,
                'home_form': home_team_form,
                'away_form': away_team_form,
                'result': result
            })

        df = pd.DataFrame(data_list)
        return df

    def prepare_prediction_data(self, home_team, away_team):
        """Prepares live data for a specific fixture to feed into the model."""
        # For demonstration, we'll use random data
        # In a real app, you would fetch actual team statistics here
        
        prediction_data = {
            'home_avg_goals': np.random.uniform(1.2, 2.1),
            'away_avg_goals': np.random.uniform(0.8, 1.9),
            'home_form': np.random.uniform(0.4, 0.9),
            'away_form': np.random.uniform(0.3, 0.8),
        }
        return pd.DataFrame([prediction_data])
