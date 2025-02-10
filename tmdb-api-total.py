import requests

API_KEY = "9a929d6de568816820a43e8d097efbdd"
BASE_URL = "https://api.themoviedb.org/3"

def get_total_count(media_type):
    url = f"{BASE_URL}/discover/{media_type}"
    params = {
        "api_key": API_KEY,
        "with_genres": 16,  # Anime genre
        "sort_by": "popularity.desc",
        "page": 1
    }
    response = requests.get(url, params=params).json()
    total_results = response.get("total_results", 0)
    return total_results

def main():
    movie_count = get_total_count("movie")
    tv_count = get_total_count("tv")
    total_count = movie_count + tv_count

    print(f"Total number of anime movies: {movie_count}")
    print(f"Total number of anime TV shows: {tv_count}")
    print(f"Total number of anime (movies + TV shows): {total_count}")

if __name__ == "__main__":
    main()