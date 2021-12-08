import streamlit as st
import pandas as pd
import my_functions as myfn

df = pd.read_csv("movie_data.csv",index_col='id')

info = st.sidebar.container()
info.title("Made by:")
info.text("")
info.image('img.jpeg',width=125)
info.subheader("**Varun Nayyar**")
info.text("Let's Chat")
info.write("[LinkedIn](https://www.linkedin.com/in/varun-nayyar-ml/)")
info.write("[GitHub](https://github.com/Omega-84)")
info.write("[My Site](https://nayyarvarun84.wixsite.com/my-site)")

st.title('MOVIE RECOMMENDATION SYSTEM')

st.header("Select a movie for which you want recommendations")

movie_list = []
for i in df.index:
    movie_list.append((i,df['title'][i]))

option = st.selectbox("Search the name : ",movie_list)

idd = option[0]

col1, col2, col3 = st.columns(3)

with col1:
    st.write("")

with col2:
    st.image(df['posters'][idd],width=250)
    st.caption(df['title'][idd])

with col3:
    st.write("")

st.subheader(f"If you watched __*{df['title'][idd]}*__, you may like : \n")

listt = myfn.get_recommendations(idd)

for i in range(len(listt)):
    st.text(listt[i][0])
    st.image(df['posters'][listt[i][1]],width=150)   
    st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
        