# utils/data_processor.py
import pandas as pd

class DataProcessor:
    @staticmethod
    def create_features(fixtures_data):
        """
        Processes raw fixtures data into a DataFrame of features (X) and targets (y).
        This is the most important step for accuracy.
        """
        data_list = []
        for fixture in fixtures_data:
            # Extract basic info
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

            # --- FEATURE ENGINEERING ---
            # This is a simplified example. A professional app would have 20+ features.
            # You would need to calculate these based on the last N games for each team.
            # Example placeholder features:
            home_team_avg_goals = 1.6  # Should be calculated from past games
            away_team_avg_goals = 1.2
            home_team_form = 0.7        # e.g., % of points from last 5 games
            away_team_form = 0.4

            data_list.append({
                'home_team': home_team,
                'away_team': away_team,
                'home_avg_goals': home_team_avg_goals,
                'away_avg_goals': away_team_avg_goals,
                'home_form': home_team_form,
                'away_form': away_team_form,
                'result': result  # This is our target (y)
            })

        df = pd.DataFrame(data_list)
        return df

    def prepare_prediction_data(self, home_team, away_team):
        """Prepares live data for a specific fixture to feed into the model."""
        # You would use the API client here to get the latest stats for these two teams
        # and calculate their current features (avg goals, form, etc.)
        prediction_data = {
            'home_avg_goals': 1.8,  # Fetched live for the specific team
            'away_avg_goals': 0.9,
            'home_form': 0.8,
            'away_form': 0.5,
        }
        return pd.DataFrame([prediction_data])
