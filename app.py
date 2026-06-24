import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="2026 World Cup Analyzer", page_icon="🏆", layout="centered")
st.title("🏆 2026 World Cup Group Stage Simulator")
st.markdown("Welcome to your interactive World Cup standings dashboard! This app processes live match data and calculates group rankings automatically.")

raw_data = """Round,Day,Date,Time,GH,GA,Referee,Notes,Year,home_team,away_team
Group stage,Thu,2026-06-11,13:00 (22:00),2,0,,,2026,Mexico,South Africa
Group stage,Thu,2026-06-11,20:00 (05:00),2,1,,,2026,Korea Republic,Czechia
Group stage,Fri,2026-06-12,15:00 (22:00),1,1,,,2026,Canada,Bosnia-Herzegovina
Group stage,Fri,2026-06-12,18:00 (04:00),4,1,,,2026,United States,Paraguay
Group stage,Sat,2026-06-13,12:00 (22:00),1,1,,,2026,Qatar,Switzerland
Group stage,Sat,2026-06-13,18:00 (01:00),1,1,,,2026,Brazil,Morocco
Group stage,Sat,2026-06-13,21:00 (04:00),0,1,,,2026,Haiti,Scotland
Group stage,Sat,2026-06-13,21:00 (07:00),2,0,,,2026,Australia,Türkiye
Group stage,Sun,2026-06-14,12:00 (20:00),7,1,,,2026,Germany,Curaçao
Group stage,Sun,2026-06-14,15:00 (23:00),2,2,,,2026,Netherlands,Japan
Group stage,Sun,2026-06-14,19:00 (02:00),1,0,,,2026,Côte d'Ivoire,Ecuador
Group stage,Sun,2026-06-14,20:00 (05:00),5,1,,,2026,Sweden,Tunisia
Group stage,Mon,2026-06-15,12:00 (22:00),1,1,,,2026,Belgium,Egypt
Group stage,Mon,2026-06-15,12:00 (19:00),0,0,,,2026,Spain,Cape Verde
Group stage,Mon,2026-06-15,18:00 (04:00),2,2,,,2026,IR Iran,New Zealand
Group stage,Mon,2026-06-15,18:00 (01:00),1,1,,,2026,Saudi Arabia,Uruguay
Group stage,Tue,2026-06-16,15:00 (22:00),3,1,,,2026,France,Senegal
Group stage,Tue,2026-06-16,18:00 (01:00),1,4,,,2026,Iraq,Norway
Group stage,Tue,2026-06-16,20:00 (04:00),3,0,,,2026,Argentina,Algeria
Group stage,Tue,2026-06-16,21:00 (07:00),3,1,,,2026,Austria,Jordan
Group stage,Wed,2026-06-17,12:00 (20:00),1,1,,,2026,Portugal,Congo DR
Group stage,Wed,2026-06-17,15:00 (23:00),4,2,,,2026,England,Croatia
Group stage,Wed,2026-06-17,19:00 (02:00),1,0,,,2026,Ghana,Panama
Group stage,Wed,2026-06-17,20:00 (05:00),3,1,,,2026,Uzbekistan,Colombia
Group stage,Thu,2026-06-18,12:00 (19:00),1,1,,,2026,Czechia,South Africa
Group stage,Thu,2026-06-18,12:00 (22:00),4,1,,,2026,Switzerland,Bosnia-Herzegovina
Group stage,Thu,2026-06-18,15:00 (01:00),6,0,,,2026,Canada,Qatar
Group stage,Thu,2026-06-18,19:00 (04:00),1,0,,,2026,Mexico,Korea Republic
Group stage,Fri,2026-06-19,12:00 (22:00),2,0,,,2026,United States,Australia
Group stage,Fri,2026-06-19,18:00 (01:00),0,1,,,2026,Scotland,Morocco
Group stage,Fri,2026-06-19,20:00 (06:00),0,1,,,2026,Türkiye,Paraguay
Group stage,Fri,2026-06-19,20:30 (03:30),3,0,,,2026,Brazil,Haiti
Group stage,Sat,2026-06-20,12:00 (20:00),5,1,,,2026,Netherlands,Sweden
Group stage,Sat,2026-06-20,16:00 (23:00),2,1,,,2026,Germany,Côte d'Ivoire
Group stage,Sat,2026-06-20,19:00 (03:00),0,0,,,2026,Ecuador,Curaçao
Group stage,Sat,2026-06-20,22:00 (07:00),0,4,,,2026,Tunisia,Japan
Group stage,Sun,2026-06-21,12:00 (19:00),4,0,,,2026,Spain,Saudi Arabia
Group stage,Sun,2026-06-21,12:00 (22:00),0,0,,,2026,Belgium,IR Iran
Group stage,Sun,2026-06-21,18:00 (01:00),2,2,,,2026,Uruguay,Cape Verde
Group stage,Sun,2026-06-21,18:00 (04:00),1,3,,,2026,New Zealand,Egypt
Group stage,Mon,2026-06-22,12:00 (20:00),2,0,,,2026,Argentina,Austria
Group stage,Mon,2026-06-22,17:00 (00:00),3,0,,,2026,France,Iraq
Group stage,Mon,2026-06-22,20:00 (03:00),3,2,,,2026,Norway,Senegal
Group stage,Mon,2026-06-22,20:00 (06:00),1,2,,,2026,Jordan,Algeria
Group stage,Tue,2026-06-23,12:00 (20:00),5,0,,,2026,Portugal,Uzbekistan
Group stage,Tue,2026-06-23,16:00 (23:00),0,0,,,2026,England,Ghana
"""

