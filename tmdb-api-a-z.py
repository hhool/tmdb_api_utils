import sys
import os
import requests
import time
from datetime import datetime
from openpyxl import Workbook
import argparse

def fetch_all_anime(entry_param, media_type):
    all_data = []
    first_failure_time = None
    last_alert_time = None
    RETRY_DELAY = 5  # seconds
    MAX_RETRIES = 3  # maximum number of retries

    page = 1
    total_pages = 1
    retry_count = 0
    while page <= total_pages:
        url = f"https://api.themoviedb.org/3/search/{media_type}"
        params = {
            "api_key": "9a929d6de568816820a43e8d097efbdd",
            "with_genres": "16",  # Genre ID for Animation
            "page": page,
            "sort_by": "popularity.desc", # Sort by popularity in descending order
            "query": entry_param  # Filter titles starting with 'A'
        }
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            total_pages = data["total_pages"]
            all_data.extend(data["results"])
            page += 1
            print(f"Retrieved {len(all_data)} items so far...", end='\r')
            retry_count = 0  # reset retry count on success
        except (requests.exceptions.RequestException, ValueError) as e:
            now = datetime.now()
            error_msg = str(e).replace('\n', ' ')[:100]  # Truncate error message
            
            if first_failure_time is None:
                first_failure_time = now
                print(f"[Initial Failure] Time: {now.strftime('%H:%M:%S')} | Error: {error_msg}... | Retrying (Ctrl+C to abort)", end='\r')
            
            if last_alert_time is None or (now - last_alert_time).seconds >= RETRY_DELAY:
                print(f"[Retrying] First failure: {first_failure_time.strftime('%H:%M:%S')} | Latest error: {error_msg}...      ", end='\r')
                last_alert_time = now
            
            retry_count += 1
            if retry_count >= MAX_RETRIES or isinstance(e, requests.exceptions.ConnectTimeout):
                print("\n[Max Retries Reached or Connection Timeout] Saving data and exiting...")
                filtered_data = filter_data(all_data, entry_param, media_type)
                # check media type and make filename
                if entry_param.isalnum():
                    filename = f"{media_type}_{entry_param.lower()}"
                else:
                    filename = f"{media_type}_other"
                save_category_to_excel(filtered_data, filename, media_type)
                print(f"Data saved to tmdb-az/{filename}.xlsx")
                exit(1)
            
            time.sleep(RETRY_DELAY)
        except KeyboardInterrupt:
            print("\n[User Interruption] Program terminated by user")
            filtered_data = filter_data(all_data, entry_param, media_type)
            # check media type and make filename
            if entry_param.isalnum():
                filename = f"{media_type}_{entry_param.lower()}"
            else:
                filename = f"{media_type}_other"
            save_category_to_excel(filtered_data, filename, media_type)
            print(f"Data saved to tmdb-az/{filename}.xlsx")
            exit(1)
    
    return filter_data(all_data, entry_param, media_type)

def filter_data(all_data, entry_param, media_type):
    filtered_data = []
    for item in all_data:
        title = item.get("title") if media_type == "movie" else item.get("name")
        if not title:
            continue
        
        first_char = title.strip()[0].upper() if title.strip() else ''
        if entry_param.isalnum() and entry_param.upper() == first_char:
            filtered_data.append(item)
        elif entry_param == '!' and not first_char.isalnum():
            filtered_data.append(item)
    
    return filtered_data

def save_category_to_excel(category_data, category_name, media_type):
    if not category_data:
        return
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Data"
    
    # Headers
    headers = ["Rank", "TMDB ID", "Title", "Type", "Rating", "Votes", "Popularity", "Release Date", "Poster"]
    ws.append(headers)
    
    # Column widths
    column_widths = {'A': 8, 'B': 12, 'C': 35, 'D': 10, 
                    'E': 8, 'F': 10, 'G': 12, 'H': 15, 'I': 25}
    for col, width in column_widths.items():
        ws.column_dimensions[col].width = width
    
    # Populate data
    for idx, item in enumerate(category_data, 1):
        tmdb_id = item.get("id", "N/A")
        title = item.get("title") if media_type == "movie" else item.get("name")
        release_date = item.get("release_date") if media_type == "movie" else item.get("first_air_date")
        
        # Handle poster image
        poster_path = item.get("poster_path", "")
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else "N/A"
        
        row = [idx, tmdb_id, title, media_type, item.get("vote_average", "N/A"), 
               item.get("vote_count", "N/A"), item.get("popularity", "N/A"), 
               release_date, poster_url]
        ws.append(row)
    
    # Ensure the directory exists
    os.makedirs("tmdb-az", exist_ok=True)
    wb.save(f"tmdb-az/{category_name}.xlsx")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch and save TMDB anime data based on entry parameter.")
    parser.add_argument("-t", "--title", required=True, help="Entry parameter to filter anime titles (A-Z, 0-9, or ! for others).")
    args = parser.parse_args()
    
    entry_param = args.title
    all_anime_tv = fetch_all_anime(entry_param, "tv")
    all_anime_movie = fetch_all_anime(entry_param, "movie")
    
    if entry_param.isalnum():
        filename_tv = f"tv_{entry_param.lower()}"
        filename_movie = f"movie_{entry_param.lower()}"
    else:
        filename_tv = "tv_other"
        filename_movie = "movie_other"
    
    save_category_to_excel(all_anime_tv, filename_tv, "tv")
    save_category_to_excel(all_anime_movie, filename_movie, "movie")
    print(f"Successfully collected {len(all_anime_tv)} TV entries and saved to tmdb-az/{filename_tv}.xlsx")
    print(f"Successfully collected {len(all_anime_movie)} movie entries and saved to tmdb-az/{filename_movie}.xlsx")