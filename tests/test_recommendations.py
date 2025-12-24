"""
Unit tests for the Movie Recommendation System.
These tests verify core functionality without requiring the full dataset.
"""
import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestConfig:
    """Test configuration module."""
    
    def test_config_imports(self):
        """Test that config module can be imported."""
        import config
        assert hasattr(config, 'NUM_RECOMMENDATIONS')
        assert hasattr(config, 'MOVIE_DATA_PATH')
        assert hasattr(config, 'ENABLE_CACHE')
    
    def test_config_defaults(self):
        """Test that config has sensible defaults."""
        import config
        assert config.NUM_RECOMMENDATIONS >= 1
        assert config.MAX_CACHE_SIZE >= 1
        assert isinstance(config.ENABLE_CACHE, bool)


class TestMyFunctions:
    """Test recommendation functions."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup for tests - skip if data file not found."""
        import config
        if not os.path.exists(config.MOVIE_DATA_PATH):
            pytest.skip("Movie data file not found")
    
    def test_get_all_movies_returns_list(self):
        """Test that get_all_movies returns a list."""
        import my_functions as myfn
        movies = myfn.get_all_movies()
        assert isinstance(movies, list)
        assert len(movies) > 0
    
    def test_get_all_movies_tuple_format(self):
        """Test that movies are returned as (id, title) tuples."""
        import my_functions as myfn
        movies = myfn.get_all_movies()
        if movies:
            first_movie = movies[0]
            assert isinstance(first_movie, tuple)
            assert len(first_movie) == 2
    
    def test_get_movie_title(self):
        """Test getting movie title."""
        import my_functions as myfn
        movies = myfn.get_all_movies()
        if movies:
            movie_id = movies[0][0]
            title = myfn.get_movie_title(movie_id)
            assert isinstance(title, str)
            assert len(title) > 0
    
    def test_get_movie_title_invalid_id(self):
        """Test that invalid movie ID returns default title."""
        import my_functions as myfn
        title = myfn.get_movie_title(-99999)
        assert title == 'Unknown Title'
    
    def test_get_movie_poster(self):
        """Test getting movie poster URL."""
        import my_functions as myfn
        import config
        movies = myfn.get_all_movies()
        if movies:
            movie_id = movies[0][0]
            poster = myfn.get_movie_poster(movie_id)
            assert isinstance(poster, str)
            # Should return either a valid URL or the default
            assert poster.startswith('http') or poster == config.DEFAULT_POSTER_URL
    
    def test_get_recommendations_returns_list(self):
        """Test that recommendations returns a list."""
        import my_functions as myfn
        movies = myfn.get_all_movies()
        if movies:
            movie_id = movies[0][0]
            recs = myfn.get_recommendations(movie_id, K=3)
            assert isinstance(recs, list)
    
    def test_get_recommendations_correct_count(self):
        """Test that we get the requested number of recommendations."""
        import my_functions as myfn
        movies = myfn.get_all_movies()
        if movies:
            movie_id = movies[0][0]
            k = 3
            recs = myfn.get_recommendations(movie_id, K=k)
            assert len(recs) == k
    
    def test_recommendations_format(self):
        """Test recommendation tuple format."""
        import my_functions as myfn
        movies = myfn.get_all_movies()
        if movies:
            movie_id = movies[0][0]
            recs = myfn.get_recommendations(movie_id, K=1)
            if recs:
                rec = recs[0]
                assert isinstance(rec, tuple)
                assert len(rec) == 2
                assert isinstance(rec[0], str)  # Description text


class TestCaching:
    """Test caching functionality."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup for tests."""
        import config
        if not os.path.exists(config.MOVIE_DATA_PATH):
            pytest.skip("Movie data file not found")
    
    def test_cache_consistency(self):
        """Test that cached results are consistent."""
        import my_functions as myfn
        movies = myfn.get_all_movies()
        if movies:
            movie_id = movies[0][0]
            
            # Get recommendations twice
            recs1 = myfn.get_recommendations(movie_id, K=3)
            recs2 = myfn.get_recommendations(movie_id, K=3)
            
            # Should return same results
            assert recs1 == recs2


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
