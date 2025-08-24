# utils/api_client.py
import requests
import pandas as pd
import streamlit as st
try:
    # Try to get the password from Streamlit's secure section
    API_KEY = st.secrets["API_FOOTBALL"]["KEY"]
    API_HOST = st.secrets["API_FOOTBALL"]["HOST"]
except:
    # If it's running on your computer, use the old file
    from config import API_KEY, API_HOST
class FootballDataClient:
    def __init__(self):
        self.base_url = "https://api-football-v1.p.rapidapi.com/v3"
        self.headers = {
            'x-rapidapi-key': API_KEY,
            'x-rapidapi-host': API_HOST
        }

    def get_historical_fixtures(self, league_id, season, last_n_matches=10):
        """Fetches historical fixtures for all teams in a league for a season."""
        url = f"{self.base_url}/fixtures"
        querystring = {"league": league_id, "season": season}
        response = requests.get(url, headers=self.headers, params=querystring)
        response.raise_for_status()  # Raises an error for bad status codes
        return response.json()['response']

    def get_team_statistics(self, team_id, league_id, season):
        """Fetches detailed statistics for a specific team in a league season."""
        url = f"{self.base_url}/teams/statistics"
        querystring = {"team": team_id, "league": league_id, "season": season}
        response = requests.get(url, headers=self.headers, params=querystring)
        response.raise_for_status()
        return response.json()['response']

# Example League IDs (You need to get these from the API documentation)
LEAGUE_IDS = {
    'England': 39,  # Premier League
    'France': 61,   # Ligue 1
    'Germany': 78,  # Bundesliga
    'Italy': 135,   # Serie A
    'Spain': 140    # La Liga
}
