import streamlit as st
import pandas as pd
import numpy as np  # Add this import if not already there
from utils.predictor import Predictor
from utils.data_processor import DataProcessor
import streamlit as st
import pandas as pd
from utils.predictor import Predictor
from utils.data_processor import DataProcessor

# Page config
st.set_page_config(page_title="Elite Football Predictor", layout="wide")
st.title("⚽ Elite Football Predictor")
st.markdown("Predict outcomes for the top 5 European leagues.")

# Initialize clients and predictors
predictor = Predictor()
data_processor = DataProcessor()

# League IDs
LEAGUE_IDS = {
    'England': 39,
    'France': 61,
    'Germany': 78,
    'Italy': 135,
    'Spain': 140
}

# Sample teams for each league
SAMPLE_TEAMS = {
    'England': ['Manchester City', 'Liverpool', 'Arsenal', 'Chelsea', 'Manchester United'],
    'France': ['PSG', 'Marseille', 'Lyon', 'Monaco', 'Lille'],
    'Germany': ['Bayern Munich', 'Borussia Dortmund', 'RB Leipzig', 'Bayer Leverkusen', 'Wolfsburg'],
    'Italy': ['Inter Milan', 'AC Milan', 'Juventus', 'Napoli', 'Roma'],
    'Spain': ['Real Madrid', 'Barcelona', 'Atletico Madrid', 'Sevilla', 'Valencia']
}

# --- Sidebar for Input ---
st.sidebar.header("Fixture Selector")
selected_league = st.sidebar.selectbox("Select League", list(LEAGUE_IDS.keys()))

# Get teams for selected league
teams = SAMPLE_TEAMS[selected_league]
selected_home_team = st.sidebar.selectbox("Home Team", teams)
selected_away_team = st.sidebar.selectbox("Away Team", [t for t in teams if t != selected_home_team])

predict_button = st.sidebar.button("Predict Outcome!", type="primary")

# --- Main Area for Output ---
if predict_button:
    with st.spinner('Crunching the data... Please wait.'):
        try:
            # 1. Prepare the data for the selected teams
            features_df = data_processor.prepare_prediction_data(selected_home_team, selected_away_team)
            
            # 2. Get the prediction
            most_likely, probabilities = predictor.predict(features_df)
            
            # 3. Display the results
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
                st.subheader(f"🎯 Predicted Outcome: **{selected_home_team} Wins**")
            elif most_likely == '2':
                st.subheader(f"🎯 Predicted Outcome: **{selected_away_team} Wins**")
            else:
                st.subheader(f"🎯 Predicted Outcome: **Draw**")
                
        except Exception as e:
            st.error(f"An error occurred during prediction: {str(e)}")

# --- League Information Section ---
st.header(f"🏆 {selected_league} Overview")
st.info("This is a demonstration app with sample data. Connect to a football API for real-time predictions.")

# Sample league table
sample_table = pd.DataFrame({
    'Position': range(1, 6),
    'Team': SAMPLE_TEAMS[selected_league],
    'Points': [68, 65, 60, 58, 55],
    'Form': ['WWLWD', 'WLWWW', 'DWLDW', 'WWDDL', 'LDWWW']
})

st.dataframe(sample_table, use_container_width=True)
