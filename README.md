# NitroType Leaderboard

This repository contains a dynamic, web-based leaderboard for NitroType players and teams. The project provides two separate pages:

- **Players (index.html):** Displays a leaderboard for individual players with details such as Points, Speed, Accuracy, and Races.
- **Teams (teams.html):** Showcases team leaderboards including Total Points, Number of Racers, and Total Races.

A dark theme is applied throughout the site along with interactive DataTables functionality to sort columns (defaulting to descending order for highest values first). Additionally, a Google Form is integrated at the top of each page to allow requests for new teams to be added to the leaderboard.

## Features

- **Data Display:** Dynamically load CSV data for players and teams via [PapaParse](https://www.papaparse.com/).
- **Interactive Tables:** Use [DataTables](https://datatables.net/) for searchable and sortable leaderboards.
- **Dark Theme:** Customized styling for a sleek, dark user interface.
- **Dynamic "Last Updated" Date:** Displays the current date (without time) as soon as the page loads.
- **Google Form Integration:** A prominently displayed link lets users request the addition of new teams.

## File Structure

- `index.html` – The player leaderboard page.
- `teams.html` – The team leaderboard page.
- Other assets (CSS, JavaScript, etc.) are loaded via CDNs.

## Prerequisites

To run this project locally, you'll need:

- A modern web browser.
- A local web server (optional but recommended).  
  *For example, you can use [Live Server for VS Code](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer) or Python’s built-in HTTP server.*

## Usage
