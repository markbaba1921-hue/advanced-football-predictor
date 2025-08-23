# utils/data_processor.py
import pandas as pd

def calculate_team_strengths(team_stats_dict, league_id):
    strength_dict = {}
    
    for team_name, stats in team_stats_dict.items():
        if not stats:
            continue
            
        try:
            goals_for = stats['goals']['for']['total']['total']
            goals_against = stats['goals']['against']['total']['total']
            matches_played = stats['fixtures']['played']['total']
            
            shots_on_goal = stats['shots']['on']['total']
            expected_goals = stats['goals']['for']['expected']['total']
            
            avg_goals_for = goals_for / matches_played if matches_played > 0 else 0
            avg_goals_against = goals_against / matches_played if matches_played > 0 else 0
            avg_xG = expected_goals / matches_played if matches_played > 0 else 0
            
            attack_strength = (avg_goals_for * 0.7) + (avg_xG * 0.3)
            defense_strength = 1 / avg_goals_against if avg_goals_against > 0 else 1
            
            strength_dict[team_name] = (attack_strength, defense_strength)
            
        except KeyError as e:
            print(f"Key error processing {team_name}: {e}")
            continue
            
    return strength_dict
