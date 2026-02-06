
import streamlit as st
st.set_page_config(
    page_title="CineMatch | Movie Recommender",
    layout="wide"
)


import pandas as pd
import pickle
import requests
import urllib.parse


with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


st.markdown("""
<div class="app-header">
  <h1>🎬 CineMatch</h1>
  <p>AI-Powered Content-Based Movie Recommendation System</p>
  <p class="how">
    Select a movie → cosine similarity on metadata → top 5 recommendations
  </p>
</div>
""", unsafe_allow_html=True)


def platform_links(movie_name):
    query = urllib.parse.quote(movie_name)
    st.markdown(f"""
    <a href="https://www.youtube.com/results?search_query={query}"
       target="_blank" class="stLinkButton">▶ Trailer</a>
    <a href="https://www.amazon.com/s?k={query}&i=instant-video"
       target="_blank" class="stLinkButton">🎬 Watch</a>
    """, unsafe_allow_html=True)

#FETCH POSTER
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}"
        params = {
            "api_key": "e967c734f0f420217b114ed68f925d82",
            "language": "en-US"
        }
        res = requests.get(url, params=params, timeout=5)
        data = res.json()
        poster_path = data.get("poster_path")

        if poster_path:
            return f"https://image.tmdb.org/t/p/original{poster_path}"
        return "https://via.placeholder.com/300x450?text=No+Poster"

    except:
        return "https://via.placeholder.com/300x450?text=Error"

#LOAD DATA
movies_dict = pickle.load(open("movie_listap.pkl", "rb"))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open("similarityap.pkl", "rb"))

#RECOMMEND FUNCTION
def recommend(movie):
    index = movies[movies["title"] == movie].index[0]
    distances = similarity[index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    names, posters, scores = [], [], []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        names.append(movies.iloc[i[0]].title)
        posters.append(fetch_poster(movie_id))
        scores.append(round(i[1] * 100, 2))

    return names, posters, scores

#MOVIE SELECT
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    selected_movie = st.selectbox(
        "Select a movie",
        movies["title"].values
    )
    show_btn = st.button("Show Recommendations")

#SHOW RESULTS
if show_btn:
    names, posters, scores = recommend(selected_movie)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("<h3 class='section-title'>Recommended Movies</h3>",
                unsafe_allow_html=True)

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.markdown(f"""
            <div class="movie-card">
              <div class="poster-wrap">
                <img src="{posters[i]}">
                <div class="rating-badge">⭐ {scores[i]}%</div>
              </div>

              <div class="movie-title">{names[i]}</div>

              <div class="why-list">
                <span>🎭 Similar genres</span>
                <span>🧩 Similar keywords</span>
                <span>📐 Cosine similarity</span>
              </div>
            </div>
            """, unsafe_allow_html=True)

            platform_links(names[i])

#FOOTER
st.markdown("""
<hr class="divider">
<p class="footer">
Built by <b>Maneesh Chauhan</b><br>
Content-Based Movie Recommendation System<br>
Powered by TMDB & Streamlit
</p>
""", unsafe_allow_html=True)
