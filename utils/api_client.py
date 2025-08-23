import requests
import pandas as pd
import streamlit as st

# Configuration
API_KEY = st.secrets.get("API_FOOTBALL", {}).get("KEY", "fake-key")
API_HOST = "api-football-v1.p.rapidapi.com"
BASE_URL = "https://api-football-v1.p.rapidapi.com/v3"

headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": API_HOST
}

def get_league_id(country_name):
    league_ids = {
        "England": 39,
        "Spain": 140, 
        "Germany": 78,
        "Italy": 135,
        "France": 61,
    }
    return league_ids.get(country_name)

def get_season():
    return 2024

def get_teams(league_id):
    """Get teams from API or return sample data"""
    url = f"{BASE_URL}/teams"
    querystring = {"league": league_id, "season": get_season()}
    
    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        data = response.json()
        
        if response.status_code == 200 and 'response' in data and data['response']:
            return data['response']
        else:
            st.warning("Using sample team data (API limit reached or no data)")
            return get_sample_teams(league_id)
            
    except Exception as e:
        st.warning(f"Using sample team data: {e}")
        return get_sample_teams(league_id)

def get_sample_teams(league_id):
    """Sample data for demonstration"""
    sample_teams = {
        39: [{'team': {'id': 1, 'name': 'Manchester City'}}, 
              {'team': {'id': 2, 'name': 'Liverpool'}},
              {'team': {'id': 3, 'name': 'Arsenal'}}],
        140: [{'team': {'id': 4, 'name': 'Real Madrid'}},
               {'team': {'id': 5, 'name': 'Barcelona'}}],
        78: [{'team': {'id': 6, 'name': 'Bayern Munich'}},
              {'team': {'id': 7, 'name': 'Dortmund'}}],
        135: [{'team': {'id': 8, 'name': 'Inter Milan'}},
               {'team': {'id': 9, 'name': 'AC Milan'}}],
        61: [{'team': {'id': 10, 'name': 'PSG'}},
              {'team': {'id': 11, 'name': 'Marseille'}}]
    }
    return sample_teams.get(league_id, [])

def get_fixtures(league_id, next_n=10):
    """Get fixtures from API or return sample fixtures"""
    url = f"{BASE_URL}/fixtures"
    querystring = {"league": league_id, "season": get_season(), "next": next_n}
    
    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        data = response.json()
        
        if response.status_code == 200 and 'response' in data and data['response']:
            return data['response']
        else:
            st.warning("Using sample fixture data (API limit reached or no data)")
            return get_sample_fixtures(league_id)
            
    except Exception as e:
        st.warning(f"Using sample fixture data: {e}")
        return get_sample_fixtures(league_id)

def get_sample_fixtures(league_id):
    """Sample fixtures for demonstration"""
    from datetime import datetime, timedelta
    import random
    
    sample_teams = {
        39: ['Manchester City', 'Liverpool', 'Arsenal', 'Chelsea', 'Man United'],
        140: ['Real Madrid', 'Barcelona', 'Atletico Madrid', 'Sevilla'],
        78: ['Bayern Munich', 'Dortmund', 'RB Leipzig', 'Leverkusen'],
        135: ['Inter Milan', 'AC Milan', 'Juventus', 'Napoli'],
        61: ['PSG', 'Marseille', 'Lyon', 'Monaco']
    }
    
    teams = sample_teams.get(league_id, [])
    fixtures = []
    
    for i in range(5):
        home_team = random.choice(teams)
        away_team = random.choice([t for t in teams if t != home_team])
        
        fixture_date = (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%dT%H:%M:%S+00:00')
        
        fixtures.append({
            'fixture': {
                'date': fixture_date,
                'timestamp': int((datetime.now() + timedelta(days=i)).timestamp())
            },
            'teams': {
                'home': {'name': home_team},
                'away': {'name': away_team}
            }
        })
    
    return fixtures
