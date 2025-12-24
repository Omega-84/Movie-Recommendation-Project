import streamlit as st
import pandas as pd
import my_functions as myfn
import config

# Page configuration
st.set_page_config(
    page_title=f"{config.APP_TITLE} - Movie Recommendations",
    page_icon=config.APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load data with caching
@st.cache_data
def load_data():
    try:
        return pd.read_csv(config.MOVIE_DATA_PATH, index_col='id')
    except FileNotFoundError:
        st.error("❌ Movie data file not found. Please check the data path.")
        return None

df = load_data()

# Sidebar
with st.sidebar:
    st.image('img.jpeg', width=100)
    st.title(config.APP_TITLE)
    st.markdown("### Made by **Varun Nayyar**")
    
    st.markdown("---")
    st.markdown("Connect with me:")
    st.markdown(
        """
        <div style="display: flex; gap: 10px;">
            <a href="https://www.linkedin.com/in/varun-nayyar-ml/" target="_blank">LinkedIn</a> •
            <a href="https://github.com/Omega-84" target="_blank">GitHub</a> •
            <a href="https://nayyarvarun84.wixsite.com/my-site" target="_blank">Website</a>
        </div>
        """, 
        unsafe_allow_html=True
    )
    st.markdown("---")

# Main Content
if df is not None:
    # Tabs for navigation
    tab1, tab2 = st.tabs(["🔍 Search & Recommend", "🔥 New Arrivals"])
    
    # --- Tab 1: Search & Recommend ---
    with tab1:
        st.title(f"{config.APP_ICON} Movie Recommender")
        st.markdown("### Discover your next favorite film")
        
        # Search Box
        movie_list = myfn.get_all_movies()
        selected_movie = st.selectbox(
            "Select a movie you love:", 
            movie_list,
            format_func=lambda x: x[1],
            placeholder="Type to search..."
        )
        
        if selected_movie:
            idd = selected_movie[0]
            
            # Selected Movie Display
            col1, col2 = st.columns([1, 2])
            
            with col1:
                poster = myfn.get_movie_poster(idd)
                st.image(poster, use_column_width=True)
            
            with col2:
                st.subheader(myfn.get_movie_title(idd))
                # Add more details if available (e.g., genres) later
            
            st.markdown("---")
            st.subheader("You might also like:")
            
            # Recommendations
            with st.spinner("Analyzing movie features..."):
                try:
                    recommendations = myfn.get_recommendations(idd)
                    
                    if not recommendations:
                        st.warning("No recommendations found.")
                    else:
                        # Display as a grid
                        cols = st.columns(len(recommendations))
                        for idx, (rec_text, rec_id) in enumerate(recommendations):
                            with cols[idx]:
                                rec_poster = myfn.get_movie_poster(rec_id)
                                rec_title = rec_text.split('\n')[0].strip() # Extract title
                                
                                st.markdown(
                                    f"""
                                    <div class="movie-card">
                                        <img src="{rec_poster}" style="width:100%; border-radius:8px; margin-bottom:10px;">
                                        <div class="movie-title">{rec_title}</div>
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )
                                # Tooltip/Expandable for details
                                with st.expander("Details"):
                                    st.caption(rec_text.replace(rec_title, "").strip())
                                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")

    # --- Tab 2: New Arrivals ---
    with tab2:
        st.title("🔥 Just Added")
        st.markdown("### Fresh movies added to our database")
        
        new_movies = myfn.get_new_arrivals(limit=18)
        
        # 6 columns grid for new arrivals
        curr_row = st.columns(6)
        
        for i, (mid, title, poster_url) in enumerate(new_movies):
            col_idx = i % 6
            # New row every 6 items
            if i > 0 and col_idx == 0:
                curr_row = st.columns(6)
            
            with curr_row[col_idx]:
                st.image(poster_url, use_column_width=True)
                st.caption(f"**{title}**")

else:
    st.error("Failed to load movie database.")