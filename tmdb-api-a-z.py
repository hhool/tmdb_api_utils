import requests
import time
from datetime import datetime
from openpyxl import Workbook
from openpyxl.drawing.image import Image
from io import BytesIO

API_KEY = "9a929d6de568816820a43e8d097efbdd"
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w200"  # Poster image size
DELAY_SECONDS = 1  # Normal request interval
RETRY_DELAY = 3    # Retry interval after failure

# Enhanced request function with infinite retry
def make_request(url, params):
    first_failure_time = None
    last_alert_time = None
    
    while True:
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except (requests.exceptions.RequestException, ValueError) as e:
            now = datetime.now()
            error_msg = str(e).replace('\n', ' ')[:100]  # Truncate error message
            
            if first_failure_time is None:
                first_failure_time = now
                print(f"[Initial Failure] Time: {now.strftime('%H:%M:%S')} | Error: {error_msg}... | Retrying (Ctrl+C to abort)", end='\r')
            
            if last_alert_time is None or (now - last_alert_time).seconds >= RETRY_DELAY:
                print(f"[Retrying] First failure: {first_failure_time.strftime('%H:%M:%S')} | Latest error: {error_msg}...      ", end='\r')
                last_alert_time = now
            
            time.sleep(RETRY_DELAY)
        except KeyboardInterrupt:
            print("\n[User Interruption] Program terminated by user")
            exit(1)

def fetch_all_anime():
    all_data = []
    
    for media_type in ["movie", "tv"]:
        page = 1
        total_pages = 1
        
        while page <= total_pages:
            url = f"{BASE_URL}/discover/{media_type}"
            params = {
                "api_key": API_KEY,
                "with_genres": 16,
                "sort_by": "popularity.desc",
                "page": page
            }
            
            response = make_request(url, params)
            
            if "results" in response:
                for item in response["results"]:
                    item["media_type"] = media_type
                all_data.extend(response["results"])
                total_pages = response.get("total_pages", 1)
                page += 1
                time.sleep(DELAY_SECONDS)

    return all_data

def save_category_to_excel(category_data, category_name):
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
        media_type = item["media_type"]
        tmdb_id = item.get("id", "N/A")
        title = item.get("title") if media_type == "movie" else item.get("name")
        release_date = item.get("release_date") if media_type == "movie" else item.get("first_air_date")
        
        # Handle poster image
        poster_path = item.get("poster_path")
        img_url = f"{IMAGE_BASE_URL}{poster_path}" if poster_path else None
        img_data = None
        if img_url:
            try:
                response = requests.get(img_url)
                img_data = BytesIO(response.content)
            except:
                img_data = None
        
        # Add row data
        row = [
            idx,
            tmdb_id,
            title,
            "Movie" if media_type == "movie" else "TV",
            item.get("vote_average", "N/A"),
            item.get("vote_count", "N/A"),
            item.get("popularity", "N/A"),
            release_date,
            "Poster" if img_data else "No Poster"
        ]
        ws.append(row)
        
        # Insert image
        if img_data:
            img = Image(img_data)
            img.width = 80
            img.height = 120
            ws.add_image(img, f'I{idx + 1}')
    
    # Save file
    filename = f"{category_name}.xlsx" if category_name != "other" else "other.xlsx"
    wb.save(filename)
    print(f"File {filename} generated successfully!")

def main():
    try:
        print("[Start] Data collection initiated (Ctrl+C to abort)")
        all_anime = fetch_all_anime()
        print(f"\nSuccessfully collected {len(all_anime)} entries")
        
        # Categorization
        categories = {chr(c): [] for c in range(65, 91)}  # A-Z
        categories["other"] = []
        
        for item in all_anime:
            title = item.get("title") if item["media_type"] == "movie" else item.get("name")
            if not title:
                categories["other"].append(item)
                continue
            
            first_char = title.strip()[0].upper() if title.strip() else ''
            if first_char.isalpha() and 'A' <= first_char <= 'Z':
                categories[first_char].append(item)
            else:
                categories["other"].append(item)
        
        # Save categories
        for char, data in categories.items():
            save_category_to_excel(data, char)
        
        print("All files generated successfully!")
    except KeyboardInterrupt:
        print("\n[Interruption] Data saving aborted by user")
        # Save the collected data so far
        for char, data in categories.items():
            save_category_to_excel(data, char)
    except Exception as e:
        print(f"\n[Critical Error] {str(e).replace('\n', ' ')}")
    finally:
        print("Program exited")

if __name__ == "__main__":
    main()