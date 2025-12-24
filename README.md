# Movie-Recommendation-Project
_____
This is the repo for a movie recommendation system made using the [IMDb](https://www.imdb.com/) dataset.

The deployed app can be found [here](https://omega-84-movie-recommendation-project-app-j8dinr.streamlit.app/).

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

![formula](https://latex.codecogs.com/gif.latex?1%20-%20%5Cfrac%7Bu%5Ccdot%20v%7D%7B%5Cleft%20%5C%7C%20u%20%5Cright%20%5C%7C%5E2%20%5Cleft%20%5C%7C%20v%20%5Cright%20%5C%7C%5E2%7D)

where u and v are the binary lists for the movies.

Finally web scraping was performed to obtain the poster links of the movies using the imdb-id. For this we used [The Movie Database's](https://www.themoviedb.org/) public API.
To know more visit this [link](https://bin.re/blog/tutorial-download-posters-with-the-movie-database-api-in-python/).

Note: You will need to obtain an API key that is accessible for free after you create an account.

---

## 🐳 Docker

### Quick Start with Docker

```bash
# Build the image
docker build -t movie-recommendation .

# Run the container
docker run -p 8501:8501 movie-recommendation
```

Then open your browser to `http://localhost:8501`

### Using Docker Compose (Recommended for Development)

```bash
# Start the application
docker-compose up

# Start in background
docker-compose up -d

# Stop the application
docker-compose down
```

### Pull from GitHub Container Registry

```bash
docker pull ghcr.io/omega-84/movie-recommendation-project:latest
docker run -p 8501:8501 ghcr.io/omega-84/movie-recommendation-project:latest
```

---

## 🔄 CI/CD Pipeline

This project uses GitHub Actions for continuous integration and deployment.

![CI/CD Pipeline](https://github.com/Omega-84/Movie-Recommendation-Project/actions/workflows/ci-cd.yml/badge.svg)

### Pipeline Stages

1. **🔍 Lint & Test** - Runs flake8 linting and pytest (if tests exist)
2. **🐳 Build Docker** - Builds and tests the Docker image
3. **📤 Push to GHCR** - Pushes to GitHub Container Registry (main branch only)

### Triggering the Pipeline

- **Automatic**: On push to `main` or `develop` branches
- **Pull Requests**: On PRs targeting `main`
- **Manual**: Via GitHub Actions "Run workflow" button

