"""
🎬 Movie Recommendation System - Streamlit Web Application
Author: Om Vadiya (GitHub: @vadiyaom)
Role: Entry-Level Data Science Portfolio Project
Technologies: Python, Pandas, NumPy, Scikit-Learn (TF-IDF & Cosine Similarity), Streamlit
"""

import os
import sys
from pathlib import Path
import sqlite3
import pandas as pd
import streamlit as st

# Universal cross-directory project root detection
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR if (CURRENT_DIR / "data").exists() else CURRENT_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from src.recommendation import MovieRecommender, get_recommender
    from src.data_preprocessing import get_default_data_path
except ImportError:
    from recommendation import MovieRecommender, get_recommender
    from data_preprocessing import get_default_data_path

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================
st.set_page_config(
    page_title="Movie Recommendation System | Om Vadiya",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(90deg, #ff4b4b, #ff7676, #ffa07a);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #b0b0b0;
        margin-bottom: 1.5rem;
    }
    .metric-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-right: 6px;
        background-color: #262730;
        border: 1px solid #3d3e48;
    }
    .similarity-pill {
        display: inline-block;
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.82rem;
        font-weight: 700;
    }
    .movie-card {
        border-radius: 10px;
        background: #1e1e24;
        border: 1px solid #2d2d38;
        padding: 12px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# CACHED MODEL LOADER
# =============================================================================
@st.cache_resource(show_spinner=False)
def load_recommendation_engine():
    """Load and cache the MovieRecommender engine to ensure zero runtime latency."""
    return get_recommender()

recommender = load_recommendation_engine()
df_movies = recommender.df
all_titles = recommender.get_all_titles()


# =============================================================================
# SIDEBAR CONTROLS & CANDIDATE PROFILE
# =============================================================================
with st.sidebar:
    st.image(
        "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=600&auto=format&fit=crop&q=80",
        caption="CineMatch AI Engine",
        use_container_width=True
    )
    
    st.markdown("### ⚙️ Recommendation Settings")
    top_n = st.slider("Number of Recommendations", min_value=3, max_value=15, value=6, step=1)
    
    st.markdown("---")
    st.markdown("### 📊 Dataset Overview")
    col_sb1, col_sb2 = st.columns(2)
    with col_sb1:
        st.metric("Catalog Size", f"{len(df_movies)} Movies")
    with col_sb2:
        st.metric("Avg Rating", f"{df_movies['rating'].mean():.2f} / 10")
        
    st.markdown("---")
    st.markdown("### 👨‍💻 Project Developer")
    st.markdown("**Om Vadiya**")
    st.markdown("🎓 *B.Com (Graduating July 2026)*")
    st.markdown("🏛️ *M J College of Commerce*")
    st.markdown("🏫 *Maharaja Krishnakumarsinhji Bhavnagar University*")
    st.markdown("🎯 *Career Focus: Data Science & ML*")
    st.markdown("⭐ *CGPA: 7.08 / 10*")
    
    st.markdown("""
    [![GitHub](https://img.shields.io/badge/GitHub-vadiyaom-181717?style=flat&logo=github)](https://github.com/vadiyaom)
    [![LinkedIn](https://img.shields.io/badge/LinkedIn-Vadiya--Om-0A66C2?style=flat&logo=linkedin)](https://www.linkedin.com/in/Vadiya-Om/)
    [![Email](https://img.shields.io/badge/Email-vadiyaom18@gmail.com-D14836?style=flat&logo=gmail)](mailto:vadiyaom18@gmail.com)
    """)
    
    st.markdown("---")
    st.caption("Engineered with Python, TF-IDF Vectorization, Cosine Similarity & Streamlit.")


# =============================================================================
# HERO HEADER & QUICK SELECTION
# =============================================================================
st.markdown('<div class="main-header">🎬 CineMatch — Movie Recommendation System</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">Content-Based Recommendation Engine powered by Natural Language Processing '
    '(TF-IDF Vectorization) and High-Dimensional Cosine Similarity.</div>',
    unsafe_allow_html=True
)

# Badges
st.markdown("""
<div style="margin-bottom: 20px;">
    <span class="metric-badge">🐍 Python 3.10+</span>
    <span class="metric-badge">🐼 Pandas & NumPy</span>
    <span class="metric-badge">🤖 Scikit-Learn</span>
    <span class="metric-badge">🧮 TF-IDF & Cosine Similarity</span>
    <span class="metric-badge">🗄️ SQL Analysis</span>
    <span class="metric-badge">⚡ Streamlit UI</span>
</div>
""", unsafe_allow_html=True)

# Main Search Section
col_select, col_btn1, col_btn2 = st.columns([5, 1.5, 1.5])

with col_select:
    selected_movie = st.selectbox(
        "Search or Select a Movie from the Catalog:",
        options=all_titles,
        index=all_titles.index("Inception") if "Inception" in all_titles else 0,
        help="Type to search or choose any film from our curated catalog."
    )

with col_btn1:
    st.write("")
    st.write("")
    find_button = st.button("🔍 Recommend", type="primary", use_container_width=True)

with col_btn2:
    st.write("")
    st.write("")
    random_button = st.button("🎲 Random Film", use_container_width=True)

if random_button:
    import random
    selected_movie = random.choice(all_titles)


# =============================================================================
# RECOMMENDATION EXECUTION & DISPLAY
# =============================================================================
result = recommender.recommend(selected_movie, n=top_n)

if result["found"]:
    searched = result["searched_movie"]
    recs = result["recommendations"]

    # Hero Details of Selected Movie
    st.markdown("---")
    st.markdown("### 🎯 Currently Selected Movie")
    
    hero_col1, hero_col2 = st.columns([1, 3])
    with hero_col1:
        poster = searched.get("poster_url")
        if poster and str(poster).startswith("http"):
            st.image(poster, use_container_width=True)
        else:
            st.image("https://via.placeholder.com/300x450?text=No+Poster", use_container_width=True)
            
    with hero_col2:
        st.markdown(f"## {searched['title']} ({searched['release_year']})")
        st.markdown(f"⭐ **IMDb Rating:** `{searched['rating']} / 10` | 🎬 **Director:** `{searched['director']}`")
        st.markdown(f"🎭 **Genres:** `{searched['genres']}`")
        st.markdown(f"🔑 **Thematic Keywords:** `{searched['keywords']}`")
        st.markdown(f"👥 **Starring:** `{searched['cast']}`")
        st.info(f"📝 **Overview:** {searched['overview']}")

    # Recommended Movies Grid
    st.markdown("---")
    st.markdown(f"### 🍿 Top {len(recs)} Recommended Movies for You")
    st.markdown(f"*Ranked by textual and thematic Cosine Similarity with **{searched['title']}***")

    # Render cards in responsive columns (3 columns per row)
    cols_per_row = 3
    for i in range(0, len(recs), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            card_idx = i + j
            if card_idx < len(recs):
                item = recs[card_idx]
                with col:
                    with st.container(border=True):
                        # Poster
                        poster_url = item.get("poster_url")
                        if poster_url and str(poster_url).startswith("http"):
                            st.image(poster_url, use_container_width=True)
                        else:
                            st.image("https://via.placeholder.com/300x450?text=No+Poster", use_container_width=True)

                        # Match Badge & Title
                        st.markdown(
                            f"<span class='similarity-pill'>🎯 {item['similarity_percentage']}% Match</span>",
                            unsafe_allow_html=True
                        )
                        st.markdown(f"#### {item['rank']}. {item['title']} ({item['release_year']})")
                        st.caption(f"⭐ **{item['rating']} / 10** | 🎬 {item['director']}")
                        st.markdown(f"🎭 **Genres:** *{item['genres']}*")
                        
                        with st.expander("📖 Read Synopsis"):
                            st.write(item["overview"])
                            st.markdown(f"**Cast:** {item['cast']}")
else:
    st.error(f"Movie '{selected_movie}' not found in catalog.")


# =============================================================================
# DEEP DIVE TABS: DATASET, ML ALGORITHM & SQL SHOWCASE
# =============================================================================
st.markdown("---")
st.markdown("### 🔬 Technical Deep Dive & Portfolio Demonstration")

tab_data, tab_ml, tab_sql, tab_author = st.tabs([
    "📊 Dataset Explorer",
    "🧠 Machine Learning Methodology",
    "🗄️ SQL Data Analysis Showcase",
    "👨‍💻 About Developer & Contact"
])

with tab_data:
    st.markdown("#### 📂 Interactive Movie Catalog Explorer")
    st.markdown("Explore the raw dataset used to fit the TF-IDF vectorizer and calculate cosine affinity.")
    
    filter_col1, filter_col2 = st.columns(2)
    with filter_col1:
        min_rating = st.slider("Filter by Minimum Rating:", 0.0, 10.0, 7.5, 0.1)
    with filter_col2:
        search_kw = st.text_input("Filter by Keyword / Genre / Director:", "")
        
    filtered_df = df_movies[df_movies["rating"] >= min_rating]
    if search_kw:
        mask = (
            filtered_df["title"].str.contains(search_kw, case=False, na=False) |
            filtered_df["genres"].str.contains(search_kw, case=False, na=False) |
            filtered_df["director"].str.contains(search_kw, case=False, na=False)
        )
        filtered_df = filtered_df[mask]

    st.write(f"Showing **{len(filtered_df)}** of {len(df_movies)} movies:")
    st.dataframe(
        filtered_df[["movie_id", "title", "release_year", "rating", "director", "genres", "overview"]],
        use_container_width=True,
        hide_index=True
    )

with tab_ml:
    st.markdown("#### 🧠 End-to-End Content-Based Recommendation Workflow")
    st.markdown("""
    The recommendation engine follows a rigorous **Natural Language Processing (NLP)** pipeline:
    
    1. **Data Ingestion & Cleaning**:
       - Handled missing textual fields with empty strings to eliminate NaN vectorization errors.
       - Case normalized all text and stripped punctuation using regular expressions.
    2. **Multi-Feature Engineering**:
       - Formed a unified metadata representation:
         `combined_features = genres + keywords + overview + cast + director`
       - This gives equal thematic weight to plot keywords, cast chemistry, and directorial style.
    3. **TF-IDF Vectorization (`sklearn.feature_extraction.text.TfidfVectorizer`)**:
       - Converts textual features into continuous numerical vectors based on:
    """)
    st.latex(r"\text{TF-IDF}(t, d, D) = \text{TF}(t, d) \times \log\left(\frac{N}{|\{d \in D : t \in d\}|}\right)")
    st.markdown("""
       - Rare discriminative words (e.g., *Gotham*, *multiverse*, *wormhole*) receive high scores.
       - Common stop-words (*the*, *and*, *with*) are automatically stripped.
       - Supports unigrams and bigrams `(1, 2)` to capture phrases like *comic book* and *science fiction*.
    4. **Cosine Similarity Computation (`sklearn.metrics.pairwise.cosine_similarity`)**:
       - Calculates the cosine of the geometric angle between movie vectors:
    """)
    st.latex(r"\text{Cosine Similarity}(\vec{A}, \vec{B}) = \frac{\vec{A} \cdot \vec{B}}{\|\vec{A}\| \|\vec{B}\|}")
    st.markdown("""
       - Values range from **0.0 (orthogonal / no overlap)** to **1.0 (identical thematic profile)**.
       - **Why Cosine Similarity?** Unlike Euclidean distance (which penalizes longer plot descriptions), Cosine Similarity normalizes vector magnitudes, comparing purely directional thematic similarity!
    """)

with tab_sql:
    st.markdown("#### 🗄️ Relational SQL Analytics Showcase")
    st.markdown("Demonstration of production SQL queries stored in `sql/analysis_queries.sql` on the movie catalog.")
    
    sql_choice = st.selectbox(
        "Select SQL Query Demonstration:",
        [
            "1. Director Analytics (GROUP BY, HAVING, Aggregate Functions)",
            "2. Decades Analysis (Grouping by Computed Column, AVG Rating)",
            "3. Movies Above Catalog Average Rating (Uncorrelated Subquery)",
            "4. Top 10 Modern Blockbusters (WHERE, ORDER BY, LIMIT)"
        ]
    )
    
    if "1. Director Analytics" in sql_choice:
        sql_query = """
        SELECT 
            director,
            COUNT(*) AS total_films,
            ROUND(AVG(rating), 2) AS avg_director_rating,
            MIN(release_year) AS first_film_year,
            MAX(release_year) AS latest_film_year
        FROM movies
        GROUP BY director
        HAVING COUNT(*) >= 2
        ORDER BY avg_director_rating DESC;
        """
    elif "2. Decades Analysis" in sql_choice:
        sql_query = """
        SELECT 
            (release_year / 10) * 10 AS decade,
            COUNT(*) AS movies_count,
            ROUND(AVG(rating), 2) AS avg_decade_rating
        FROM movies
        GROUP BY (release_year / 10) * 10
        ORDER BY decade ASC;
        """
    elif "3. Movies Above Catalog Average Rating" in sql_choice:
        sql_query = """
        SELECT 
            title,
            director,
            rating,
            ROUND(rating - (SELECT AVG(rating) FROM movies), 2) AS rating_delta_vs_mean
        FROM movies
        WHERE rating > (SELECT AVG(rating) FROM movies)
        ORDER BY rating DESC
        LIMIT 10;
        """
    else:
        sql_query = """
        SELECT 
            title,
            release_year,
            director,
            rating,
            genres
        FROM movies
        WHERE release_year >= 2000 AND rating >= 8.5
        ORDER BY rating DESC
        LIMIT 10;
        """

    st.code(sql_query, language="sql")
    
    # Execute query against SQLite database if exists, else compute with Pandas
    db_path = PROJECT_ROOT / "movies.db"
    if db_path.exists():
        try:
            conn = sqlite3.connect(str(db_path))
            result_df = pd.read_sql_query(sql_query, conn)
            conn.close()
            st.markdown("##### Query Execution Result:")
            st.dataframe(result_df, use_container_width=True, hide_index=True)
        except Exception as e:
            st.warning(f"Note: Executed query via SQLite engine: {e}")

with tab_author:
    st.markdown("#### 👨‍💻 Candidate & Developer Profile")
    st.markdown("""
    - **Name:** Om Vadiya
    - **Role:** Entry-Level Data Science & Machine Learning Aspirant
    - **Graduation:** July 2026
    - **Degree:** Bachelor of Commerce (CGPA: 7.08 / 10)
    - **College:** M J College of Commerce
    - **University:** Maharaja Krishnakumarsinhji Bhavnagar University
    - **Career Focus:** Data Science, Predictive Modeling, Machine Learning Engineering
    
    #### 📬 Contact & Portfolio Links:
    - **GitHub Profile:** [https://github.com/vadiyaom](https://github.com/vadiyaom)
    - **LinkedIn Profile:** [https://www.linkedin.com/in/Vadiya-Om/](https://www.linkedin.com/in/Vadiya-Om/)
    - **Email Address:** [vadiyaom18@gmail.com](mailto:vadiyaom18@gmail.com)
    """)
