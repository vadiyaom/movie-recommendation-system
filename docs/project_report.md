# Project Report: Movie Recommendation System

**Author:** Om Vadiya  
**Role:** Entry-Level Data Science Aspirant  
**Degree:** Bachelor of Computer Applications (B.C.A) (Graduating July 2026, CGPA: 7.08/10)  
**Institution:** M J College of Commerce, Maharaja Krishnakumarsinhji Bhavnagar University  
**Contact:** [vadiyaom18@gmail.com](mailto:vadiyaom18@gmail.com) | [GitHub Profile](https://github.com/vadiyaom) | [LinkedIn Profile](https://www.linkedin.com/in/Vadiya-Om/) | [Live Web App](https://movie-recommendation-systemgit-ryp9wamswmrnmusjugepw7.streamlit.app/)  

---

## 1. Introduction
With the exponential proliferation of digital streaming media platforms (e.g., Netflix, Prime Video, Disney+), consumers are faced with an overwhelming volume of content choices—a phenomenon widely described as the *paradox of choice*. Recommendation systems have emerged as an indispensable cornerstone of modern data-driven entertainment ecosystems.

This project delivers an end-to-end, content-based Movie Recommendation System. Built upon core principles of Natural Language Processing (NLP), numerical linear algebra, and relational SQL analytics, the application maps unstructured movie metadata into high-dimensional vector spaces and computes cosine similarities to deliver fast, highly accurate, and explainable movie recommendations.

---

## 2. Problem Statement
In large movie catalogs, users frequently struggle to find relevant titles that align with their specific thematic tastes, favorite directors, or specific plot elements. Standard generic filters (such as sorting solely by year or highest IMDb rating) fail to capture the nuanced thematic affinities between films.

The core challenge addressed by this project is:
> *Given a target movie selected or searched by a user, how can we mathematically evaluate and rank the catalog to surface the top 10 most stylistically and thematically similar movies without requiring personal user rating histories or sensitive user data?*

---

## 3. Objectives
The technical objectives of this portfolio project are:
1. **Data Preprocessing & Hygiene**: Build a reliable preprocessing pipeline in Python and Pandas to clean unstructured textual attributes (genres, keywords, cast, overview, director) and handle missing entries safely.
2. **Feature Engineering**: Consolidate disparate descriptive text fields into an enriched metadata document (`combined_features`) for each movie record.
3. **Machine Learning Model Implementation**: Formulate a high-dimensional vector representation using **TF-IDF (Term Frequency - Inverse Document Frequency)** and quantify pairwise movie similarity using **Cosine Similarity**.
4. **Relational Analytics (SQL)**: Design a structured relational schema and write production-grade analytical SQL queries to extract deep business insights regarding genres, director performance, and user search trends.
5. **Interactive User Interface**: Deliver an interactive, responsive web application via **Streamlit** (with automated latency optimization via precomputed similarity matrices).
6. **Production Version Control & Cloud Deployment**: Organize the repository adhering to professional Data Science standards ready for one-click deployment on free cloud platforms (e.g., Streamlit Community Cloud).

---

## 4. Dataset
The project is built on a curated dataset stored at `data/movies.csv` containing 50 renowned titles spanning multiple decades and diverse genres.

### Dataset Schema
| Column | Data Type | Description |
|---|---|---|
| `movie_id` | Integer | Primary unique identifier for each film. |
| `title` | String | Official commercial release title. |
| `genres` | String | Comma-separated genre classifications (e.g., Action, Sci-Fi). |
| `overview` | String | Plot synopsis detailing character goals and narrative conflicts. |
| `keywords` | String | Curated thematic tags (e.g., *batman*, *superhero*, *time travel*). |
| `cast` | String | Comma-separated list of prominent lead actors and actresses. |
| `director` | String | Primary directing talent. |
| `rating` | Float | Average IMDb viewer rating (range 0.0 to 10.0). |
| `release_year` | Integer | Year of theatrical release. |
| `poster_url` | String | Web URL pointing to high-resolution promotional artwork. |

*(Note: The system is designed dynamically so larger datasets—such as the TMDB 5,000 or TMDB 45,000 dataset—can be dropped directly into `data/movies.csv` without modifying algorithmic logic).*

---

## 5. Technologies Used
| Category | Technology | Purpose & Application |
|---|---|---|
| **Core Language** | Python 3.10+ | Scripting, pipeline construction, algorithmic logic. |
| **Data Manipulation** | Pandas | Tabular data manipulation, handling nulls, transformations. |
| **Numerical Processing** | NumPy | Matrix structures, vector operations, array sorting. |
| **Machine Learning** | Scikit-Learn | `TfidfVectorizer`, `cosine_similarity` computations. |
| **Relational Database** | SQL / SQLite | Schema definition, data integrity, aggregations, CTEs. |
| **Web Application** | Streamlit | Interactive web user interface, parameter widgets, dataframes. |
| **Version Control** | Git & GitHub | Branch management, atomic commits, remote collaboration. |

---

## 6. Data Preprocessing
The preprocessing pipeline (`src/data_preprocessing.py`) executes standard Data Science cleaning practices:
- **Null Value Imputation**: Missing textual attributes are imputed with empty strings (`""`), guaranteeing that vectorizers do not encounter `NaN` float values. Missing numerical ratings are imputed with `0.0`.
- **Text Normalization**: All textual inputs undergo case-folding (lowercase conversion) and regex-based removal of special characters (`re.sub(r"[^\w\s]", " ", text)`), ensuring identical tokens (e.g., "Nolan" and "nolan") map to identical vector dimensions.
- **Whitespace Stripping**: Redundant space sequences are collapsed into single delimiters.

---

## 7. Exploratory Data Analysis (EDA)
Exploratory data analysis conducted in `notebooks/movie_recommendation.ipynb` revealed key distributions:
1. **Rating Distribution**: Movie ratings in the catalog range from 7.0 to 9.2, with a mean rating of ~8.2, reflecting a catalog of critically praised cinema.
2. **Genre Prevalence**: Action, Sci-Fi, and Drama represent the highest frequency genres in the catalog.
3. **Director Concentration**: Prominent directors such as Christopher Nolan have multiple interconnected entries, providing strong benchmark ground-truth pairs (e.g., *The Dark Knight* series, *Inception*, and *Interstellar*).

---

## 8. Feature Engineering
Single-column models frequently fail because plot summaries alone omit directorial nuance, while genre tags alone lack story granularity. 

To overcome this, a unified feature document is generated:
```
combined_features = genres + " " + keywords + " " + overview + " " + cast + " " + director
```
This synthesis ensures that two films sharing an identical director and primary actor receive an additive similarity boost, while retaining semantic thematic relevance from the plot synopsis and keyword tags.

---

## 9. Machine Learning Methodology
The machine learning pipeline implements **Content-Based Filtering**:
1. **Document Corpus Creation**: Each movie's `combined_features` string forms an individual document within a corpus of size $N=50$.
2. **TF-IDF Vectorization**:
   $$\text{TF-IDF}(t, d, D) = \text{TF}(t, d) \times \log\left(\frac{N}{|\{d \in D : t \in d\}|}\right)$$
   - Standard English stop words (*and*, *in*, *of*) are stripped.
   - N-gram range is configured as unigrams and bigrams `(1, 2)` to capture compound terms (*comic book*, *time travel*).
   - The corpus is transformed into a high-dimensional sparse matrix of shape $(N, M)$, where $M$ represents the unique vocabulary size.

---

## 10. Recommendation Algorithm
Pairwise similarity is evaluated using **Cosine Similarity**:
$$\text{Cosine Similarity}(\vec{A}, \vec{B}) = \frac{\vec{A} \cdot \vec{B}}{\|\vec{A}\| \|\vec{B}\|} = \frac{\sum_{i=1}^{m} A_i B_i}{\sqrt{\sum_{i=1}^{m} A_i^2} \sqrt{\sum_{i=1}^{m} B_i^2}}$$

### Step-by-Step Recommendation Generation:
1. Identify the row index $i$ corresponding to the user-queried movie title.
2. Retrieve the $i$-th row from the pairwise Cosine Similarity matrix: $S_i = [s_{i, 0}, s_{i, 1}, \dots, s_{i, N-1}]$.
3. Enumerate similarities as `(movie_index, similarity_score)` tuples.
4. Sort tuples in descending order of similarity score.
5. Exclude the query movie itself (which holds a self-similarity score of $1.0$).
6. Slice the top $K$ items (default $K=10$ or user-selected) and join with movie metadata.

---

## 11. System Architecture
```
┌────────────────────────────────────────────────────────┐
│                   Streamlit Web UI                     │
│    (Sidebar Sliders, Movie Selectbox, Detail Cards)    │
└───────────────────────────┬────────────────────────────┘
                            │ User Selection / Query
                            ▼
┌────────────────────────────────────────────────────────┐
│             MovieRecommender Engine (src)              │
│       - Cached TF-IDF Vectorizer                       │
│       - Precomputed Cosine Similarity Matrix           │
└─────────────┬────────────────────────────┬─────────────┘
              │                            │
              ▼                            ▼
┌──────────────────────────┐  ┌──────────────────────────┐
│ Preprocessing Pipeline   │  │ Relational SQL Analytics │
│ (src/data_preprocessing) │  │ (sql/analysis_queries)   │
└─────────────┬────────────┘  └────────────┬─────────────┘
              │                            │
              ▼                            ▼
       data/movies.csv                 movies.db
```

---

## 12. Results & Verification
The algorithm demonstrates exceptional qualitative alignment with real-world thematic affinity:
- **Query:** *The Dark Knight*  
  **Top Recommendations:** *Batman Begins*, *The Dark Knight Rises*, *The Prestige*, *Inception*.  
  *(Captures DC comics lore, Batman franchise continuity, and Christopher Nolan directorial affinity).*
- **Query:** *Inception*  
  **Top Recommendations:** *Tenet*, *Interstellar*, *The Matrix*, *Shutter Island*.  
  *(Captures complex sci-fi, time/reality manipulation, and lead actor Leonardo DiCaprio).*
- **Query:** *Toy Story*  
  **Top Recommendations:** *Up*, *The Lion King*, *Spider-Man: Into the Spider-Verse*.  
  *(Captures family animation and adventure dynamics).*

---

## 13. Screenshots
Visual evidence of the running application is stored in the `screenshots/` directory:
- `screenshots/home.png`: Main dashboard with search controls and catalog metrics.
- `screenshots/recommendations.png`: Responsive card layout displaying top movie matches and similarity percentages.
- `screenshots/results.png`: Technical deep dive tabs illustrating SQL query execution and cosine similarity metrics.

---

## 14. Limitations
1. **Cold Start for Unseen Metadata**: A purely content-based recommender cannot recommend movies containing vocabulary absent from its training vocabulary unless the matrix is updated.
2. **Serendipity Ceiling**: Content-based systems inherently recommend items similar to what is already known, preventing unexpected cross-genre discoveries.
3. **No Dynamic User Feedback**: Does not currently track personalized individual watch histories or collaborative user ratings over time.

---

## 15. Future Scope
1. **Hybrid Filtering**: Integrate Collaborative Filtering (e.g., Matrix Factorization / SVD) alongside Content-Based Filtering once user interaction datasets are collected.
2. **Live TMDB API Integration**: Dynamically query live movie trailers, streaming provider links, and real-time box office data via TMDB REST API.
3. **Cloud Database Migration**: Migrate SQLite search logs to a cloud PostgreSQL database (e.g., Supabase or Neon).

---

## 16. Conclusion
The Movie Recommendation System provides a robust, production-ready demonstration of foundational Data Science and Machine Learning competencies. Combining structured data preprocessing, natural language vectorization, geometric similarity metrics, analytical SQL queries, and an intuitive Streamlit interface, this project reflects the analytical rigor, clean engineering standards, and practical problem-solving expected of an entry-level Data Science professional.
