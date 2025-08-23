# app.py
import streamlit as st
import pandas as pd
from utils.api_client import FootballDataClient, LEAGUE_IDS
from utils.predictor import Predictor
from utils.data_processor import DataProcessor

# Page config
st.set_page_config(page_title="Elite Football Predictor", layout="wide")
st.title("⚽ Elite Football Predictor")
st.markdown("Predict outcomes for the top 5 European leagues.")

# Initialize clients and predictors
predictor = Predictor()
data_processor = DataProcessor()
# api_client = FootballDataClient() # Uncomment when you have API keys

# --- Sidebar for Input ---
st.sidebar.header("Fixture Selector")
selected_league = st.sidebar.selectbox("Select League", list(LEAGUE_IDS.keys()))
selected_home_team = st.sidebar.selectbox("Home Team", ["Manchester City", "Bayern Munich", "PSG", "..."] ) # Populate from API
selected_away_team = st.sidebar.selectbox("Away Team", ["Liverpool", "Borussia Dortmund", "Marseille", "..."])

predict_button = st.sidebar.button("Predict Outcome!")

# --- Main Area for Output ---
if predict_button:
    with st.spinner('Crunching the data... Please wait.'):
        # 1. Prepare the data for the selected teams
        # In a real app, this would use the `api_client` to get LIVE data
        features_df = data_processor.prepare_prediction_data(selected_home_team, selected_away_team)
        
        # 2. Get the prediction
        most_likely, probabilities = predictor.predict(features_df)
        
        # 3. Display the results in a professional way
        st.success("Prediction Complete!")
        
        col1, col2, col3 = st.columns(3)
        
        # Home Win Column
        with col1:
            percent_home = probabilities.get('1', 0) * 100
            st.metric(label=f"{selected_home_team} Win", value=f"{percent_home:.1f}%")
            st.progress(percent_home / 100)
        
        # Draw Column
        with col2:
            percent_draw = probabilities.get('X', 0) * 100
            st.metric(label="Draw", value=f"{percent_draw:.1f}%")
            st.progress(percent_draw / 100)
        
        # Away Win Column
        with col3:
            percent_away = probabilities.get('2', 0) * 100
            st.metric(label=f"{selected_away_team} Win", value=f"{percent_away:.1f}%")
            st.progress(percent_away / 100)
        
        # Show the most likely outcome
        if most_likely == '1':
            st.subheader(f"Predicted Outcome: **{selected_home_team} Wins**")
        elif most_likely == '2':
            st.subheader(f"Predicted Outcome: **{selected_away_team} Wins**")
        else:
            st.subheader(f"Predicted Outcome: **Draw**")

# --- Section to show league tables or upcoming fixtures ---
st.header(f"🏆 {selected_league} Overview")
# Here you could use api_client to get and display a league table or next fixtures
# df = pd.DataFrame(...)
# st.dataframe(df)
