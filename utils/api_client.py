# utils/api_client.py
import streamlit as st
from datetime import datetime, timedelta
import random

def get_league_id(country_name):
    league_ids = {
        "England": "premier-league",
        "Spain": "la-liga", 
        "Germany": "bundesliga",
        "Italy": "serie-a",
        "France": "ligue-1",
    }
    return league_ids.get(country_name)

def get_season():
    return "2024-2025"

def get_teams(league_id):
    """Hardcoded teams for each league"""
    teams_data = {
        "premier-league": [
            {'team': {'id': 1, 'name': 'Manchester City'}},
            {'team': {'id': 2, 'name': 'Liverpool'}},
            {'team': {'id': 3, 'name': 'Arsenal'}},
            {'team': {'id': 4, 'name': 'Chelsea'}},
            {'team': {'id': 5, 'name': 'Manchester United'}},
            {'team': {'id': 6, 'name': 'Tottenham'}},
            {'team': {'id': 7, 'name': 'Newcastle'}},
            {'team': {'id': 8, 'name': 'Aston Villa'}}
        ],
        "la-liga": [
            {'team': {'id': 9, 'name': 'Real Madrid'}},
            {'team': {'id': 10, 'name': 'Barcelona'}},
            {'team': {'id': 11, 'name': 'Atletico Madrid'}},
            {'team': {'id': 12, 'name': 'Sevilla'}},
            {'team': {'id': 13, 'name': 'Valencia'}}
        ],
        "bundesliga": [
            {'team': {'id': 14, 'name': 'Bayern Munich'}},
            {'team': {'id': 15, 'name': 'Dortmund'}},
            {'team': {'id': 16, 'name': 'RB Leipzig'}},
            {'team': {'id': 17, 'name': 'Leverkusen'}}
        ],
        "serie-a": [
            {'team': {'id': 18, 'name': 'Inter Milan'}},
            {'team': {'id': 19, 'name': 'AC Milan'}},
            {'team': {'id': 20, 'name': 'Juventus'}},
            {'team': {'id': 21, 'name': 'Napoli'}}
        ],
        "ligue-1": [
            {'team': {'id': 22, 'name': 'PSG'}},
            {'team': {'id': 23, 'name': 'Marseille'}},
            {'team': {'id': 24, 'name': 'Lyon'}},
            {'team': {'id': 25, 'name': 'Monaco'}}
        ]
    }
    return teams_data.get(league_id, [])

def get_fixtures(league_id, next_n=10):
    """Generate realistic fixtures for the next 2 weeks"""
    teams = [team['team']['name'] for team in get_teams(league_id)]
    fixtures = []
    
    for i in range(next_n):
        random.shuffle(teams)
        home_team = teams[0]
        away_team = teams[1]
        
        match_date = (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%dT%H:%M:%S+00:00')
        
        fixtures.append({
            'fixture': {
                'date': match_date,
                'timestamp': int((datetime.now() + timedelta(days=i)).timestamp())
            },
            'teams': {
                'home': {'name': home_team},
                'away': {'name': away_team}
            }
        })
    
    return fixtures

def get_team_statistics(league_id, team_id):
    """Generate realistic stats for each team"""
    return {
        'goals': {'for': {'total': {'total': random.randint(30, 80)}, 
                         'expected': {'total': random.uniform(35, 75)}}, 
                 'against': {'total': {'total': random.randint(20, 50)}}},
        'fixtures': {'played': {'total': 38}},
        'shots': {'on': {'total': random.randint(100, 250)}}
    }
