# utils/data_processor.py
def calculate_team_strengths(team_stats_dict, league_id):
    """Hardcoded realistic team strengths"""
    premier_league = {
        'Manchester City': (2.7, 0.7),
        'Liverpool': (2.5, 0.8),
        'Arsenal': (2.3, 0.9),
        'Chelsea': (2.0, 1.1),
        'Manchester United': (1.9, 1.2),
        'Tottenham': (2.1, 1.3),
        'Newcastle': (1.8, 1.2),
        'Aston Villa': (1.7, 1.3)
    }
    
    la_liga = {
        'Real Madrid': (2.6, 0.8),
        'Barcelona': (2.4, 0.9),
        'Atletico Madrid': (2.0, 0.8),
        'Sevilla': (1.8, 1.1),
        'Valencia': (1.6, 1.2)
    }
    
    bundesliga = {
        'Bayern Munich': (2.8, 0.7),
        'Dortmund': (2.3, 1.0),
        'RB Leipzig': (2.1, 1.1),
        'Leverkusen': (2.0, 1.0)
    }
    
    serie_a = {
        'Inter Milan': (2.2, 0.8),
        'AC Milan': (2.1, 0.9),
        'Juventus': (1.9, 0.8),
        'Napoli': (2.0, 1.1)
    }
    
    ligue_1 = {
        'PSG': (2.7, 0.8),
        'Marseille': (2.0, 1.2),
        'Lyon': (1.9, 1.3),
        'Monaco': (2.1, 1.4)
    }
    
    leagues = {
        "premier-league": premier_league,
        "la-liga": la_liga,
        "bundesliga": bundesliga,
        "serie-a": serie_a,
        "ligue-1": ligue_1
    }
    
    return leagues.get(league_id, {})
