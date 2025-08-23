# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.api_client import get_league_id, get_fixtures, get_teams, get_team_statistics
from utils.data_processor import calculate_team_strengths
from utils.predictor import predict_league_fixtures, advanced_predict_match

st.set_page_config(
    page_title="Advanced Football Predictor",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("⚽ Advanced European Football Predictor")
st.markdown("Predicting matches across top 5 European leagues with live data")

st.sidebar.header("League Selection")
selected_league = st.sidebar.selectbox(
    "Choose a League",
    ["England", "Spain", "Germany", "Italy", "France"]
)

@st.cache_data(ttl=3600)
def load_league_data(league_name):
    league_id = get_league_id(league_name)
    
    teams_data = get_teams(league_id)
    team_stats = {}
    
    for team in teams_data:
        team_id = team['team']['id']
        team_name = team['team']['name']
        stats = get_team_statistics(league_id, team_id)
        team_stats[team_name] = stats
    
    strengths = calculate_team_strengths(team_stats, league_id)
    
    fixtures = get_fixtures(league_id, next_n=10)
    
    return {
        'league_id': league_id,
        'teams': teams_data,
        'strengths': strengths,
        'fixtures': fixtures
    }

with st.spinner(f"Loading {selected_league} league data..."):
    league_data = load_league_data(selected_league)

if league_data['fixtures']:
    predictions = predict_league_fixtures(league_data['fixtures'], league_data['strengths'])
    
    st.header(f"Upcoming {selected_league} League Predictions")
    
    prediction_rows = []
    for pred in predictions:
        fixture = pred['fixture']
        home_team = fixture['teams']['home']['name']
        away_team = fixture['teams']['away']['name']
        match_date = pd.to_datetime(fixture['fixture']['date']).strftime('%Y-%m-%d %H:%M')
        
        prediction_rows.append({
            'Date': match_date,
            'Match': f"{home_team} vs {away_team}",
            'Most Likely Score': pred['most_likely_score'],
            'Home Win %': f"{pred['home_win']:.1f}%",
            'Draw %': f"{pred['draw']:.1f}%",
            'Away Win %': f"{pred['away_win']:.1f}%",
            'BTTS %': f"{pred['btts_prob']:.1f}%",
            'Over 2.5 %': f"{pred['over_25_prob']:.1f}%"
        })
    
    df = pd.DataFrame(prediction_rows)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.header("Team Strength Rankings")
    strength_rows = []
    for team_name, (attack, defense) in league_data['strengths'].items():
        strength_rows.append({
            'Team': team_name,
            'Attack Strength': attack,
            'Defense Strength': defense,
            'Overall': (attack + defense) / 2
        })
    
    strength_df = pd.DataFrame(strength_rows).sort_values('Overall', ascending=False)
    st.dataframe(strength_df, use_container_width=True)
    
else:
    st.warning("No upcoming fixtures found or there was an error loading data.")

st.markdown("---")
st.caption("Data provided by API-FOOTBALL • Predictions based on Poisson distribution models • For demonstration purposes")
