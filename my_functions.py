import numpy as np
import pandas as pd
import operator
from scipy import spatial
from ast import literal_eval as eval
from functools import lru_cache
import config

# Load data once at module level
df = pd.read_csv(config.MOVIE_DATA_PATH, index_col='id')

# Normalize popularity to [0, 1] range to prevent it from dominating the distance metric
# (Cosine distance is 0-1, but absolute popularity diff was huge for new movies)
if 'popularity' in df.columns:
    df['popularity'] = (df['popularity'] - df['popularity'].min()) / (df['popularity'].max() - df['popularity'].min())

for i in ['Genre list', 'Top actor list', 'Director list', 'Genres bin', 'Actors bin', 'Director bin']:
    df[i] = df[i].apply(lambda x: eval(x))


def create_movie_dict(dataframe, index):
    """Create a tuple containing specific information about the movie.
    
    Args:
        dataframe: The pandas dataframe containing movie records
        index: The index of movie record
        
    Returns:
        Tuple with (title, genres_bin, actors_bin, director_bin, popularity)
    """
    try:
        tup = (
            dataframe['title'][index],
            tuple(dataframe['Genres bin'][index]),  # Convert to tuple for hashing
            tuple(dataframe['Actors bin'][index]),
            tuple(dataframe['Director bin'][index]),
            dataframe['popularity'][index]
        )
        return tup
    except KeyError:
        return None


def compute_dist(df1, ind1, df2, ind2):
    """Computes the distance between 2 movies based on cosine distance.
    
    Args:
        df1, df2: DataFrames containing movie data
        ind1, ind2: Indices of the movies to compare
        
    Returns:
        Combined distance score (lower = more similar)
    """
    mov1 = create_movie_dict(df1, ind1)
    mov2 = create_movie_dict(df2, ind2)
    
    if mov1 is None or mov2 is None:
        return float('inf')  # Return high distance for invalid movies
    
    genre_distance = spatial.distance.cosine(mov1[1], mov2[1])
    actor_distance = spatial.distance.cosine(mov1[2], mov2[2])
    dir_distance = spatial.distance.cosine(mov1[3], mov2[3])
    popularity_distance = abs(mov1[4] - mov2[4])
    
    return genre_distance + popularity_distance + actor_distance + dir_distance


# Cache recommendations to avoid recomputation
@lru_cache(maxsize=config.MAX_CACHE_SIZE)
def get_recommendations_cached(movie_id, k=5):
    """Cached version of get_recommendations for better performance."""
    return _compute_recommendations(movie_id, k)


def _compute_recommendations(movie_id, k):
    """Internal function to compute recommendations."""
    distances = []
    training = df.drop(movie_id, axis=0)
    train_movie_dict = dict(zip(training.index, training['title']))
    
    for key, value in train_movie_dict.items():
        dist = compute_dist(training, key, df, movie_id)
        distances.append((value, dist, key))
    
    distances.sort(key=operator.itemgetter(1))
    
    recommendation_list = []
    for i in range(min(k, len(distances))):  # Handle edge case
        name = distances[i][0]
        idd = distances[i][2]
        
        # Safely get movie details with defaults
        genre_list = df['Genre list'].get(idd, [])
        actor_list = df['Top actor list'].get(idd, [])
        director_list = df['Director list'].get(idd, [])
        
        recommendation_list.append((
            str(
                name + ' \n\t ' + 
                " Genre: " + str(genre_list).strip('[]').replace(' ', '') +
                ' \n\t ' + " Actors: " + str(actor_list).strip('[]') + 
                ' \n\t ' + " Director(s): " + str(director_list).strip('[]')
            ),
            idd
        ))
    
    return recommendation_list


def get_recommendations(ID, K=None):
    """Get movie recommendations based on similarity.
    
    Args:
        ID: The movie index to get recommendations for
        K: Number of recommendations (default from config)
        
    Returns:
        List of tuples: (recommendation_text, movie_id)
    """
    if K is None:
        K = config.NUM_RECOMMENDATIONS
        
    if config.ENABLE_CACHE:
        return list(get_recommendations_cached(ID, K))
    else:
        return _compute_recommendations(ID, K)


def get_movie_poster(movie_id):
    """Get movie poster URL with fallback for missing posters.
    
    Args:
        movie_id: The movie index
        
    Returns:
        Poster URL or default placeholder
    """
    try:
        poster = df['posters'].get(movie_id)
        if poster and str(poster).strip() and str(poster) != 'nan':
            return poster
    except Exception:
        pass
    return config.DEFAULT_POSTER_URL


def get_movie_title(movie_id):
    """Safely get movie title.
    
    Args:
        movie_id: The movie index
        
    Returns:
        Movie title or 'Unknown Title'
    """
    try:
        return df['title'].get(movie_id, 'Unknown Title')
    except Exception:
        return 'Unknown Title'


def get_all_movies():
    """Get list of all movies for the dropdown.
    
    Returns:
        List of tuples: (movie_id, title)
    """
    movie_list = []
    # Reverse order to show newest additions first
    for i in df.index[::-1]:
        try:
            movie_list.append((i, df['title'][i]))
        except KeyError:
            continue
    return movie_list


def get_new_arrivals(limit=10):
    """Get the most recently added movies.
    
    Args:
        limit: Number of movies to return
        
    Returns:
        List of tuples: (movie_id, title, poster_url)
    """
    new_movies = []
    # Get last 'limit' movies from the dataframe
    recent_indices = df.index[-limit:][::-1]
    
    for idx in recent_indices:
        try:
            title = df['title'][idx]
            poster = get_movie_poster(idx)
            new_movies.append((idx, title, poster))
        except Exception:
            continue
            
    return new_movies
