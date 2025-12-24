# Configuration settings for the Movie Recommendation System
import os

# Number of recommendations to show
NUM_RECOMMENDATIONS = int(os.getenv("NUM_RECOMMENDATIONS", "5"))

# Data file paths
MOVIE_DATA_PATH = os.getenv("MOVIE_DATA_PATH", "movie_data.csv")
IMDB_DATA_PATH = os.getenv("IMDB_DATA_PATH", "imdb_data.csv")

# Default poster image
DEFAULT_POSTER_URL = os.getenv(
    "DEFAULT_POSTER_URL",
    "https://via.placeholder.com/250x375?text=No+Poster"
)

# UI Settings
APP_TITLE = "CineSphere"
APP_ICON = "🎬"
THEME_COLOR = "#E50914"  # Netflix Red

# Cache settings
ENABLE_CACHE = os.getenv("ENABLE_CACHE", "true").lower() == "true"
MAX_CACHE_SIZE = int(os.getenv("MAX_CACHE_SIZE", "1000"))
