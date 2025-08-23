# utils/api_client.py
import requests
import pandas as pd
import streamlit as st

API_KEY = st.secrets["API_FOOTBALL"]["KEY"]
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
    return 2023

def get_teams(league_id):
    url = f"{BASE_URL}/teams"
    querystring = {"league": league_id, "season": get_season()}
    try:
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
        if data['results'] > 0:
            return data['response']
        else:
            return []
    except Exception as e:
        st.error(f"Error fetching teams: {e}")
        return []

def get_team_statistics(league_id, team_id):
    url = f"{BASE_URL}/teams/statistics"
    querystring = {"league": league_id, "season": get_season(), "team": team_id}
    try:
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
        return data['response']
    except Exception as e:
        st.error(f"Error fetching stats for team {team_id}: {e}")
        return None

def get_fixtures(league_id, next_n=10):
    url = f"{BASE_URL}/fixtures"
    querystring = {"league": league_id, "season": get_season(), "next": next_n}
    try:
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
        if data['results'] > 0:
            return data['response']
        else:
            return []
    except Exception as e:
        st.error(f"Error fetching fixtures: {e}")
        return []
