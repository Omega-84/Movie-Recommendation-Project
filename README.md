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

The logic behind the program revolves aroung [KNN](https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm) that a particular object is influenced by other objects in its proximity. However, we used [cosine distances](https://en.wikipedia.org/wiki/Cosine_similarity) to compute our recommended movies and not the [Nearest Neighbour](https://scikit-learn.org/stable/modules/neighbors.html) class available in Scikit-learn.
A mega-list was created for genres, actors and directors which consisted of all unique entities in them. Using them we created a binary-sparse list for all 3 features which represented if the entity was present in a particular movie or not.
To compute the closeness, we import Scipy's [spatial.distance.cosine](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.cosine.html) method to calculate the distances.

The spatial.distance.cosine object calculates the distance between 2 1-d array u and v as

\begin{equation}
\begin{center}

1 - u.v/(mod(u)^2 mod(v)^2)

\end{center}
\end{equation}


