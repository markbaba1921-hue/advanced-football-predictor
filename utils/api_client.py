def get_teams(league_id):
    url = f"{BASE_URL}/teams"
    querystring = {"league": league_id, "season": get_season()}
    try:
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
        # Check if the 'response' key exists and has data
        if 'response' in data and data['response']:
            return data['response']
        else:
            return []
    except Exception as e:
        st.error(f"Error fetching teams: {e}")
        return []
