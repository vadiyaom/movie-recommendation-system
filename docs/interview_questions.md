# 25 Project-Specific Interview Questions & Answers

**Candidate:** Om Vadiya  
**Role:** Entry-Level Data Scientist  
**Project:** Content-Based Movie Recommendation System  
**Repository:** [movie-recommendation-system](https://github.com/vadiyaom/movie-recommendation-system)  

---

## 🐍 Section 1: Python Core, Data Structures & File Handling

### Question 1: How did you handle file paths across different operating systems (Windows vs Linux) in your project?
**Answer:** In both `src/data_preprocessing.py` and `src/recommendation.py`, I used Python's object-oriented `pathlib.Path` module instead of hardcoding raw strings with backslashes. For example, `Path(__file__).resolve().parent.parent / "data" / "movies.csv"` dynamically resolves the absolute path relative to the executing file. This guarantees that the code runs seamlessly across local Windows environments (PowerShell) and cloud Linux containers (Streamlit Community Cloud).  
**Concept being tested:** File handling, cross-platform portability, `pathlib` vs `os.path`.

---

### Question 2: In what scenarios did you use Python dictionaries versus lists in the recommendation module?
**Answer:** Lists were utilized for ordered collections where sequential index retrieval or sorting was required—such as storing ranked movie recommendation dictionaries, holding vocabulary n-grams, or returning alphabetical movie titles via `get_all_titles()`. Dictionaries were used to represent key-value metadata entities for each movie (e.g., `{"title": ..., "rating": ..., "genres": ...}`) and structured return payloads containing boolean flags, status messages, and recommendation lists, allowing $O(1)$ key lookups.  
**Concept being tested:** Python built-in data structures (lists vs. dictionaries), time complexity.

---

### Question 3: How is modularity achieved through Python functions and classes in this project?
**Answer:** The codebase is decoupled into single-responsibility components: `src/data_preprocessing.py` exposes reusable functions (`load_dataset`, `clean_text`, `handle_missing_values`, `create_combined_features`), while `src/recommendation.py` encapsulates state inside the `MovieRecommender` class. The class initializes the model once, caches the TF-IDF matrix and similarity matrix, and exposes public query methods (`recommend`, `get_all_titles`). This prevents redundant re-computation on every user search request.  
**Concept being tested:** Object-Oriented Programming (OOP), modular programming, separation of concerns.

---

## 🐼 Section 2: Pandas, NumPy & Data Cleaning

### Question 4: How did you identify and handle missing values in your dataset?
**Answer:** I used `df.isnull().sum()` during exploratory analysis to identify missing values. For textual columns (`genres`, `overview`, `keywords`, `cast`, `director`), I used `fillna("")` to impute missing entries with empty strings. Text vectorization breaks if `NaN` floats are passed into string concatenation or tokenizers. For numerical columns (`rating`), I used `pd.to_numeric(errors="coerce").fillna(0.0)` to ensure valid numerical types without discarding entire rows.  
**Concept being tested:** Missing value treatment, imputation strategies, Pandas `fillna()`.

---

### Question 5: What is the difference between `df.copy()` and a slice assignment in Pandas, and where did you use it?
**Answer:** When cleaning data inside `handle_missing_values()` and `create_combined_features()`, I explicitly called `df.copy()`. If you modify a DataFrame slice directly without `.copy()`, Pandas produces a `SettingWithCopyWarning` because it cannot determine whether you are modifying a copy or the original DataFrame in memory. `.copy()` creates an independent deep copy of the underlying data buffer.  
**Concept being tested:** Pandas memory views vs copies, avoidance of `SettingWithCopyWarning`.

---

### Question 6: How does NumPy assist in calculating and sorting recommendation similarities?
**Answer:** The pairwise Cosine Similarity calculation produces a 2-dimensional NumPy `ndarray` of dimensions $(N, N)$. NumPy enables highly optimized C-level vector operations. When searching for similar movies, we extract the row vector for the target film and use NumPy's vector indexing and array sorting routines (`argsort()[::-1]` or enumerated sorting) to rapidly locate indices of the highest cosine values.  
**Concept being tested:** NumPy multidimensional arrays, vector indexing, performance optimization.

---

## 🗄️ Section 3: Relational SQL Analytics

### Question 7: Explain the difference between `WHERE` and `HAVING` using an example from your `sql/analysis_queries.sql`.
**Answer:** The `WHERE` clause filters individual rows *before* any grouping or aggregation takes place. The `HAVING` clause filters aggregated groups *after* the `GROUP BY` clause has collapsed the rows. In our project's director analytics query:
```sql
SELECT director, COUNT(*) AS total_films, AVG(rating) AS avg_director_rating
FROM movies
WHERE release_year >= 2000
GROUP BY director
HAVING COUNT(*) >= 2;
```
Here, `WHERE` first discards pre-2000 films; then `GROUP BY` aggregates films by director; finally, `HAVING` retains only directors with 2 or more films in that subset.  
**Concept being tested:** SQL execution order, row-level filtering vs group-level filtering.

---

### Question 8: Why did you normalize genres into a many-to-many junction table (`movie_genres`) in `sql/create_tables.sql`?
**Answer:** In the raw CSV dataset, genres are stored as a comma-delimited string (e.g., `"Action, Crime, Drama"`), which violates First Normal Form (1NF) requiring atomic column values. By designing three tables—`movies`, `genres` (lookup table), and `movie_genres` (junction table holding foreign keys `movie_id` and `genre_id`)—we eliminate data redundancy, prevent update anomalies, and allow fast indexed joins to calculate genre-level aggregations.  
**Concept being tested:** Database normalization (1NF, 2NF, 3NF), relational schema design, junction tables.

---

### Question 9: What is a Common Table Expression (CTE), and how did you use it in your SQL analysis?
**Answer:** A CTE is a temporary named result set defined using the `WITH` clause that exists only during the execution scope of a single SQL query. It improves readability and modularity compared to nested subqueries. In Query 10 of `sql/analysis_queries.sql`, I used a CTE named `RankedGenreMovies` containing a `DENSE_RANK() OVER (PARTITION BY genre_name ORDER BY rating DESC)` window function, and then selected the top movie for each genre where `rank_within_genre = 1`.  
**Concept being tested:** SQL CTEs (`WITH` clause), query modularity, window ranking functions.

---

### Question 10: What is the difference between an `INNER JOIN` and a `LEFT JOIN` in your project queries?
**Answer:** An `INNER JOIN` returns only records that have matching keys in both tables. When joining `movies` and `movie_genres`, it returns only movies that have assigned genre associations. A `LEFT JOIN` returns all rows from the left table, and matching rows from the right table (or `NULL` if no match exists). In our search history analysis, we used a `LEFT JOIN` between `movies` and `search_history` so that films with zero search history are still included in the report with a count of `0` via `COALESCE`.  
**Concept being tested:** SQL JOIN types, handling unmatched records, `COALESCE` function.

---

### Question 11: What is a Subquery, and how does a scalar subquery differ from a correlated subquery?
**Answer:** A subquery is an inner query nested within an outer `SELECT`, `FROM`, or `WHERE` statement. A scalar subquery returns a single scalar value (one row, one column) and executes independently—for example:
```sql
SELECT title, rating FROM movies WHERE rating > (SELECT AVG(rating) FROM movies);
```
A correlated subquery references columns from the outer query table, executing once for every candidate row evaluated by the outer query.  
**Concept being tested:** SQL subqueries, scalar vs correlated subqueries.

---

## 🤖 Section 4: Machine Learning & Recommendation Systems

### Question 12: What is Content-Based Filtering, and how does it differ from Collaborative Filtering?
**Answer:** Content-Based Filtering recommends items based on the **intrinsic features** of the items themselves (e.g., director, plot, genre, cast) and a user's known preference for a specific item. Collaborative Filtering recommends items based on the **collective interaction behavior** of multiple users (e.g., user-item rating matrices, user similarities). Content-Based Filtering does not suffer from the cold-start problem for new items because as long as metadata exists, the item can be vectorized immediately.  
**Concept being tested:** Recommendation system paradigms, Content-Based vs Collaborative Filtering, cold-start dynamics.

---

### Question 13: Explain the mathematical intuition behind TF-IDF vectorization.
**Answer:** TF-IDF stands for Term Frequency-Inverse Document Frequency.
- **Term Frequency (TF)** measures how often a word occurs in a specific movie's metadata string: $\text{TF}(t, d) = \frac{\text{count}(t \text{ in } d)}{\text{total words in } d}$.
- **Inverse Document Frequency (IDF)** measures how rare or informative that word is across the entire corpus: $\text{IDF}(t, D) = \log\left(\frac{N}{\text{DF}(t)}\right)$.
Multiplying $\text{TF} \times \text{IDF}$ gives high weight to words that are frequent in a specific movie but rare across other movies (e.g., *Gotham*, *Joker*, *Pandora*), while suppressing common stop words (e.g., *the*, *a*, *movie*).  
**Concept being tested:** Natural Language Processing (NLP), text representation, mathematical formulation of TF-IDF.

---

### Question 14: What is Cosine Similarity, and why did you choose it over Euclidean Distance?
**Answer:** Cosine Similarity measures the cosine of the angle between two non-zero vectors in an $M$-dimensional space:
$$\text{Cosine Similarity}(\vec{A}, \vec{B}) = \frac{\vec{A} \cdot \vec{B}}{\|\vec{A}\| \|\vec{B}\|}$$
Euclidean distance measures the straight-line distance between points in space, which is heavily distorted by document length: a long movie overview with 150 words would be placed far away from a short overview of 30 words even if they discussed the exact same topic. Cosine Similarity normalizes vector length by their Euclidean norms, evaluating purely directional alignment and thematic affinity.  
**Concept being tested:** Vector similarity metrics, Cosine Similarity vs Euclidean Distance, impact of vector magnitude.

---

### Question 15: Why didn't you split your dataset into Train and Test sets in this project?
**Answer:** Unsupervised content-based recommendation systems using deterministic vector similarity metrics (TF-IDF + Cosine Similarity) do not learn parametric weights or minimize a loss function via gradient descent. The entire corpus serves as the reference catalog. A train/test split is essential when training supervised models (like regression or classification) or collaborative filtering models with explicit user ground-truth ratings ($y$) to evaluate metrics like RMSE or NDCG@K.  
**Concept being tested:** Supervised vs unsupervised machine learning, train-test splitting rationale.

---

### Question 16: What is Overfitting, and does it apply to this TF-IDF recommendation engine?
**Answer:** Overfitting occurs when a machine learning model memorizes patterns or noise in training data, resulting in poor generalization on unseen test data. In TF-IDF content-based filtering, classical parameter overfitting does not occur because there are no model weights being optimized. However, a related issue is vocabulary over-specificity: if you include too many high-order n-grams or rare tokens without minimum document frequency thresholds (`min_df`), vectors become overly sparse, leading to zero similarity between related films.  
**Concept being tested:** Machine learning generalization, overfitting, vocabulary sparsity.

---

### Question 17: How would you evaluate the performance of this recommendation system in a production environment?
**Answer:** Since offline rating ground-truth is absent, evaluation can be conducted through:
1. **Offline Qualitative & Sanity Checks:** Verifying known domain pairs (e.g., *Batman Begins* queries must retrieve *The Dark Knight* in top-3).
2. **Catalog Coverage & Diversity:** Calculating the percentage of total movies ever recommended across all queries, and average inter-list similarity.
3. **Online A/B Testing:** Measuring user engagement metrics in production—Click-Through Rate (CTR) on recommended movies, watch duration, and session retention.  
**Concept being tested:** Evaluation metrics for recommender systems (CTR, Coverage, Diversity, Serendipity).

---

## 🔬 Section 5: Feature Engineering & Preprocessing

### Question 18: What is Feature Engineering, and what features did you engineer in this project?
**Answer:** Feature Engineering is the process of creating new representations or combining existing raw variables to improve model performance. In this project, individual metadata columns (`genres`, `keywords`, `overview`, `cast`, `director`) each held incomplete signals. I engineered a composite feature column called `combined_features`:
```python
df["combined_features"] = genres + " " + keywords + " " + overview + " " + cast + " " + director
```
This synthesized representation allowed the vectorizer to simultaneously capture narrative theme, genre identity, cast collaboration, and directorial style.  
**Concept being tested:** Feature Engineering, multimodal text aggregation.

---

### Question 19: Why did you configure `ngram_range=(1, 2)` in your `TfidfVectorizer`?
**Answer:** An n-gram is a contiguous sequence of $n$ items from a given sample of text. A unigram $(1)$ considers single words (e.g., `"comic"`, `"book"`), whereas a bigram $(2)$ considers word pairs (e.g., `"comic book"`, `"science fiction"`). By using `(1, 2)`, the model preserves the semantic meaning of compound phrases that have vastly different contexts when broken into isolated words.  
**Concept being tested:** Text tokenization, n-gram representation in NLP.

---

## ⚡ Section 6: Deployment, Streamlit & Version Control

### Question 20: What is Streamlit, and why is it preferred for Data Science portfolio applications?
**Answer:** Streamlit is an open-source Python framework designed for rapid development of interactive web applications for machine learning and data science. It enables Python developers to create rich, stateful user interfaces containing sliders, search inputs, dataframes, and charts with zero frontend HTML/CSS/JavaScript overhead, allowing rapid prototyping and direct integration with Pandas and Scikit-Learn.  
**Concept being tested:** Web application frameworks for Data Science, Streamlit architecture.

---

### Question 21: How does caching improve the performance of your Streamlit application?
**Answer:** In Streamlit, any user interaction causes the entire Python script to rerun from top to bottom. If the CSV reading, TF-IDF vector fitting, and pairwise cosine similarity calculation were repeated on every click, the user would experience substantial latency. By wrapping the initialization in `@st.cache_resource`, Streamlit caches the fitted `MovieRecommender` instance in memory across sessions and reruns, reducing recommendation response time to sub-10 milliseconds.  
**Concept being tested:** Streamlit caching (`@st.cache_resource` / `@st.cache_data`), latency optimization.

---

### Question 22: What is the purpose of `requirements.txt` and why should it only include essential libraries?
**Answer:** `requirements.txt` specifies the exact Python packages and minimum versions required to reproduce the execution environment. In cloud platforms like Streamlit Community Cloud or Render, the build process runs `pip install -r requirements.txt`. Keeping it minimal (only `pandas`, `numpy`, `scikit-learn`, `streamlit`) accelerates container build time, minimizes memory consumption, prevents dependency conflicts, and avoids security vulnerabilities from unneeded packages.  
**Concept being tested:** Dependency management, reproducibility, deployment build pipelines.

---

### Question 23: Explain the role of `.gitignore` in a collaborative Data Science repository.
**Answer:** The `.gitignore` file specifies intentionally untracked files that Git should ignore. It prevents virtual environments (`venv/`, `.venv/`), compiled Python bytecode (`__pycache__/`, `*.pyc`), IDE configurations (`.vscode/`), and OS temporary files (`.DS_Store`) from being committed to the repository. This keeps the GitHub repository lightweight, prevents secrets or local cache leakage, and ensures that team members do not encounter conflicting environment artifacts.  
**Concept being tested:** Git version control best practices, repository hygiene.

---

### Question 24: What are the primary steps to deploy this repository to Streamlit Community Cloud for free?
**Answer:**
1. Push the project codebase to a public GitHub repository with `requirements.txt` and `src/app.py`.
2. Navigate to [share.streamlit.io](https://share.streamlit.io) and sign in using GitHub OAuth.
3. Click "New App", select the repository (`vadiyaom/movie-recommendation-system`), choose branch `main`, and set the App entry point file path to `src/app.py`.
4. Click "Deploy". Streamlit provisions a free container, installs dependencies from `requirements.txt`, and generates a public URL (e.g., `https://vadiyaom-movie-recommender.streamlit.app`).  
**Concept being tested:** Cloud deployment workflow, continuous deployment from GitHub.

---

### Question 25: What is the difference between `git add .`, `git commit -m`, and `git push`?
**Answer:**
- `git add .`: Moves all newly created and modified files in the working directory to the Git staging area (Index).
- `git commit -m "message"`: Records a permanent, versioned snapshot of the staged files in the local Git repository history, accompanied by a descriptive log message.
- `git push -u origin main`: Transfers the local commits from the local `main` branch to the remote repository on GitHub (`origin`), setting up upstream tracking.  
**Concept being tested:** Git core commands, three-tier Git architecture (Working Directory -> Staging Area -> Local Repository -> Remote Repository).
