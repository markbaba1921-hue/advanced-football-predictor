import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from utils.predictor import Predictor
from utils.data_processor import DataProcessor

# Page config
st.set_page_config(page_title="Elite Football Predictor", layout="wide")
st.title("⚽ Elite Football Predictor Pro")
st.markdown("### Professional Football Predictions for Top European Leagues")

# Initialize predictor
predictor = Predictor()
data_processor = DataProcessor()

# League information
LEAGUES = {
    'Premier League': {'id': 39, 'country': 'England', 'logo': '🏴󠁧󠁢󠁥󠁮󠁧󠁿'},
    'La Liga': {'id': 140, 'country': 'Spain', 'logo': '🇪🇸'},
    'Serie A': {'id': 135, 'country': 'Italy', 'logo': '🇮🇹'},
    'Bundesliga': {'id': 78, 'country': 'Germany', 'logo': '🇩🇪'},
    'Ligue 1': {'id': 61, 'country': 'France', 'logo': '🇫🇷'}
}

# Sidebar for league selection
st.sidebar.header("📊 League Selection")
selected_league_name = st.sidebar.selectbox(
    "Choose League",
    list(LEAGUES.keys()),
    index=0
)

selected_league = LEAGUES[selected_league_name]

# Generate sample match data for the next 7 days
def generate_sample_fixtures(league_name, num_matches=10):
    teams = {
        'Premier League': ['Manchester City', 'Liverpool', 'Arsenal', 'Chelsea', 'Manchester United', 
                          'Tottenham', 'Newcastle', 'Aston Villa', 'West Ham', 'Brighton'],
        'La Liga': ['Real Madrid', 'Barcelona', 'Atletico Madrid', 'Sevilla', 'Valencia',
                   'Villarreal', 'Real Sociedad', 'Athletic Bilbao', 'Betis', 'Osasuna'],
        'Serie A': ['Inter Milan', 'AC Milan', 'Juventus', 'Napoli', 'Roma',
                   'Lazio', 'Atalanta', 'Fiorentina', 'Bologna', 'Torino'],
        'Bundesliga': ['Bayern Munich', 'Borussia Dortmund', 'RB Leipzig', 'Bayer Leverkusen',
                      'Wolfsburg', 'Eintracht Frankfurt', 'Borussia Mönchengladbach', 'Freiburg'],
        'Ligue 1': ['PSG', 'Marseille', 'Lyon', 'Monaco', 'Lille',
                   'Rennes', 'Nice', 'Lens', 'Reims', 'Nantes']
    }
    
    fixtures = []
    today = datetime.now()
    
    for i in range(num_matches):
        match_date = today + timedelta(days=i % 7)
        home_team = teams[league_name][i % len(teams[league_name])]
        away_team = teams[league_name][(i + 1) % len(teams[league_name])]
        
        fixtures.append({
            'Date': match_date.strftime('%Y-%m-%d'),
            'Time': f"{(15 + i % 6):02d}:00",
            'Home Team': home_team,
            'Away Team': away_team,
            'League': league_name
        })
    
    return pd.DataFrame(fixtures)

# Main content
st.header(f"{selected_league['logo']} {selected_league_name} Predictions")

# Generate and display fixtures
fixtures_df = generate_sample_fixtures(selected_league_name, 15)
st.subheader("📅 Upcoming Matches & Predictions")

# Display each match with predictions
for _, match in fixtures_df.iterrows():
    with st.container():
        col1, col2, col3, col4 = st.columns([1, 2, 1, 3])
        
        with col1:
            st.write(f"**{match['Date']}**")
            st.write(match['Time'])
        
        with col2:
            st.write(f"**{match['Home Team']}** vs **{match['Away Team']}**")
        
        with col3:
            if st.button("Predict", key=f"btn_{match['Home Team']}_{match['Away Team']}"):
                # Prepare data and get prediction
                features_df = data_processor.prepare_prediction_data(
                    match['Home Team'], 
                    match['Away Team']
                )
                most_likely, probabilities = predictor.predict(features_df)
                
                # Store in session state
                st.session_state[f"pred_{match['Home Team']}_{match['Away Team']}"] = {
                    'most_likely': most_likely,
                    'probabilities': probabilities
                }
        
        with col4:
            prediction_key = f"pred_{match['Home Team']}_{match['Away Team']}"
            if prediction_key in st.session_state:
                pred = st.session_state[prediction_key]
                
                # Display probabilities
                col41, col42, col43 = st.columns(3)
                with col41:
                    st.metric("Home Win", f"{pred['probabilities']['1']*100:.1f}%")
                with col42:
                    st.metric("Draw", f"{pred['probabilities']['X']*100:.1f}%")
                with col43:
                    st.metric("Away Win", f"{pred['probabilities']['2']*100:.1f}%")
                
                # Show predicted outcome
                if pred['most_likely'] == '1':
                    st.success(f"**Predicted: {match['Home Team']} Wins**")
                elif pred['most_likely'] == '2':
                    st.success(f"**Predicted: {match['Away Team']} Wins**")
                else:
                    st.info("**Predicted: Draw**")
            else:
                st.write("Click Predict to see forecast")

        st.markdown("---")

# League standings section
st.header("🏆 Current League Standings")

# Generate sample standings
def generate_standings(league_name):
    teams = {
        'Premier League': ['Manchester City', 'Liverpool', 'Arsenal', 'Chelsea', 'Manchester United', 
                          'Tottenham', 'Newcastle', 'Aston Villa', 'West Ham', 'Brighton'],
        'La Liga': ['Real Madrid', 'Barcelona', 'Atletico Madrid', 'Sevilla', 'Valencia',
                   'Villarreal', 'Real Sociedad', 'Athletic Bilbao', 'Betis', 'Osasuna'],
        'Serie A': ['Inter Milan', 'AC Milan', 'Juventus', 'Napoli', 'Roma',
                   'Lazio', 'Atalanta', 'Fiorentina', 'Bologna', 'Torino'],
        'Bundesliga': ['Bayern Munich', 'Borussia Dortmund', 'RB Leipzig', 'Bayer Leverkusen',
                      'Wolfsburg', 'Eintracht Frankfurt', 'Borussia Mönchengladbach', 'Freiburg'],
        'Ligue 1': ['PSG', 'Marseille', 'Lyon', 'Monaco', 'Lille',
                   'Rennes', 'Nice', 'Lens', 'Reims', 'Nantes']
    }
    
    standings = []
    for i, team in enumerate(teams[league_name]):
        standings.append({
            'Position': i + 1,
            'Team': team,
            'Played': 20,
            'Won': 15 - i,
            'Drawn': 3,
            'Lost': 2 + i,
            'Goals For': 40 - i * 2,
            'Goals Against': 15 + i,
            'Goal Difference': 25 - i * 3,
            'Points': 48 - i * 3
        })
    
    return pd.DataFrame(standings)

# Display standings
standings_df = generate_standings(selected_league_name)
st.dataframe(standings_df, use_container_width=True, hide_index=True)

# Footer
st.markdown("---")
st.markdown("""
**Note:** This is a demonstration app using advanced statistical models. 
For real-time predictions with actual data, connect to a football API.
""")
