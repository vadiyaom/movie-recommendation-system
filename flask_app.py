"""
Movie Recommendation System - Flask Web Application (Alternative Server).

A production-ready Flask application implementing content-based
movie recommendations using Scikit-Learn TF-IDF & Cosine Similarity,
backed by an SQLite search history logger.
"""

import os
from pathlib import Path
from flask import Flask, render_template, request, jsonify, redirect, url_for
from src.recommendation import get_recommender, recommend_movies
from database import init_db, add_search, get_search_history

# Setup absolute paths for templates and static folders
BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

app = Flask(
    __name__,
    template_folder=str(TEMPLATES_DIR),
    static_folder=str(STATIC_DIR)
)

# Initialize SQLite database schema
init_db()

# Pre-load dataset and precompute TF-IDF & similarity matrix at startup
recommender = get_recommender()


@app.route("/", methods=["GET"])
def home():
    """Renders the homepage with the search form and suggestions."""
    all_movies = recommender.get_all_titles()
    recent_history = get_search_history(limit=5)
    return render_template(
        "index.html",
        all_movies=all_movies,
        recent_history=recent_history,
        error_message=None
    )


@app.route("/recommend", methods=["GET", "POST"])
def recommend():
    """Handles recommendation requests via GET or POST."""
    if request.method == "POST":
        movie_query = request.form.get("movie_title", "").strip()
    else:
        movie_query = request.args.get("title", "").strip()

    all_movies = recommender.get_all_titles()

    if not movie_query:
        return render_template(
            "index.html",
            all_movies=all_movies,
            recent_history=get_search_history(limit=5),
            error_message="Please enter a movie name to get recommendations."
        ), 400

    result = recommend_movies(movie_query, n=10)

    if not result["found"]:
        return render_template(
            "recommendations.html",
            query_title=movie_query,
            found=False,
            error_message=(
                f"Movie '{movie_query}' was not found in our database. "
                "Please select or enter a movie from our available list."
            ),
            all_movies=all_movies,
            searched_movie=None,
            recommendations=[]
        ), 404

    searched_title = result["searched_movie"]["title"]
    add_search(searched_title)

    return render_template(
        "recommendations.html",
        query_title=searched_title,
        found=True,
        error_message=None,
        all_movies=all_movies,
        searched_movie=result["searched_movie"],
        recommendations=result["recommendations"]
    )


@app.route("/history", methods=["GET"])
def history():
    """Displays previous searches stored in SQLite database."""
    search_logs = get_search_history(limit=50)
    all_movies = recommender.get_all_titles()
    return render_template(
        "index.html",
        all_movies=all_movies,
        recent_history=search_logs,
        view_history=True,
        error_message=None
    )


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "ok",
        "movies_loaded": len(recommender.get_all_titles()),
        "service": "Movie Recommendation System"
    }), 200


@app.route("/api/movies", methods=["GET"])
def api_movies():
    """API route returning all available movie titles."""
    return jsonify(recommender.get_all_titles()), 200


@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for("home"))


@app.errorhandler(500)
def server_error(e):
    return render_template(
        "index.html",
        all_movies=recommender.get_all_titles(),
        recent_history=get_search_history(limit=5),
        error_message="An unexpected server error occurred. Please try again."
    ), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
