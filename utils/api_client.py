import requests
import pandas as pd
import streamlit as st

class FootballDataClient:
    def __init__(self):
        # Try to get the secrets from Streamlit Cloud. If running locally, use a fallback.
        try:
            self.api_key = st.secrets["API_FOOTBALL"]["KEY"]
            self.api_host = st.secrets["API_FOOTBALL"]["HOST"]
        except (KeyError, FileNotFoundError):
            # Fallback for local development (create a config.py file with these variables)
            try:
                from config import API_KEY, API_HOST
                self.api_key = API_KEY
                self.api_host = API_HOST
            except ImportError:
                self.api_key = None
                self.api_host = None
                print("API credentials not found. Please set up secrets.toml or config.py")

        self.base_url = "https://api-football-v1.p.rapidapi.com/v3"
        self.headers = {
            'x-rapidapi-key': self.api_key,
            'x-rapidapi-host': self.api_host
        } if self.api_key else {}

    def get_historical_fixtures(self, league_id, season, last_n_matches=10):
        """Fetches historical fixtures for all teams in a league for a season."""
        if not self.api_key:
            return {"error": "API credentials not configured"}
            
        url = f"{self.base_url}/fixtures"
        querystring = {"league": league_id, "season": season}
        try:
            response = requests.get(url, headers=self.headers, params=querystring)
            response.raise_for_status()
            return response.json()['response']
        except Exception as e:
            return {"error": str(e)}

    def get_team_statistics(self, team_id, league_id, season):
        """Fetches detailed statistics for a specific team in a league season."""
        if not self.api_key:
            return {"error": "API credentials not configured"}
            
        url = f"{self.base_url}/teams/statistics"
        querystring = {"team": team_id, "league": league_id, "season": season}
        try:
            response = requests.get(url, headers=self.headers, params=querystring)
            response.raise_for_status()
            return response.json()['response']
        except Exception as e:
            return {"error": str(e)}