df = pd.read_csv(io.StringIO(raw_data))
df = df.dropna(subset=["GH", "GA"])
df["GH"] = df["GH"].astype(int)
df["GA"] = df["GA"].astype(int)

teams = {}
for _, row in df.iterrows():
    home, away = row["home_team"], row["away_team"]
    gh, ga = row["GH"], row["GA"]
    for t in [home, away]:
        if t not in teams:
            teams[t] = {"PTS": 0, "GF": 0, "GA": 0}
    teams[home]["GF"] += gh
    teams[home]["GA"] += ga
    teams[away]["GF"] += ga
    teams[away]["GA"] += gh
    if gh > ga:
        teams[home]["PTS"] += 3
    elif gh < ga:
        teams[away]["PTS"] += 3
    else:
        teams[home]["PTS"] += 1
        teams[away]["PTS"] += 1

standings = pd.DataFrame.from_dict(teams, orient="index").reset_index()
standings.rename(columns={"index": "Team"}, inplace=True)
standings["GD"] = standings["GF"] - standings["GA"]

groups = {
    "Group A": ["Mexico", "South Africa", "Korea Republic", "Czechia"],
    "Group B": ["Canada", "Bosnia-Herzegovina", "Qatar" ,  "Switzerland" ],
    "Group C": ["Haiti", "Scotland", "Brazil", "Morocco"],
    "Group D": ["United States" , "Paraguay", "Australia", "Türkiye"],
    "Group E": ["Germany", "Curaçao","Côte d'Ivoire", "Ecuador" ],
    "Group F": ["Netherlands", "Japan", "Sweden", "Tunisia"],
    "Group G": ["Belgium", "Egypt","IR Iran", "New Zealand" ],
    "Group H": ["Spain", "Cape Verde", "Saudi Arabia", "Uruguay"],
    "Group I": ["France", "Senegal", "Iraq", "Norway"],
    "Group J": ["Argentina", "Algeria", "Austria", "Jordan"],
    "Group K": ["Portugal", "Congo DR", "Uzbekistan", "Colombia"],
    "Group L": ["England", "Croatia","Ghana", "Panama"],
}


st.header("🔍 Explore Group Standings")
selected_group = st.selectbox("Choose a Group to display:", list(groups.keys()))

if selected_group:
    team_list = groups[selected_group]
    group_df = standings[standings["Team"].isin(team_list)].copy()
    group_df = group_df.sort_values(
        by=["PTS", "GD", "GF", "GA"], ascending=[False, False, False, False]
    ).reset_index(drop=True)
    
    st.subheader(f"📊 Live Standings: {selected_group}")
    st.dataframe(group_df[["Team", "PTS", "GD", "GF", "GA"]], use_container_width=True)

st.divider()

st.header("⚽ Team Statistics Lookup")
all_teams_list = sorted(standings["Team"].unique())
selected_team = st.selectbox("Select a Team to view its tournament summary:", all_teams_list)

if selected_team:
    team_stats = standings[standings["Team"] == selected_team].iloc[0]
    
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label="Points (PTS)", value=int(team_stats["PTS"]))
    col2.metric(label="Goal Difference (GD)", value=int(team_stats["GD"]))
    col3.metric(label="Goals For (GF)", value=int(team_stats["GF"]))
    col4.metric(label="Goals Against (GA)", value=int(team_stats["GA"]))

