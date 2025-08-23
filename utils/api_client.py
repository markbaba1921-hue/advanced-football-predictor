def get_teams(league_id):
    url = f"{BASE_URL}/teams"
    querystring = {"league": league_id, "season": get_season()}
    try:
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
        if data['results'] > 0:  # <--- This is the problematic line
            return data['response']
        else:
            return []
    except Exception as e:
        st.error(f"Error fetching teams: {e}")
        return []
