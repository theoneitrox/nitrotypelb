# NitroType Season Leaderboards

This repository contains two main components:

1. **Python Script:**  
   A script to fetch seasonal statistics from the NitroType API for a predefined list of team tags. It processes player data to calculate additional metrics (like accuracy and speed) and generates two CSV files:
   - A player leaderboard sorted by Points (highest first).
   - A team leaderboard that aggregates points for each team.
   
2. **HTML Pages:**  
   Two dark-themed webpages that display the leaderboards interactively using DataTables and PapaParse:
   - `index.html` – Displays the **Player Leaderboard**.
   - `teams.html` – Displays the **Team Leaderboard**.
   
   Both pages include a prominent Google Form link at the top for requesting a team to be added to the leaderboard.

---

## Features

### Python Script

- **Data Fetching:**  
  Uses the NitroType API to obtain seasonal data for each team in a predefined list (`TEAM_TAGS`).

- **Calculations:**  
  - **Accuracy:** Calculated as `(typed - errs) / typed`.
  - **Speed (WPM):** Computed using the formula `(((points / races) / accuracy) - 100) * 2`.

- **CSV Generation:**  
  Produces two CSV files with the current date (formatted as YYYYMMDD):
  - `nitrotype_season_leaderboard_YYYYMMDD.csv`
  - `nitrotype_team_leaderboard_YYYYMMDD.csv`

- **Team Aggregation:**  
  Sums points from all players to compute total team scores.

### HTML Pages

- **Dynamic Data Loading:**  
  The pages use PapaParse to load CSV files dynamically and DataTables to offer search, sort (with default descending order on all sortable columns), and pagination functionality.

- **Dark Theme:**  
  Custom CSS ensures that all components—including table cells (even on selection and sorting)—adhere to a dark style.

- **Google Form Integration:**  
  Each page features a link at the top allowing users to request that a new team be added to the leaderboard.  
  (Link: [Request for a Team to be Added](https://docs.google.com/forms/d/e/1FAIpQLScn1hSm12gN-W-h3rrm6VpNa9lI_4u2yVuXGqTaEihU4yHc9A/viewform?usp=dialog))

---

## File Structure

- `README.md` – This file.
- `nitrotype_leaderboard.py` – Python script for fetching and processing NitroType data.
- `index.html` – Player leaderboard webpage.
- `teams.html` – Team leaderboard webpage.
- CSV files (generated dynamically, e.g., `nitrotype_season_leaderboard_YYYYMMDD.csv` and `nitrotype_team_leaderboard_YYYYMMDD.csv`).

---

## Prerequisites and Setup

### For the Python Script

1. **Dependencies:**  
   Ensure you have Python 3.6 or higher and install the following packages:
   ```bash
   pip install requests pandas
Configuration:

The script uses a predefined list of team tags in the TEAM_TAGS variable. Adjust this list as needed.

Helper functions within the script calculate accuracy and speed from the API data.

Running the Script: Execute the script to generate the CSV files:

bash
python nitrotype_leaderboard.py
CSV files will be created in the repository’s root directory with names that include the current date.

For the HTML Pages
CSV Files: Ensure that the generated CSV files are present in the same directory as index.html and teams.html.

Local Testing: For best results, run a local web server (this avoids issues with file URL restrictions). For example, using Python’s built-in HTTP server:

bash
python -m http.server 8000
Then visit:

http://localhost:8000/index.html for the player leaderboard.

http://localhost:8000/teams.html for the team leaderboard.

Customization:

Adjust the embedded CSS in the <style> sections of the HTML files to change the appearance (such as dark mode colors, fonts, etc.).

Modify the Google Form URL in the .request-link sections if you’re using a different form.

Customization Options
Team Tags and Data Calculations: Modify the TEAM_TAGS variable and helper functions (calculate_accuracy, calculate_speed) in nitrotype_leaderboard.py to suit changes in API structure or your data requirements.

HTML Styling and Features: Both HTML pages feature embedded CSS for dark mode styling. Adjust the styles or DataTables configuration (e.g., modifying the default sort order or appearance) according to your preferences.

Google Form: The Google Form link is placed at the top of each page. You can update this link at any time by modifying the URL in the corresponding HTML files.

Contributing
If you have ideas for improvements or additional features, please feel free to fork the repository and submit a pull request. For major changes, opening an issue first to discuss your ideas is appreciated.

License
This project is licensed under the MIT License.

Happy coding and racing!
