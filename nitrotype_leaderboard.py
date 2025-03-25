import requests
import pandas as pd
from datetime import datetime
import time

TEAM_TAGS = [
    "PR2W", "NTPD1", "SSH", "BEEHVE", "RFTP", "S0RC", "TCHR", "NTO", "P1RE",
    "CAM0", "NCT", "PSR", "N8TE", "FASZ", "SER", "T0WER", "ZH", "LOVGOD", "DLX",
    "RVNT", "RIV4L", "FAM3", "RZ", "EXOTIC", "RI5E", "VFU", "SNTL", "SAIL", "HONT",
    "NTRS34", "NTT", "2VCTRY", "T3X5", "ST0RM", "DUAL", "AMPX", "TNGN", "ZSH", "VLN",
    "CATPLT", "4cu", "BRAVE", "NS7", "WTRMN", "AL0N3D", "NI1TRO", "LOFH", "DIV1",
    "NTW", "LLJ4R", "UNREST", "NGREEN", "TRUST", "GSGMWO", "LSH", "HZE", "BAYLOR",
    "OVCR", "LTC", "SG1MAS", "XWX", "FERARI", "DCPTCN", "RL1", "RL", "AL3", "HELIUM",
    "NTP444", "SSNAKS", "NHS", "DOGGIS", "2S", "0PT", "ESTER", "ASPN", "50I", "MED13L",
    "FLAGZ", "JTAU", "W2V", "WPMWPM", "SZM", "4EP", "TGNM", "ZTAGZ", "PIGFLY", "KR0W",
    "TOTUF7", "F0J", "D4RKER", "TALK", "VXL", "LE4GUE", "TWO", "FUZHOU", "SK4P", "VTI",
    "GLZ", "B0MBA", "KAPOK", "ERC", "SPRME", "BMW", "NT20", "NT", "CYCV", "PTB", "XS9",
    "KBSM", "190IQ", "PCMSG", "FRLB", "ZER0SE", "PR2WX", "CZBZ", "M1NE", "NTM", "MEYBO",
    "LXW"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "application/json",
}

def get_team_data(team_tag, retries=3, delay=5):
    """Fetch season data and stats from the API for a team."""
    url = f"https://www.nitrotype.com/api/v2/teams/{team_tag}"
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=HEADERS, timeout=10, verify=True)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'OK':
                    season = data['results'].get('season', [])
                    stats = data['results'].get('stats', [])
                    return season, stats
            return [], []
        except Exception as e:
            print(f"Error fetching data for team {team_tag}: {e}")
            time.sleep(delay)
    return [], []

def get_team_stats(stats):
    """Extract relevant stats from 'board: season'."""
    for stat in stats:
        if stat.get('board') == 'season':
            return {
                'typed': int(stat.get('typed', 0)),  # Convert to integer
                'secs': int(stat.get('secs', 0)),    # Convert to integer
                'played': int(stat.get('played', 0)),  # Convert to integer
                'errs': int(stat.get('errs', 0))    # Convert to integer
            }
    return {'typed': 0, 'secs': 0, 'played': 0, 'errs': 0}

def calculate_wpm(typed, secs):
    """Calculate WPM (words per minute) from typed characters and seconds."""
    return (typed / 5) / (secs / 60) if secs > 0 else 0

def calculate_points(wpm, accuracy, races):
    """Calculate total points using the formula per race."""
    return (100 + (wpm / 2)) * accuracy * races

def calculate_accuracy(typed, errs):
    """Calculate accuracy as a percentage."""
    return (typed - errs) / typed if typed > 0 else 0

# Save the timestamp of the script execution
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open("timestamp.txt", "w") as file:
    file.write(f"Last Updated: {timestamp}")

all_players = []
team_summary = {}  # Store team stats

for team_tag in TEAM_TAGS:
    season_data, stats_data = get_team_data(team_tag)
    if not season_data:
        print(f"No seasonal data found for team {team_tag}")
        continue

    # Extract team stats from 'board: season'
    team_stats = get_team_stats(stats_data)
    typed = team_stats['typed']
    secs = team_stats['secs']
    played = team_stats['played']
    errs = team_stats['errs']

    # Calculate team-level WPM, accuracy, and total points
    accuracy = calculate_accuracy(typed, errs)
    wpm = calculate_wpm(typed, secs)
    points = calculate_points(wpm, accuracy, played)

    team_summary[team_tag] = {
        'Team': team_tag,
        'TotalPoints': points,
        'Racers': sum(1 for player in season_data if player.get('points') is not None),
        'Races': played
    }

    # Process individual players
    for member in season_data:
        if member.get('points') is not None:
            username = member.get('username', 'N/A')
            display_name = member.get('displayName', 'N/A')
            profile_link = f"https://www.nitrotype.com/racer/{username}"
            title = member.get('title', 'N/A')
            car_id = member.get('carID', 0)
            hue_angle = member.get('carHueAngle', 0)

            points = member.get('points', 0)
            typed = int(member.get('typed', 0))  # Convert to integer
            errs = int(member.get('errs', 0))    # Convert to integer
            races = int(member.get('played', 0)) # Convert to integer

            accuracy = calculate_accuracy(typed, errs)
            speed = calculate_wpm(typed, secs)

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

    timestamp_filename = datetime.now().strftime("%Y%m%d")
    df.to_csv(f'nitrotype_season_leaderboard_{timestamp_filename}.csv', index=False)

    df_teams = pd.DataFrame(list(team_summary.values()))
    df_teams = df_teams.sort_values(by='TotalPoints', ascending=False)
    df_teams.to_csv(f'nitrotype_team_leaderboard_{timestamp_filename}.csv', index=False)
