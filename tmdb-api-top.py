import requests
import os
from openpyxl import Workbook
from openpyxl.drawing.image import Image
from io import BytesIO

API_KEY = "9a929d6de568816820a43e8d097efbdd"
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w200"  # Adjust to a smaller cover image size

def fetch_top(media_type, sort_by, genres=None, count=100):
    results = []
    page = 1
    
    while len(results) < count:
        url = f"{BASE_URL}/discover/{media_type}?api_key={API_KEY}"
        params = {
            "sort_by": sort_by,
            "vote_count.gte": 1000 if "vote_average" in sort_by else None,
            "page": page
        }
        if (genres is not None):
            params["with_genres"] = genres
            
        response = requests.get(url, params=params).json()
        if "results" in response:
            results.extend(response["results"])
        print(f"Retrieved {len(results)}%{count} items so far...", end='\r')
        page += 1

    print("Sorting results...")
    size = min(len(results), count)
    sorted_results = sorted(
        results,
        key=lambda x: x["vote_average" if "vote_average" in sort_by else "popularity"],
        reverse=True
    )[:size]
    return sorted_results

def save_to_excel(data, filename, media_type):
    wb = Workbook()
    ws = wb.active
    ws.title = "Top {len(data)}"

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
    print(f"Writing data to {filename}...")
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
            img.width = 160
            img.height = 240
            cell = f'I{idx + 1}'  # Cover image in column I
            ws.add_image(img, cell)

    # Save file
    wb.save(filename)

def main(top_count, genre_id=None):
    # Fetch data
    movies_by_rating = fetch_top("movie", "vote_average.desc", genre_id, top_count)
    tv_by_rating = fetch_top("tv", "vote_average.desc", genre_id, top_count)
    movies_by_popularity = fetch_top("movie", "popularity.desc", genre_id, top_count)
    tv_by_popularity = fetch_top("tv", "popularity.desc", genre_id, top_count)

    # Save to Excel
    print("Saving data to Excel files...")
    folder = "tmdb-top"
    if not os.path.exists(folder):
        os.makedirs(folder)
    path_movies_by_rating = os.path.join(folder, "movies_by_rating.xlsx")
    path_tv_by_rating = os.path.join(folder, "tv_by_rating.xlsx")
    path_movies_by_popularity = os.path.join(folder, "movies_by_popularity.xlsx")
    path_tv_by_popularity = os.path.join(folder, "tv_by_popularity.xlsx")

    save_to_excel(movies_by_rating, path_movies_by_rating, "movie")
    save_to_excel(tv_by_rating, path_tv_by_rating, "tv")
    save_to_excel(movies_by_popularity, path_movies_by_popularity, "movie")
    save_to_excel(tv_by_popularity, path_tv_by_popularity, "tv")

    print("Excel files have been generated!")
    
if __name__ == "__main__":
    # parse top count from command line
    import argparse
    parser = argparse.ArgumentParser(description="Fetch and save top TMDB anime data.")
    parser.add_argument("-c", "--count", type=int, default=100, help="Number of top items to fetch.")
    parser.add_argument("-g", "--genre", type=int, default=None, help="Genre ID to filter.")
    args = parser.parse_args()
    
    main(args.count, args.genre)