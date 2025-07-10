import streamlit as st
import requests 
import pickle

# Background image URL
background_url = "https://assets.nflxext.com/ffe/siteui/vlv3/8200f588-2e93-4c95-8eab-ebba17821657/web/IN-en-20250616-TRIFECTA-perspective_9cbc87b2-d9bb-4fa8-9f8f-a4fe8fc72545_large.jpg"

# Load all necessary Netflix Sans weights
st.markdown("""
    <style>
    @font-face {
        font-family: 'Netflix Sans';
        font-weight: 400;
        font-style: normal;
        src: url(https://assets.nflxext.com/ffe/siteui/fonts/netflix-sans/v3/NetflixSans_W_Rg.woff2) format('woff2'),
             url(https://assets.nflxext.com/ffe/siteui/fonts/netflix-sans/v3/NetflixSans_W_Rg.woff) format('woff');
    }

    @font-face {
        font-family: 'Netflix Sans';
        font-weight: 900;
        font-style: normal;
        src: url(https://assets.nflxext.com/ffe/siteui/fonts/netflix-sans/v3/NetflixSans_W_Bd.woff2) format('woff2'),
             url(https://assets.nflxext.com/ffe/siteui/fonts/netflix-sans/v3/NetflixSans_W_Bd.woff) format('woff');
    }

    
    </style>
""", unsafe_allow_html=True)

# Apply global styling and background
st.markdown(f"""
    <style>
              
    .stApp {{
        background: 
        linear-gradient(to top, rgba(0, 0, 0, 0.5) 0%, rgba(0,0,0,0.3) 40%, rgba(0,0,0,0) 100%),
        radial-gradient(circle at center, rgba(0, 0, 0, 0.6) 0%, rgba(0, 0, 0, 0.2) 70%, rgba(0, 0, 0, 0) 100%),
        linear-gradient(to bottom, rgba(0,0,0,0.5) 0%, rgba(0,0,0,0.85) 90%, rgba(0,0,0,1) 100%),
        url("{background_url}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}


    html, body, [class*="css"] {{
        font-family: 'Netflix Sans', sans-serif !important;
        color: white !important;
    }}

    .big {{
        font-family: 'Netflix Sans' !important;
        font-weight: 900 !important;
        font-size: 65px !important;
        text-align: center !important;
        
        line-height: 1.2 !important;
        text-shadow: 2px 2px 6px rgba(0,0,0,0.75) !important;
    }}

    .small{{
        font-family: 'Netflix Sans' !important;
        font-weight: 570 !important;
        font-size: 25px !important;
        text-align: center !important;
    }}

    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    
    .custom-label {
        font-family: 'Netflix Sans', sans-serif !important;
        font-size: 17px;
        color: white;
        font-weight: 400;
        text-align: center;
        margin-top: 10px;
    }
            
    div[data-baseweb="select"]> div {
        background-color: rgba(80, 80, 80, 0.5) !important;  /* Transparent black */
        border: 1px solid #e50914;
        border-radius: 8px; 
        height: 50px !important;  /* Increase height */
            margin-top: -15px;
    }
    
            
    div[data-baseweb="select"] > div > div {
        color: white !important;
        font-size: 20px !important;
        padding-top: 10px;
    }

    div[data-baseweb="select"]:focus {
        outline: none !important;
        box-shadow: none !important;
    }
    </style>
""", unsafe_allow_html=True)



# Text that uses the custom font and weight
st.markdown('<p class="big">Unlimited movies, TV shows and more</p>', unsafe_allow_html=True)


st.markdown('<p class="small">Your next favorite movie awaits.</p>',unsafe_allow_html=True)


st.markdown('<div class="custom-label">Not sure what to watch next? Select one movie you’ve liked, and we’ll handle the rest.</div>', unsafe_allow_html=True)

#loading the pkl files
movies = pickle.load(open("movies_list.pkl","rb"))
similarity = pickle.load(open("similarity.pkl","rb"))
movie_list = list(movies["title"].astype(str))

#fetching Posters
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=e2632be724f51a5028bce1c93a5ba4cf&language=en-US"
    response = requests.get(url)
    data = response.json()
    fullpath = "https://image.tmdb.org/t/p/w500/"+data["poster_path"]
    return fullpath

#recommend function
def recommend(movie):
    index = movies[movies["title"]==movie].index[0]
    distance = sorted(list(enumerate(similarity[index])),reverse=True,key=lambda vector:vector[1])
    recommend_movie =[]
    recommend_poster = []
    for i in distance[0:5]:
        movie_id = movies.iloc[i[0]].id
        recommend_movie.append(movies.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(movie_id))
    return recommend_movie,recommend_poster

select_value = st.selectbox("", movie_list, index=0)

if st.button("Recommend"):
    movie_name,movie_poster = recommend(select_value)
    col1,col2,col3,col4,col5 = st.columns(5)

    with col1:
        st.image(movie_poster[0],use_container_width=True)
        st.text(movie_name[0])

    with col2:
        st.image(movie_poster[1],use_container_width=True)
        st.text(movie_name[1])
    
    with col3:
        st.image(movie_poster[2],use_container_width=True)
        st.text(movie_name[2])

    with col4:
        st.image(movie_poster[3],use_container_width=True)
        st.text(movie_name[3])

    with col5:
        
        st.image(movie_poster[4],use_container_width=True)
        st.text(movie_name[4])