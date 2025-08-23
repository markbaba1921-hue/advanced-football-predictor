# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.api_client import get_league_id, get_fixtures, get_teams
from utils.data_processor import calculate_team_strengths
from utils.predictor import predict_league_fixtures

# Page configuration
st.set_page_config(
    page_title="Advanced Football Predictor",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional look
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #FF4B4B;
        text-align: center;
        margin-bottom: 1rem;
    }
    .prediction-card {
        background-color: #F0F2F6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .score-display {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #FF4B4B;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">⚽ Advanced European Football Predictor</h1>', unsafe_allow_html=True)
st.markdown("### Predicting matches across top 5 European leagues with live data and machine learning")

# Sidebar
st.sidebar.header("⚙️ Settings")
selected_league = st.sidebar.selectbox(
    "Choose a League",
    ["England", "Spain", "Germany", "Italy", "France"],
    index=0
)

# Advanced filters
st.sidebar.header("🔍 Filters")
show_visualizations = st.sidebar.checkbox("Show Advanced Visualizations", value=True)
min_confidence = st.sidebar.slider("Minimum Confidence Level", 0, 100, 50)

# Function for visualizations
def create_advanced_visualizations(predictions_df):
    """Create interactive visualizations for predictions"""
    try:
        # Convert percentage strings to numbers
        df = predictions_df.copy()
        df['Home Win %'] = df['Home Win %'].str.replace('%', '').astype(float)
        df['Draw %'] = df['Draw %'].str.replace('%', '').astype(float)
        df['Away Win %'] = df['Away Win %'].str.replace('%', '').astype(float)
        df['BTTS %'] = df['BTTS %'].str.replace('%', '').astype(float)
        df['Over 2.5 %'] = df['Over 2.5 %'].str.replace('%', '').astype(float)
        
        # Create tabs for different visualizations
        tab1, tab2, tab3 = st.tabs(["Win Probabilities", "Expected Goals", "Betting Markets"])
        
        with tab1:
            # Win probability chart
            fig = px.bar(df, x='Match', y=['Home Win %', 'Draw %', 'Away Win %'],
                         title='📊 Match Outcome Probabilities', barmode='stack',
                         color_discrete_map={'Home Win %': '#FF4B4B', 'Draw %': '#2E86AB', 'Away Win %': '#00CC96'})
            fig.update_layout(showlegend=True, yaxis_title="Probability (%)")
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            # Expected goals scatter plot
            fig2 = px.scatter(df, x='Home xG', y='Away xG', text='Match',
                             title='⚽ Expected Goals Analysis', 
                             size='Over 2.5 %', color='Home Win %',
                             hover_data=['Most Likely Score', 'BTTS %'])
            fig2.update_traces(textposition='top center')
            fig2.update_layout(showlegend=True)
            st.plotly_chart(fig2, use_container_width=True)
        
        with tab3:
            # Betting markets analysis
            fig3 = px.scatter(df, x='BTTS %', y='Over 2.5 %', text='Match',
                             title='🎯 Both Teams to Score & Over 2.5 Goals Probability',
                             color='Home Win %', size='Home Win %')
            fig3.update_traces(textposition='top center')
            st.plotly_chart(fig3, use_container_width=True)
            
    except Exception as e:
        st.warning(f"Could not create visualizations: {e}")

# Main app logic
@st.cache_data(ttl=3600)
def load_league_data(league_name):
    league_id = get_league_id(league_name)
    
    teams_data = get_teams(league_id)
    team_stats = {team['team']['name']: None for team in teams_data}
    
    strengths = calculate_team_strengths(team_stats, league_id)
    fixtures = get_fixtures(league_id, next_n=10)
    
    return {
        'league_id': league_id,
        'teams': teams_data,
        'strengths': strengths,
        'fixtures': fixtures
    }

# Load data with progress
with st.spinner(f"📡 Loading {selected_league} league data..."):
    league_data = load_league_data(selected_league)

if league_data['fixtures']:
    with st.spinner("🧠 Calculating predictions with AI..."):
        predictions = predict_league_fixtures(league_data['fixtures'], league_data['strengths'])
    
    # Prepare data for display
    prediction_rows = []
    for pred in predictions:
        fixture = pred['fixture']
        home_team = fixture['teams']['home']['name']
        away_team = fixture['teams']['away']['name']
        
        prediction_rows.append({
            'Match': f"{home_team} vs {away_team}",
            'Most Likely Score': pred['most_likely_score'],
            'Home Win %': f"{pred['home_win']}%",
            'Draw %': f"{pred['draw']}%",
            'Away Win %': f"{pred['away_win']}%",
            'BTTS %': f"{pred['btts_prob']}%",
            'Over 2.5 %': f"{pred['over_25_prob']}%",
            'Home xG': pred['home_xG'],
            'Away xG': pred['away_xG'],
            'Confidence': pred.get('confidence', 'high')
        })
    
    # Create DataFrame
    df = pd.DataFrame(prediction_rows)
    
    # Display predictions
    st.header(f"📅 Upcoming {selected_league} League Predictions")
    
    # Show most likely score in a prominent card
    if not df.empty:
        most_likely_match = df.iloc[0]
        st.markdown(f"""
        <div class="prediction-card">
            <h3>🔥 Match of the Day</h3>
            <h4>{most_likely_match['Match']}</h4>
            <div class="score-display">{most_likely_match['Most Likely Score']}</div>
            <p>Home Win: {most_likely_match['Home Win %']} | Draw: {most_likely_match['Draw %']} | Away Win: {most_likely_match['Away Win %']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Display all predictions in a dataframe
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Advanced visualizations
    if show_visualizations:
        st.header("📈 Advanced Analytics")
        create_advanced_visualizations(df)
    
    # Team strength rankings
    st.header("🏆 Team Strength Rankings")
    strength_rows = []
    for team_name, (attack, defense) in league_data['strengths'].items():
        strength_rows.append({
            'Team': team_name,
            'Attack Strength': round(attack, 2),
            'Defense Strength': round(defense, 2),
            'Overall Rating': round((attack + defense) / 2, 2)
        })
    
    strength_df = pd.DataFrame(strength_rows).sort_values('Overall Rating', ascending=False)
    st.dataframe(strength_df, use_container_width=True, hide_index=True)
    
    # Download button
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download Predictions (CSV)",
        data=csv,
        file_name=f"{selected_league}_predictions.csv",
        mime="text/csv"
    )
    
else:
    st.warning("⚠️ No upcoming fixtures found. This could be due to:")
    st.info("""
    - Season hasn't started yet
    - International break
    - Data source temporarily unavailable
    - Try selecting a different league
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>⚡ Powered by Machine Learning & Poisson Distribution Models</p>
    <p>📊 Data sources: Live web scraping & statistical analysis</p>
    <p>🎯 For demonstration purposes only</p>
</div>
""", unsafe_allow_html=True)