st.divider()

# --- NEW SECTION: CUSTOM ANALYTICAL VIEWS ---
st.header("📋 Advanced Tournament Leaderboards")
st.markdown("Use the selector below to filter and analyze unified standings across different categories.")

# Create a selection menu for the user
view_option = st.selectbox(
    "Select a view:",
    [
        "📊 Overall Standings (All 48 Teams)",
        "⭐ Arab Nations Standings",
        "🕒 3rd-Place Teams Tracker (Top 8 Qualify)"
    ]
)

# ----------------- VIEW 1: OVERALL STANDINGS -----------------
if view_option == "📊 Overall Standings (All 48 Teams)":
    st.subheader("🌍 Universal Leaderboard")
    
    overall_df = standings.sort_values(by=['PTS', 'GD', 'GF'], ascending=[False, False, False]).reset_index(drop=True)
    overall_df.index = overall_df.index + 1
    overall_df.index.name = "Rank"
    
    st.dataframe(overall_df[['Team', 'PTS', 'GD', 'GF', 'GA']], use_container_width=True)

# ----------------- VIEW 2: ARAB NATIONS STANDINGS -----------------
elif view_option == "⭐ Arab Nations Standings":
    st.subheader("🇲🇦 🇩🇿 划🇸🇦 Regional Leaderboard: Arab Nations")
    
    arab_teams_list = ['Algeria', 'Morocco', 'Saudi Arabia', 'Egypt', 'Tunisia', 'Qatar', 'Jordan', 'Iraq']
    arab_df = standings[standings['Team'].isin(arab_teams_list)].copy()
    
    if not arab_df.empty:
        arab_df = arab_df.sort_values(by=['PTS', 'GD', 'GF'], ascending=[False, False, False]).reset_index(drop=True)
        arab_df.index = arab_df.index + 1
        arab_df.index.name = "Rank"
        st.dataframe(arab_df[['Team', 'PTS', 'GD', 'GF', 'GA']], use_container_width=True)
    else:
        st.info("No stats available for Arab nations yet.")

# ----------------- VIEW 3: 3RD PLACE TRACKER (TOP 8 QUALIFY) -----------------
elif view_option == "🕒 3rd-Place Teams Tracker (Top 8 Qualify)":
    st.subheader("🎟️ Best 3rd-Placed Teams Leaderboard")
    st.markdown("In the 48-team format, the **top 8 best third-placed teams** advance to the Round of 32.")
    
    third_placed_teams = []
    for g_name, g_teams in groups.items():
        g_df = standings[standings['Team'].isin(g_teams)].copy()
        g_df = g_df.sort_values(by=['PTS', 'GD', 'GF', 'GA'], ascending=[False, False, False, False]).reset_index(drop=True)
        if len(g_df) >= 3:
            third_placed_teams.append(g_df.iloc[2])
            
    if third_placed_teams:
        third_df = pd.DataFrame(third_placed_teams).sort_values(by=['PTS', 'GD', 'GF'], ascending=[False, False, False]).reset_index(drop=True)
        third_df.index = third_df.index + 1
        third_df.index.name = "Rank"
        
        third_df['Status'] = ['✅ Qualified (Top 8)' if i <= 8 else '❌ Eliminated' for i in third_df.index]
        
        def highlight_qualified(row):
            return ['background-color: #d4edda; color: #155724;' if row['Status'] == '✅ Qualified (Top 8)' else '' for _ in row]
            
        styled_third_df = third_df[['Team', 'PTS', 'GD', 'GF', 'GA', 'Status']].style.apply(highlight_qualified, axis=1)
        
        st.dataframe(styled_third_df, use_container_width=True)
    else:
        st.info("Group stage matches are incomplete. 3rd-place data will generate once groups populate.")

st.divider()
st.header("📊 Tournament Leaderboards")
col_attack, col_defense = st.columns(2)

with col_attack:
    st.subheader("🔥 Top 5 Attacks")
    top_attacks = standings.nlargest(5, 'GF')[['Team', 'GF', 'PTS']]
    top_attacks.index = range(1, 6)
    st.dataframe(top_attacks, use_container_width=True)

with col_defense:
    st.subheader("🛡️ Top 5 Defenses")
    top_defenses = standings.nsmallest(5, 'GA')[['Team', 'GA', 'PTS']]
    top_defenses.index = range(1, 6)
    st.dataframe(top_defenses, use_container_width=True)


