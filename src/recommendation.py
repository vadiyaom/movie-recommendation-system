"""
Recommendation Algorithm Module.

Uses TF-IDF Vectorization and Cosine Similarity to find
the most similar movies based on textual metadata features.
Optimized for zero runtime latency by precomputing similarity at startup.
"""

from pathlib import Path
from typing import List, Dict, Any, Optional
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

try:
    from src.data_preprocessing import preprocess_data, get_default_data_path
except ImportError:
    from data_preprocessing import preprocess_data, get_default_data_path


class MovieRecommender:
    """
    Content-Based Movie Recommender utilizing TF-IDF and Cosine Similarity.
    """

    def __init__(self, data_path: Optional[str | Path] = None):
        """
        Initialize and fit the recommendation engine with the movie dataset.
        """
        self.data_path = data_path or get_default_data_path()
        self.df: pd.DataFrame = pd.DataFrame()
        self.tfidf_vectorizer: Optional[TfidfVectorizer] = None
        self.tfidf_matrix = None
        self.similarity_matrix: Optional[np.ndarray] = None
        self._build_model()

    def _build_model(self) -> None:
        """
        Preprocess dataset, compute TF-IDF matrix, and precalculate
        cosine similarity matrix once at application startup.
        """
        # Load and preprocess data
        self.df = preprocess_data(self.data_path)

        # Reset index to ensure 0-to-N continuous index alignment
        self.df = self.df.reset_index(drop=True)

        # Initialize TF-IDF Vectorizer with English stop-words
        self.tfidf_vectorizer = TfidfVectorizer(
            stop_words="english",
            max_features=5000,
            ngram_range=(1, 2)
        )

        # Compute TF-IDF matrix from combined features
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.df["combined_features"])

        # Precompute pairwise cosine similarity matrix
        self.similarity_matrix = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)

    def get_all_titles(self) -> List[str]:
        """Return a sorted list of all movie titles available in the dataset."""
        return sorted(self.df["title"].tolist())

    def find_movie_index(self, query_title: str) -> Optional[int]:
        """
        Find the DataFrame index for a movie title using case-insensitive matching.
        Also attempts fuzzy/partial substring matching if exact match is not found.

        Parameters:
            query_title (str): The search string from user.

        Returns:
            Optional[int]: Index of matched movie, or None if not found.
        """
        if not query_title or not isinstance(query_title, str):
            return None

        clean_query = query_title.strip().lower()
        if not clean_query:
            return None

        # 1. Exact case-insensitive match
        for idx, title in enumerate(self.df["title"]):
            if title.strip().lower() == clean_query:
                return idx

        # 2. Substring / partial match (starts with or contained within)
        for idx, title in enumerate(self.df["title"]):
            lower_title = title.strip().lower()
            if lower_title.startswith(clean_query) or clean_query in lower_title:
                return idx

        return None

    def recommend(self, movie_title: str, n: int = 10) -> Dict[str, Any]:
        """
        Recommend top N similar movies for a given movie title.

        Parameters:
            movie_title (str): Title of the movie to base recommendations on.
            n (int): Number of recommendations to return (default: 10).

        Returns:
            Dict[str, Any]: Dictionary containing:
                - 'searched_movie': Details of the input movie
                - 'recommendations': List of top N similar movie dictionaries
                - 'found': Boolean indicating if the movie was found
                - 'message': Informational or error message
        """
        idx = self.find_movie_index(movie_title)

        if idx is None:
            return {
                "found": False,
                "message": (
                    f"Movie '{movie_title}' not found. "
                    "Please enter a movie from our available movie list."
                ),
                "searched_movie": None,
                "recommendations": []
            }

        searched_row = self.df.iloc[idx]
        searched_movie_info = {
            "movie_id": int(searched_row["movie_id"]) if "movie_id" in searched_row else idx + 1,
            "title": str(searched_row.get("title", "Unknown Title")),
            "genres": str(searched_row.get("genres", "N/A")),
            "rating": float(searched_row.get("rating", 0.0)),
            "release_year": int(searched_row.get("release_year", 0)),
            "overview": str(searched_row.get("overview", "")),
            "poster_url": str(searched_row.get("poster_url", "")),
            "director": str(searched_row.get("director", "N/A")),
            "cast": str(searched_row.get("cast", "N/A")),
            "keywords": str(searched_row.get("keywords", "N/A"))
        }

        # Retrieve similarity scores for this movie
        sim_scores = list(enumerate(self.similarity_matrix[idx]))

        # Sort movies based on similarity score in descending order
        sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Exclude the searched movie itself (which is at index idx with score 1.0)
        filtered_scores = [item for item in sorted_scores if item[0] != idx]

        # Take top n movies
        top_items = filtered_scores[:n]

        recommendations = []
        for rank, (sim_idx, score) in enumerate(top_items, start=1):
            row = self.df.iloc[sim_idx]
            # Convert similarity score (0.0 to 1.0) into a percentage
            score_pct = round(float(score) * 100, 1)

            recommendations.append({
                "rank": rank,
                "movie_id": int(row["movie_id"]) if "movie_id" in row else sim_idx + 1,
                "title": str(row.get("title", "Unknown Title")),
                "genres": str(row.get("genres", "N/A")),
                "rating": float(row.get("rating", 0.0)),
                "release_year": int(row.get("release_year", 0)),
                "overview": str(row.get("overview", "")),
                "poster_url": str(row.get("poster_url", "")),
                "director": str(row.get("director", "N/A")),
                "cast": str(row.get("cast", "N/A")),
                "keywords": str(row.get("keywords", "N/A")),
                "similarity_score": score_pct,
                "similarity_percentage": score_pct
            })

        return {
            "found": True,
            "message": "Success",
            "searched_movie": searched_movie_info,
            "recommendations": recommendations
        }


# Singleton recommender instance initialized at startup
_global_recommender: Optional[MovieRecommender] = None


def get_recommender(data_path: Optional[str | Path] = None) -> MovieRecommender:
    """Return the singleton instance of MovieRecommender."""
    global _global_recommender
    if _global_recommender is None:
        _global_recommender = MovieRecommender(data_path)
    return _global_recommender


def recommend_movies(movie_title: str, n: int = 10) -> Dict[str, Any]:
    """
    Convenience wrapper to get top N movie recommendations.

    Parameters:
        movie_title (str): Title of the movie.
        n (int): Number of similar movies to return (default: 10).

    Returns:
        Dict[str, Any]: Recommendation result dictionary.
    """
    recommender = get_recommender()
    return recommender.recommend(movie_title, n=n)


if __name__ == "__main__":
    print("Testing recommendation engine...")
    engine = get_recommender()
    test_title = "The Dark Knight"
    print(f"\nRecommendations for '{test_title}':")
    results = engine.recommend(test_title, n=5)
    if results["found"]:
        for i, rec in enumerate(results["recommendations"], 1):
            print(f"{i}. {rec['title']} ({rec['release_year']}) - Similarity: {rec['similarity_score']}%")
    else:
        print(results["message"])
