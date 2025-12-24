"""
Add New Movies Script for Movie Recommendation System

This script helps you add new movies to the dataset by:
1. Fetching movie data from TMDB API
2. Processing genres, actors, directors
3. Fetching poster URLs
4. Appending to the existing dataset

Requirements:
- TMDB API key (free at https://www.themoviedb.org/settings/api)
- Set your API key as environment variable: TMDB_API_KEY

Usage:
    python add_movies.py --movie "The Dark Knight"
    python add_movies.py --tmdb-id 155
    python add_movies.py --imdb-id tt0468569
    python add_movies.py --batch movies_to_add.txt
"""

import os
import sys
import json
import argparse
import requests
import pandas as pd
from ast import literal_eval

# TMDB API configuration
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3"
POSTER_BASE_URL = "https://www.themoviedb.org/t/p/original"


def search_movie(title):
    """Search for a movie by title on TMDB."""
    url = f"{TMDB_BASE_URL}/search/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "query": title,
        "include_adult": False
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        results = response.json().get("results", [])
        if results:
            return results[0]  # Return first match
    return None


def get_movie_details(tmdb_id):
    """Get detailed movie information from TMDB."""
    url = f"{TMDB_BASE_URL}/movie/{tmdb_id}"
    params = {
        "api_key": TMDB_API_KEY,
        "append_to_response": "credits"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    return None


def find_by_imdb_id(imdb_id):
    """Find TMDB movie by IMDB ID."""
    url = f"{TMDB_BASE_URL}/find/{imdb_id}"
    params = {
        "api_key": TMDB_API_KEY,
        "external_source": "imdb_id"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        results = response.json().get("movie_results", [])
        if results:
            return results[0]["id"]
    return None


def load_existing_data():
    """Load existing movie data and get the master lists."""
    df = pd.read_csv("movie_data.csv", index_col='id')
    
    # Parse the list columns
    for col in ['Genre list', 'Top actor list', 'Director list', 'Genres bin', 'Actors bin', 'Director bin']:
        df[col] = df[col].apply(lambda x: literal_eval(x) if isinstance(x, str) else x)
    
    # Extract unique values to build master lists
    all_genres = set()
    all_actors = set()
    all_directors = set()
    
    for genres in df['Genre list']:
        if isinstance(genres, list):
            all_genres.update(genres)
    
    for actors in df['Top actor list']:
        if isinstance(actors, list):
            all_actors.update(actors)
    
    for directors in df['Director list']:
        if isinstance(directors, list):
            all_directors.update(directors)
    
    return df, sorted(all_genres), sorted(all_actors), sorted(all_directors)


def create_binary_vector(items, master_list):
    """Create a binary vector indicating presence in master list."""
    vector = [0] * len(master_list)
    for item in items:
        if item in master_list:
            idx = master_list.index(item)
            vector[idx] = 1
    return vector


def process_movie(movie_details, df, genre_list, actor_list, director_list):
    """Process movie details and create a row for the dataframe."""
    # Extract basic info
    tmdb_id = movie_details['id']
    title = movie_details['title']
    popularity = movie_details.get('popularity', 0)
    imdb_id = movie_details.get('imdb_id', '')
    
    # Extract genres
    genres = [g['name'] for g in movie_details.get('genres', [])]
    
    # Extract top 3 actors from credits
    credits = movie_details.get('credits', {})
    cast = credits.get('cast', [])[:3]
    actors = [c['name'] for c in cast]
    
    # Extract directors from credits
    crew = credits.get('crew', [])
    directors = [c['name'] for c in crew if c.get('job') == 'Director']
    
    # Create binary vectors (new entities will be 0s - they're not in master list)
    genres_bin = create_binary_vector(genres, genre_list)
    actors_bin = create_binary_vector(actors, actor_list)
    director_bin = create_binary_vector(directors, director_list)
    
    # Get poster URL
    poster_path = movie_details.get('poster_path', '')
    poster_url = f"{POSTER_BASE_URL}/{poster_path}" if poster_path else ""
    
    return {
        'id': tmdb_id,
        'title': title,
        'popularity': popularity,
        'imdb_id': imdb_id,
        'Genre list': genres,
        'Top actor list': actors,
        'Director list': directors,
        'Genres bin': genres_bin,
        'Actors bin': actors_bin,
        'Director bin': director_bin,
        'posters': poster_url
    }


def add_movie_by_title(title):
    """Add a movie by searching its title."""
    print(f"🔍 Searching for: {title}")
    
    result = search_movie(title)
    if not result:
        print(f"❌ Movie not found: {title}")
        return False
    
    tmdb_id = result['id']
    return add_movie_by_tmdb_id(tmdb_id)


def add_movie_by_tmdb_id(tmdb_id):
    """Add a movie by its TMDB ID."""
    print(f"📥 Fetching movie details for TMDB ID: {tmdb_id}")
    
    details = get_movie_details(tmdb_id)
    if not details:
        print(f"❌ Could not fetch details for TMDB ID: {tmdb_id}")
        return False
    
    # Load existing data
    df, genre_list, actor_list, director_list = load_existing_data()
    
    # Check if movie already exists
    if tmdb_id in df.index:
        print(f"⚠️ Movie already exists: {details['title']}")
        return False
    
    # Process and add movie
    new_movie = process_movie(details, df, genre_list, actor_list, director_list)
    
    # Create new row
    new_row = pd.DataFrame([new_movie])
    new_row.set_index('id', inplace=True)
    
    # Append to existing data
    df = pd.concat([df, new_row])
    
    # Save back to CSV
    df.to_csv("movie_data.csv")
    
    print(f"✅ Added: {new_movie['title']}")
    print(f"   Genres: {new_movie['Genre list']}")
    print(f"   Actors: {new_movie['Top actor list']}")
    print(f"   Directors: {new_movie['Director list']}")
    print(f"   Poster: {new_movie['posters'][:50]}...")
    
    return True


def add_movie_by_imdb_id(imdb_id):
    """Add a movie by its IMDB ID."""
    print(f"🔍 Looking up IMDB ID: {imdb_id}")
    
    tmdb_id = find_by_imdb_id(imdb_id)
    if not tmdb_id:
        print(f"❌ Could not find movie with IMDB ID: {imdb_id}")
        return False
    
    return add_movie_by_tmdb_id(tmdb_id)


def add_movies_from_file(filename):
    """Add multiple movies from a file (one title per line)."""
    with open(filename, 'r') as f:
        titles = [line.strip() for line in f if line.strip()]
    
    print(f"📋 Adding {len(titles)} movies from {filename}\n")
    
    success = 0
    failed = 0
    
    for title in titles:
        if add_movie_by_title(title):
            success += 1
        else:
            failed += 1
        print()
    
    print(f"\n📊 Summary: {success} added, {failed} failed")


def rebuild_binary_vectors():
    """Rebuild all binary vectors (use after adding many new movies with new actors/genres)."""
    print("🔄 Rebuilding binary vectors...")
    
    df = pd.read_csv("movie_data.csv", index_col='id')
    
    # Parse list columns
    for col in ['Genre list', 'Top actor list', 'Director list']:
        df[col] = df[col].apply(lambda x: literal_eval(x) if isinstance(x, str) else x)
    
    # Build complete master lists
    all_genres = set()
    all_actors = set()
    all_directors = set()
    
    for genres in df['Genre list']:
        if isinstance(genres, list):
            all_genres.update(genres)
    
    for actors in df['Top actor list']:
        if isinstance(actors, list):
            all_actors.update(actors)
    
    for directors in df['Director list']:
        if isinstance(directors, list):
            all_directors.update(directors)
    
    genre_list = sorted(all_genres)
    actor_list = sorted(all_actors)
    director_list = sorted(all_directors)
    
    print(f"   Genres: {len(genre_list)}")
    print(f"   Actors: {len(actor_list)}")
    print(f"   Directors: {len(director_list)}")
    
    # Rebuild binary vectors for all movies
    df['Genres bin'] = df['Genre list'].apply(lambda x: create_binary_vector(x, genre_list))
    df['Actors bin'] = df['Top actor list'].apply(lambda x: create_binary_vector(x, actor_list))
    df['Director bin'] = df['Director list'].apply(lambda x: create_binary_vector(x, director_list))
    
    # Save
    df.to_csv("movie_data.csv")
    print("✅ Binary vectors rebuilt!")


def main():
    parser = argparse.ArgumentParser(description="Add movies to the recommendation system")
    parser.add_argument("--movie", "-m", help="Movie title to search and add")
    parser.add_argument("--tmdb-id", "-t", type=int, help="TMDB movie ID")
    parser.add_argument("--imdb-id", "-i", help="IMDB movie ID (e.g., tt0468569)")
    parser.add_argument("--batch", "-b", help="File with movie titles (one per line)")
    parser.add_argument("--rebuild", "-r", action="store_true", 
                        help="Rebuild binary vectors after adding movies")
    
    args = parser.parse_args()
    
    if not TMDB_API_KEY:
        print("❌ Error: TMDB_API_KEY environment variable not set!")
        print("   Get your free API key at: https://www.themoviedb.org/settings/api")
        print("   Then run: export TMDB_API_KEY='your_api_key'")
        sys.exit(1)
    
    if args.movie:
        add_movie_by_title(args.movie)
    elif args.tmdb_id:
        add_movie_by_tmdb_id(args.tmdb_id)
    elif args.imdb_id:
        add_movie_by_imdb_id(args.imdb_id)
    elif args.batch:
        add_movies_from_file(args.batch)
    elif args.rebuild:
        rebuild_binary_vectors()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
