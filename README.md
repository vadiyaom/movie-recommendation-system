# 🎬 CineMatch — Movie Recommendation System

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.x-black?logo=flask)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3%2B-orange?logo=scikit-learn)
![Deployment](https://img.shields.io/badge/Deploy-Render%20Free%20Tier-success?logo=render)
![License](https://img.shields.io/badge/License-MIT-green)

A complete, production-ready **Content-Based Movie Recommendation System** built with **Python, Scikit-Learn, and Flask**. It vectorizes rich movie metadata (genres, overview, keywords, cast, and director) using **TF-IDF Vectorization** and computes high-dimensional **Cosine Similarity** to instantly recommend the top 10 movies most similar to any searched title.

Designed specifically for **$0 / ₹0 free deployment** on **Render**, requiring **no paid APIs**, **no paid databases**, and **no paid cloud infrastructure**.

---

## 🌟 Key Features

- **Content-Based Machine Learning Engine**: Uses TF-IDF and Cosine Similarity to find thematic and stylistic movie affinities.
- **Top 10 Recommendations**: Displays interactive movie cards with poster artwork, genre tags, IMDb rating, release year, overview, and percentage similarity match.
- **Zero Runtime Latency**: The TF-IDF matrix and similarity models are precomputed at server startup so user searches respond in milliseconds.
- **Search History Logging**: Stores successful search queries in an SQLite database using parameterized queries to prevent SQL injection.
- **Robust Fallback Handling**:
  - Gracefully handles unknown movies with helpful suggestions.
  - Automatically renders custom CSS poster fallbacks if remote poster image links fail or the user is offline.
  - Validates empty search inputs on both frontend and backend.
- **Modern Responsive Dark Theme**: Handcrafted cinema dark aesthetic with glassmorphism, glowing micro-animations, and mobile responsiveness without heavy UI frameworks.
- **Free Cloud Ready**: Includes `render.yaml` for 1-click Render blueprint deployment.

---

## 🏗️ Project Architecture

```text
index.html / recommendations.html (Frontend UI)
       │
       ▼ (HTTP GET / POST)
   Flask Application (app.py)
       │
       ├─────────────────────────────────┐
       ▼                                 ▼
Recommendation Engine (src/recommendation.py)   SQLite Database (database.py)
       │                                         │
       ▼                                         ▼
Preprocessing Pipeline (src/data_preprocessing.py)  movies.db (Search History)
       │
       ▼
Movie Dataset (data/movies.csv)
```

---

## 🧠 Machine Learning Workflow

```text
                 MOVIE DATASET (movies.csv)
                            ↓
                      DATA CLEANING
             (Handle NaNs, Lowercase, Normalize)
                            ↓
                   FEATURE ENGINEERING
           (genres + keywords + overview + cast + director)
                            ↓
                 COMBINE MOVIE FEATURES
                            ↓
                    TF-IDF VECTORIZATION
             (TfidfVectorizer: 1-gram & 2-gram)
                            ↓
                     TF-IDF MATRIX
                            ↓
                   COSINE SIMILARITY
             (Pairwise Dot Product / Norms)
                            ↓
                   SIMILARITY SCORES
                            ↓
                      SORT MOVIES
                 (Descending Affinity)
                            ↓
               EXCLUDE SEARCHED QUERY MOVIE
                            ↓
                TOP 10 RECOMMENDATIONS
                            ↓
                     FLASK WEBSITE
```

---

## 📁 Project Folder Structure

```text
Movie-Recommendation-System/
│
├── data/
│   └── movies.csv                 # 50-movie curated dataset with metadata & posters
│
├── notebooks/
│   └── movie_recommendation.ipynb # Step-by-step Data Science & EDA notebook
│
├── src/
│   ├── __init__.py                # Package initializer
│   ├── data_preprocessing.py      # Cleaning and feature engineering pipeline
│   └── recommendation.py          # TF-IDF & Cosine Similarity recommendation engine
│
├── templates/
│   ├── index.html                 # Main search UI & history view
│   └── recommendations.html       # Top 10 recommendations grid & hero card
│
├── static/
│   ├── css/
│   │   └── style.css              # Custom cinema dark theme stylesheet
│   └── js/
│       └── script.js              # Interactivity, loading states & poster fallback
│
├── app.py                         # Flask web application controller & routes
├── database.py                    # SQLite search history manager
├── requirements.txt               # Lightweight production dependencies
├── render.yaml                    # Render Free Web Service deployment spec
├── .gitignore                     # Git ignore rules for clean repository
└── README.md                      # Comprehensive project documentation
```

---

## 📊 Dataset Information

The application includes `data/movies.csv` featuring 50 popular films spanning sci-fi, action, crime, drama, animation, and fantasy. Each record contains:

| Column | Description | Example |
|---|---|---|
| `movie_id` | Unique identifier | `1` |
| `title` | Official release title | `The Dark Knight` |
| `genres` | Primary genre classifications | `Action, Crime, Drama` |
| `overview` | Synopsis of the plot | `When the menace known as the Joker...` |
| `keywords` | Descriptive plot and theme tags | `batman dc comics joker gotham vigilante` |
| `cast` | Lead actors and actresses | `Christian Bale, Heath Ledger, Aaron Eckhart` |
| `director` | Directing talent | `Christopher Nolan` |
| `rating` | Average viewer rating (0–10) | `9.0` |
| `release_year` | Original release year | `2008` |
| `poster_url` | High-resolution public poster URL | `https://image.tmdb.org/t/p/w500/...` |

### Scaling to a Larger Dataset
To expand the catalog to 5,000+ or 45,000+ titles:
1. Download the public [TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata) or [The Movies Dataset](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset) from Kaggle for free.
2. Ensure the CSV contains the matching column headers or map them in `src/data_preprocessing.py`.
3. Place the file at `data/movies.csv`. The recommendation engine will automatically process the new records at startup!

> **Dataset Disclaimer**: The application code is licensed separately under MIT. Third-party movie metadata and imagery belong to their respective copyright holders (e.g. TMDB). Please review and comply with their terms of use for commercial redistribution.

---

## 💻 Local Installation (Windows & Linux)

### Step 1: Open Terminal / PowerShell
Clone or navigate to your project directory:
```powershell
cd e:\Desktop\movie
```

### Step 2: Create a Virtual Environment
```powershell
python -m venv venv
```

### Step 3: Activate the Virtual Environment
- **On Windows (PowerShell):**
  ```powershell
  venv\Scripts\Activate.ps1
  ```
  *(If PowerShell displays an execution policy warning, run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` once).*
- **On Windows (Command Prompt):**
  ```cmd
  venv\Scripts\activate.bat
  ```
- **On macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

### Step 4: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 5: Run the Flask Web Application
```powershell
python app.py
```

### Step 6: Open in Your Browser
Visit:
```text
http://127.0.0.1:5000
```

---

## 🚀 Free Deployment Guide on Render ($0 / ₹0)

Render provides free hosting for Python web services with automated GitHub deployments.

### Step 1: Create a Free GitHub Account & Repository
1. Go to [github.com](https://github.com) and create a free account if you haven't already.
2. Click **New Repository**, name it `movie-recommendation-system`, select **Public**, and click **Create repository**.

### Step 2: Push Your Code to GitHub
Run the following commands inside your local project root:

```bash
# 1. Initialize git version control
git init

# 2. Stage all project files (ignoring files specified in .gitignore)
git add .

# 3. Create the initial commit
git commit -m "Initial Movie Recommendation System"

# 4. Set the default branch to main
git branch -M main

# 5. Connect your remote GitHub repository (replace with your URL)
git remote add origin https://github.com/YOUR_USERNAME/movie-recommendation-system.git

# 6. Push code to GitHub
git push -u origin main
```

**Explanation of Git Commands for Beginners:**
- `git init`: Initializes a new Git repository locally.
- `git add .`: Packages all changes in the current directory ready for committing.
- `git commit -m "..."`: Records a snapshot of your files with a descriptive message.
- `git branch -M main`: Renames your primary working branch to `main`.
- `git remote add origin <URL>`: Links your local computer folder to your remote GitHub page.
- `git push -u origin main`: Uploads your committed files to GitHub.

---

### Step 3: Create a Free Account on Render
1. Visit [render.com](https://render.com) and click **Sign Up** using your GitHub account.

### Step 4: Deploy the Web Service
1. In your Render Dashboard, click **New +** and select **Web Service**.
2. Select **Build and deploy from a Git repository** and connect your `movie-recommendation-system` repository.
3. Configure the service settings:
   - **Name**: `cine-movie-recommender` (or any unique name)
   - **Region**: Choose the region closest to you (e.g. Frankfurt, Oregon, Singapore)
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: **Free** ($0 / month)
4. Click **Deploy Web Service**.

### Step 5: Access Your Live Application
Render will provision the container, install dependencies, and launch Gunicorn. Within 2–3 minutes, your live public URL will be ready:
```text
https://cine-movie-recommender.onrender.com
```

---

## ⚠️ Free Deployment Limitations & Architecture Considerations

Render's free tier provides generous compute resources for personal portfolios and university projects. Keep the following operational characteristics in mind:

1. **Inactivity Sleep & Cold Starts**: Free Render web services spin down after 15 minutes of inactivity. When a new visitor accesses the URL, the initial request takes approximately 30–50 seconds to warm up ("cold start"). Subsequent requests are fast and responsive.
2. **Ephemeral SQLite Filesystem**: Free instances do not include persistent disk attachments. If the container restarts or re-deploys, changes written to `movies.db` (search history) may reset.
   - **Why this design is safe**: The recommendation system runs entirely off `data/movies.csv` and Scikit-Learn in-memory data structures. It **never depends on SQLite for recommendations**. Search history is an optional perk, and database errors are isolated with fail-safe exception guards.
   - **If permanent persistence is required later**: You can easily swap the SQLite connection for a free cloud PostgreSQL database (e.g. Supabase, Neon, or Render Free Postgres).

---

## 🔬 Data Science & Machine Learning Deep Dive

### What is Content-Based Filtering?
Content-Based Filtering is an information retrieval technique that recommends items based on the **intrinsic characteristics of the items themselves** rather than user behavior. In movie recommendation, if a user enjoys *The Dark Knight*, the algorithm analyzes attributes such as genres (*Action, Crime*), directors (*Christopher Nolan*), lead actors (*Christian Bale*), and plot keywords (*vigilante, Gotham*) to recommend other films sharing these features.

### What is TF-IDF?
**TF-IDF** stands for **Term Frequency-Inverse Document Frequency**:
$$\text{TF-IDF}(t, d, D) = \text{TF}(t, d) \times \text{IDF}(t, D)$$
1. **Term Frequency (TF)**: How frequently a word $t$ appears in a specific movie's description $d$.
2. **Inverse Document Frequency (IDF)**: Measures how common or rare a word is across the entire movie catalog $D$:
   $$\text{IDF}(t, D) = \log\left(\frac{N}{|\{d \in D : t \in d\}|}\right)$$
- Common words (like "the", "a", "movie") appear in all descriptions and receive an IDF weight near zero.
- Distinctive words (like "joker", "gotham", "wormhole", "pandora", "mob") appear in only a few movies and receive a high IDF weight.

### What is Cosine Similarity?
Cosine Similarity evaluates the geometric cosine of the angle between two multi-dimensional feature vectors $\vec{A}$ and $\vec{B}$:
$$\text{Cosine Similarity}(\vec{A}, \vec{B}) = \frac{\vec{A} \cdot \vec{B}}{\|\vec{A}\| \|\vec{B}\|} = \frac{\sum_{i=1}^{n} A_i B_i}{\sqrt{\sum_{i=1}^{n} A_i^2} \sqrt{\sum_{i=1}^{n} B_i^2}}$$
- **Value of 1.0 (100%)**: The two vectors point in the identical direction (maximal thematic similarity).
- **Value of 0.0 (0%)**: The vectors are perpendicular (no overlapping relevant vocabulary).

### Why Do Similar Movies Receive Higher Scores?
When two movies share uncommon tokens (e.g., "Christopher Nolan", "Christian Bale", "Gotham", "vigilante"), the dot product of their TF-IDF vectors produces a high numerator. Because the vectors are normalized by Euclidean magnitude, long overviews do not artificially bias the score, ensuring fair comparison.

---

## 🧪 Testing Guide

Verify the system using the following test cases:

| Test Case | User Input | Expected Result |
|---|---|---|
| **Test 1** | `The Dark Knight` | Renders top recommendations (*Batman Begins*, *The Dark Knight Rises*, *The Prestige*, etc.) with >20% affinity. |
| **Test 2** | `Inception` | Returns mind-bending sci-fi films (*Tenet*, *Interstellar*, *The Matrix*, *Shutter Island*). |
| **Test 3** | `xyzabc123` | Does **not** crash. Displays: *"Movie 'xyzabc123' not found. Please enter a movie from our available movie list."* |
| **Test 4** | *(Empty string)* | Client-side validation prompts user; backend displays: *"Please enter a movie name to get recommendations."* |

---

## 🛠️ Common Errors & Solutions

1. **`ModuleNotFoundError: No module named 'sklearn'`**
   - **Cause**: Virtual environment not activated or dependencies not installed.
   - **Fix**: Run `venv\Scripts\activate` followed by `pip install -r requirements.txt`.
2. **`Address already in use: Port 5000`**
   - **Cause**: Another service or previous Flask instance is still running on port 5000.
   - **Fix**: Run `python app.py` on another port via environment variable `$env:PORT="5001"; python app.py` or stop the running process.
3. **Images not loading / Red cross icon**
   - **Cause**: Slow internet or restricted network blocking TMDB image domains.
   - **Fix**: The application includes an automatic JavaScript error trap (`handlePosterError`) that gracefully converts broken images into an elegant CSS gradient poster card with the movie title.

---

## 💼 Resume & Portfolio Description

Use this summary on your resume, LinkedIn, or during interviews:

> **Movie Recommendation System**
> *Python | Pandas | Scikit-learn | Flask | SQLite | Render*
> - Engineered an end-to-end content-based movie recommendation web application using TF-IDF vectorization and Cosine Similarity across multi-field metadata (genres, plot synopsis, cast, and director).
> - Optimized search latency by precomputing vector matrices at startup, delivering sub-10ms recommendations.
> - Developed a full-stack Flask application with automated SQLite query logging, responsive Jinja2 templates, and deployed online using Render's free cloud infrastructure.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute this software for educational and personal portfolio purposes.
