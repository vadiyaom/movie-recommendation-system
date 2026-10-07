/**
 * CineMatch - Frontend Interactivity & Fallback Logic
 * 
 * Handles:
 * 1. Form validation & loading feedback
 * 2. Quick tag selection
 * 3. Graceful poster image fallback for offline or broken TMDB links
 */

document.addEventListener("DOMContentLoaded", () => {
    initSearchForm();
});

/**
 * Handle form submission state, validate non-empty queries,
 * and provide visual feedback to the user.
 */
function initSearchForm() {
    const form = document.getElementById("recommendation-form");
    const input = document.getElementById("movie-search-input");
    const submitBtn = document.getElementById("search-submit-btn");

    if (!form || !input || !submitBtn) return;

    form.addEventListener("submit", (e) => {
        const query = input.value.trim();

        if (!query) {
            e.preventDefault();
            alert("Please enter a movie name to get recommendations.");
            input.focus();
            return;
        }

        // Show loading state and prevent duplicate clicks
        const btnText = submitBtn.querySelector(".btn-text");
        const btnSpinner = submitBtn.querySelector(".btn-spinner");

        if (btnText && btnSpinner) {
            btnText.style.display = "none";
            btnSpinner.style.display = "inline-block";
        }

        submitBtn.disabled = true;
    });
}

/**
 * Click handler for popular / trending movie suggestion chips
 * Automatically fills the search input and submits the search form.
 * 
 * @param {string} movieTitle - Title of the selected movie
 */
function selectMovie(movieTitle) {
    const input = document.getElementById("movie-search-input");
    const form = document.getElementById("recommendation-form");

    if (input && form) {
        input.value = movieTitle;
        // Trigger submit
        form.requestSubmit ? form.requestSubmit() : form.submit();
    }
}

/**
 * Fallback handler for missing or broken poster images.
 * Replaces the failed image with an elegant in-card gradient placeholder.
 * 
 * @param {HTMLImageElement} imgElement - The failed image element
 * @param {string} movieTitle - Title of the movie to display on the placeholder
 */
function handlePosterError(imgElement, movieTitle) {
    // Avoid infinite loop if fallback itself encounters an issue
    imgElement.onerror = null;

    // Create a styled fallback block
    const fallbackDiv = document.createElement("div");
    fallbackDiv.className = "poster-fallback";
    fallbackDiv.innerHTML = `
        <div class="poster-fallback-icon">🎬</div>
        <div class="poster-fallback-title">${escapeHtml(movieTitle || "Movie Poster")}</div>
    `;

    // Replace the img tag with the fallback container
    if (imgElement.parentElement) {
        imgElement.parentElement.replaceChild(fallbackDiv, imgElement);
    }
}

/**
 * Basic HTML escaping utility for safe rendering
 */
function escapeHtml(text) {
    const div = document.createElement("div");
    div.innerText = text;
    return div.innerHTML;
}
