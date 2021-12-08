# Movie-Recommendation-Project
_____
This is the repo for a movie recommendation system made using the [IMDb](https://www.imdb.com/) dataset.

The deployed app can be found [here](https://share.streamlit.io/omega-84/movie-recommendation-project/main/app.py).

The dataset was cleaned and trivial/non-essential features were discarded.

Final dataset consited of the following features-
1. ID
2. Title
3. IMDb ID
4. List of genres
5. List of top 3 actors 
6. List of director(s)
7. Popularity

The logic behind the program revolves aroung [KNN](https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm) that a particular object is influenced by other objects in its proximity. However, we used [cosine distance](https://en.wikipedia.org/wiki/Cosine_similarity) to compute our recommended movies and not the [Nearest Neighbour](https://scikit-learn.org/stable/modules/neighbors.html) class available in Scikit-learn.


