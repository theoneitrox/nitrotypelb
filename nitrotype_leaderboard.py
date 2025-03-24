import requests
import pandas as pd
from datetime import datetime
import time

TEAM_TAGS = [
    "PR2W", "NTPD1", "SSH", "BEEHVE", "RFTP", "S0RC", "TCHR", "NTO", "P1RE",
    "CAM0", "NCT", "PSR", "N8TE", "FASZ", "SER", "T0WER", "ZH", "LOVGOD", "DLX",
    "RVNT", "RIV4L", "FAM3", "RZ", "EXOTIC", "RI5E", "VFU", "SNTL", "SAIL", "HONT",
    "NTRS34", "NTT", "2VCTRY", "T3X5", "ST0RM", "DUAL", "AMPX", "TNGN", "ZSH", "VLN",
    "CATPLT", "STRGRI", "BRAVE", "NS7", "WTRMN", "LVR96", "NI1TRO", "LOFH", "DIV1",
    "NTW", "LLJ4R", "UNREST", "NGREEN", "TRUST", "GSGMWO", "LSH", "HZE", "BAYLOR",
    "OVCR", "LTC", "SG1MAS", "XWX", "FERARI", "DCPTCN", "RL1", "RL", "AL3", "HELIUM",
    "NTP444", "SSNAKS", "NHS", "DOGGIS", "2S", "0PT", "ESTER", "ASPN", "50I", "MED13L",
    "FLAGZ", "JTAU", "W2V", "WPMWPM", "SZM", "4EP", "TGNM", "ZTAGZ", "PIGFLY", "KR0W",
    "TOTUF7", "F0J", "D4RKER", "TALK", "VXL", "LE4GUE", "TWO", "FUZHOU", "SK4P", "VTI",
    "GLZ", "B0MBA", "KAPOK", "ERC", "SPRME", "BMW", "NT20", "NT", "CYCV", "PTB", "XS9",
    "KBSM", "190IQ", "PCMSG", "FRLB", "ZER0SE", "PR2WX", "CZBZ", "M1NE", "P1NKS", "MEYBO",
    "LXW"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "application/json",
}

def get_season_stats(team_tag, retries=3, delay=5):
    url = f"https://www.nitrotype.com/api/v2/teams/{team_tag}"
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=HEADERS, timeout=10, verify=True)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'OK' and 'season' in data['results']:
                    return data['results']['season']
            return []
        except Exception as e:
            print(f"Error fetching data for team {team_tag}: {e}")
            time.sleep(delay)
    return []

def calculate_accuracy(typed, errs):
    return (typed - errs) / typed if typed > 0 else 0

def calculate_speed(points, accuracy, races):
    if accuracy > 0 and races > 0:
        wpm = (((points / races) / accuracy) - 100) * 2
        return wpm
    return 0

all_players = []
for team_tag in TEAM_TAGS:
    season_data = get_season_stats(team_tag)
    if not season_data:
        print(f"No seasonal data found for team {team_tag}")
        continue

    for member in season_data:
        if member.get('points') is not None:
            username = member.get('username', 'N/A')
            display_name = member.get('displayName', 'N/A')
            profile_link = f"https://www.nitrotype.com/racer/{username}"
            title = member.get('title', 'N/A')
            car_id = member.get('carID', 0)
            hue_angle = member.get('carHueAngle', 0)

            points = member.get('points', 0)
            typed = member.get('typed', 0)
            errs = member.get('errs', 0)
            races = member.get('played', 0)

            accuracy = calculate_accuracy(typed, errs)
            speed = calculate_speed(points, accuracy, races)

            all_players.append({
                'Username': username,
                'ProfileLink': profile_link,
                'DisplayName': display_name,
                'Title': title,
                'CarID': car_id,
                'CarHueAngle': hue_angle,
                'Speed': speed,
                'Races': races,
                'Points': points,
                'Accuracy': accuracy * 100,
                'Team': team_tag
            })

if not all_players:
    print("No valid player data found. Please verify the team tags and API responses.")
else:
    df = pd.DataFrame(all_players)
    df = df.sort_values(by='Points', ascending=False)

    timestamp = datetime.now().strftime("%Y%m%d")
    df.to_csv(f'nitrotype_season_leaderboard_{timestamp}.csv', index=False)

    team_totals = {}
    for player in all_players:
        team = player['Team']
        if team not in team_totals:
            team_totals[team] = 0
        team_totals[team] += player['Points']

    df_teams = pd.DataFrame([{'Team': t, 'TotalPoints': v} for t, v in team_totals.items()])
    df_teams = df_teams.sort_values(by='TotalPoints', ascending=False)
    df_teams.to_csv(f'nitrotype_team_leaderboard_{timestamp}.csv', index=False)