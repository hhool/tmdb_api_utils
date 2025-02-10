import requests
import os
from openpyxl import Workbook
from openpyxl.drawing.image import Image
from io import BytesIO

API_KEY = "9a929d6de568816820a43e8d097efbdd"
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w200"  # Adjust to a smaller cover image size

def fetch_top_100(media_type, sort_by):
    results = []
    page = 1
    
    while len(results) < 100 and page <= 5:
        url = f"{BASE_URL}/discover/{media_type}?api_key={API_KEY}"
        params = {
            "with_genres": 16,
            "sort_by": sort_by,
            "vote_count.gte": 1000 if "vote_average" in sort_by else None,
            "page": page
        }
        response = requests.get(url, params=params).json()
        if "results" in response:
            results.extend(response["results"])
        page += 1

    sorted_results = sorted(
        results,
        key=lambda x: x["vote_average" if "vote_average" in sort_by else "popularity"],
        reverse=True
    )[:100]
    return sorted_results

def save_to_excel(data, filename, media_type):
    wb = Workbook()
    ws = wb.active
    ws.title = "Top 100"

    # New headers (including TMDB ID)
    headers = ["Rank", "TMDB ID", "Title", "Type", "Rating", "Vote Count", "Popularity", "Release Date", "Cover"]
    ws.append(headers)

    # Set column widths (including new ID column)
    column_widths = {
        'A': 8,    # Rank
        'B': 12,   # TMDB ID
        'C': 35,   # Title
        'D': 10,   # Type
        'E': 8,    # Rating
        'F': 10,   # Vote Count
        'G': 12,   # Popularity
        'H': 15,   # Release Date
        'I': 25    # Cover
    }
    for col, width in column_widths.items():
        ws.column_dimensions[col].width = width

    # Fill data
    for idx, item in enumerate(data, 1):
        # Get key data
        tmdb_id = item.get("id", "N/A")
        title = item.get("title") if media_type == "movie" else item.get("name")
        media_type_label = "Movie" if media_type == "movie" else "TV"
        release_date = item.get("release_date") if media_type == "movie" else item.get("first_air_date")

        # Download cover image
        poster_path = item.get("poster_path")
        img_url = f"{IMAGE_BASE_URL}{poster_path}" if poster_path else None
        img_data = None
        if img_url:
            try:
                response = requests.get(img_url)
                img_data = BytesIO(response.content)
            except:
                img_data = None

        # Write row data
        row = [
            idx,
            tmdb_id,
            title,
            media_type_label,
            item.get("vote_average"),
            item.get("vote_count"),
            item.get("popularity"),
            release_date,
            "Cover Image" if img_data else "No Cover"
        ]
        ws.append(row)

        # Insert image (adjust to column I)
        if img_data:
            img = Image(img_data)
            img.width = 80
            img.height = 120
            cell = f'I{idx + 1}'  # Cover image in column I
            ws.add_image(img, cell)

    # Save file
    wb.save(filename)

# Fetch data
movies_by_rating = fetch_top_100("movie", "vote_average.desc")
tv_by_rating = fetch_top_100("tv", "vote_average.desc")
movies_by_popularity = fetch_top_100("movie", "popularity.desc")
tv_by_popularity = fetch_top_100("tv", "popularity.desc")

# Save to Excel
save_to_excel(movies_by_rating, "movies_by_rating.xlsx", "movie")
save_to_excel(tv_by_rating, "tv_by_rating.xlsx", "tv")
save_to_excel(movies_by_popularity, "movies_by_popularity.xlsx", "movie")
save_to_excel(tv_by_popularity, "tv_by_popularity.xlsx", "tv")

print("Excel files have been generated!")