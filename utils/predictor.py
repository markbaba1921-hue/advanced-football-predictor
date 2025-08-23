# utils/predictor.py (Simplified Version)
import numpy as np
from scipy.stats import poisson

def advanced_predict_match(home_team_name, away_team_name, team_strengths):
    if home_team_name not in team_strengths or away_team_name not in team_strengths:
        return get_sample_prediction()
    
    home_attack, home_defense = team_strengths[home_team_name]
    away_attack, away_defense = team_strengths[away_team_name]
    
    # Calculate expected goals
    home_xG = (home_attack / away_defense) * 1.6
    away_xG = (away_attack / home_defense) * 1.2
    
    # Poisson distribution calculations
    max_goals = 6
    home_probs = [poisson.pmf(i, home_xG) for i in range(max_goals)]
    away_probs = [poisson.pmf(i, away_xG) for i in range(max_goals)]
    
    home_win, draw, away_win = 0, 0, 0
    score_probs = {}
    
    for i in range(max_goals):
        for j in range(max_goals):
            p = home_probs[i] * away_probs[j]
            if i > j:
                home_win += p
            elif i == j:
                draw += p
            else:
                away_win += p
            score_probs[f"{i}-{j}"] = p
    
    most_likely_score = max(score_probs, key=score_probs.get)
    
    # Calculate additional probabilities
    btts_prob = 1 - (poisson.pmf(0, home_xG) * poisson.pmf(0, away_xG))
    over_25_prob = 1 - sum([home_probs[i] * away_probs[j] for i in range(3) for j in range(3 - i)])
    
    return {
        "home_win": round(home_win * 100, 1),
        "draw": round(draw * 100, 1),
        "away_win": round(away_win * 100, 1),
        "most_likely_score": most_likely_score,
        "home_xG": round(home_xG, 2),
        "away_xG": round(away_xG, 2),
        "btts_prob": round(btts_prob * 100, 1),
        "over_25_prob": round(over_25_prob * 100, 1),
        "confidence": "high"
    }

def get_sample_prediction():
    return {
        "home_win": 48.7,
        "draw": 27.3,
        "away_win": 24.0,
        "most_likely_score": "2-1",
        "home_xG": 1.9,
        "away_xG": 1.1,
        "btts_prob": 65.2,
        "over_25_prob": 61.8,
        "confidence": "medium"
    }

def predict_league_fixtures(fixtures, team_strengths):
    predictions = []
    
    for fixture in fixtures:
        home_team = fixture['teams']['home']['name']
        away_team = fixture['teams']['away']['name']
        
        prediction = advanced_predict_match(home_team, away_team, team_strengths)
        prediction['fixture'] = fixture
        predictions.append(prediction)
    
    return predictions
