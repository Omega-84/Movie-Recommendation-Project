import streamlit as st
import pandas as pd
import my_functions as myfn
import config

# Page configuration
st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="centered"
)

# Load data
@st.cache_data
def load_data():
    """Load movie data with caching for performance."""
    try:
        return pd.read_csv(config.MOVIE_DATA_PATH, index_col='id')
    except FileNotFoundError:
        st.error("❌ Movie data file not found. Please check the data path.")
        return None

df = load_data()

# Sidebar - Author info
info = st.sidebar.container()
info.title("Made by:")
info.text("")

try:
    info.image('img.jpeg', width=125)
except Exception:
    info.text("📷 Profile image unavailable")

info.subheader("**Varun Nayyar**")
info.text("Let's Chat")
info.write("[LinkedIn](https://www.linkedin.com/in/varun-nayyar-ml/)")
info.write("[GitHub](https://github.com/Omega-84)")
info.write("[My Site](https://nayyarvarun84.wixsite.com/my-site)")

# Main content
st.title('🎬 MOVIE RECOMMENDATION SYSTEM')

if df is not None:
    st.header("Select a movie for which you want recommendations")
    
    # Get movie list safely
    movie_list = myfn.get_all_movies()
    
    if not movie_list:
        st.error("❌ No movies found in the database.")
    else:
        option = st.selectbox("Search the name:", movie_list)
        idd = option[0]
        
        # Display selected movie
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("")
        
        with col2:
            poster_url = myfn.get_movie_poster(idd)
            try:
                st.image(poster_url, width=250)
            except Exception:
                st.image(config.DEFAULT_POSTER_URL, width=250)
            st.caption(myfn.get_movie_title(idd))
        
        with col3:
            st.write("")
        
        # Get and display recommendations
        st.subheader(f"If you watched __*{myfn.get_movie_title(idd)}*__, you may like:")
        
        with st.spinner("Finding similar movies..."):
            try:
                recommendations = myfn.get_recommendations(idd)
                
                if not recommendations:
                    st.warning("No recommendations found for this movie.")
                else:
                    for i, (rec_text, rec_id) in enumerate(recommendations):
                        st.text(rec_text)
                        
                        poster_url = myfn.get_movie_poster(rec_id)
                        try:
                            st.image(poster_url, width=150)
                        except Exception:
                            st.image(config.DEFAULT_POSTER_URL, width=150)
                        
                        st.markdown(
                            """<hr style="height:10px;border:none;color:#333;background-color:#333;" />""",
                            unsafe_allow_html=True
                        )
            except Exception as e:
                st.error(f"❌ Error generating recommendations: {str(e)}")
else:
    st.error("❌ Unable to load movie data. Please check your configuration.")