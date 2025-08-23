import pandas as pd

def calculate_team_strengths(team_stats_dict, league_id):
    """Calculate team strengths with fallback to sample data"""
    strength_dict = {}
    
    if not team_stats_dict:
        return get_sample_strengths(league_id)
    
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
            
        except KeyError:
            continue
            
    return strength_dict if strength_dict else get_sample_strengths(league_id)

def get_sample_strengths(league_id):
    """Sample team strengths for demonstration"""
    sample_data = {
        39: {'Manchester City': (2.5, 0.8), 'Liverpool': (2.3, 1.0), 'Arsenal': (2.1, 0.9), 
             'Chelsea': (1.8, 1.1), 'Man United': (1.7, 1.2)},
        140: {'Real Madrid': (2.4, 0.8), 'Barcelona': (2.2, 0.9), 'Atletico Madrid': (1.9, 0.8)},
        78: {'Bayern Munich': (2.6, 0.7), 'Dortmund': (2.2, 1.1), 'RB Leipzig': (2.0, 1.2)},
        135: {'Inter Milan': (2.1, 0.8), 'AC Milan': (1.9, 0.9), 'Juventus': (1.8, 0.8)},
        61: {'PSG': (2.5, 0.8), 'Marseille': (1.9, 1.1), 'Lyon': (1.8, 1.2)}
    }
    return sample_data.get(league_id, {})
