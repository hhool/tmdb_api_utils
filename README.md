# TMDB API Project

This project uses the TMDB (The Movie Database) API to fetch and process data related to anime movies and TV shows. The project includes scripts to fetch data, categorize it, and save it to Excel files.

## Files

- `tmdb-api-a-z.py`: Fetches all anime data, categorizes it by the first letter of the title, and saves the data to Excel files.
- `tmdb-api-top.py`: Fetches the top 100 anime movies and TV shows based on rating and popularity, and saves the data to Excel files.
- `tmdb-api-total.py`: Fetches the total number of anime movies and TV shows available on TMDB.

## Requirements

- Python 3.x
- `requests` library
- `openpyxl` library

You can install the required libraries using pip:

```sh
pip install requests openpyxl
