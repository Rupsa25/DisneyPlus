import streamlit as st
import os
import pandas as pd
from utils.recommender import recommend_movie
from utils.helpers import pre_process
import warnings
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
warnings.filterwarnings('ignore')


st.set_page_config(page_title = "Disney Plus", page_icon = ":movie_camera:", layout = "wide")

# st.header("Disney Data Dashboard")


# movie_name = st.sidebar.text_input("Enter the name of a movie:", "The Shawshank Redemption")


# df = pd.read_csv('disney_plus_titles.csv')
# df = pre_process(df)



#load dataset
# f1 = st.file_uploader(":file_uploader: Upload a file", type = (["csv","txt","xlsx","xls"]))
# if f1 is not None:
#     filename = f1.name
#     st.write(filename)
#     df = pd.read_csv(filename,encoding = "ISO-8859-1")
# else:
file_path = '/Users/rupsachakraborty/Desktop/JOB/Kaggle/DisneyData/disney_plus_titles.csv'
df = pd.read_csv(file_path,encoding = "ISO-8859-1")



selected_type = st.sidebar.selectbox('Select Type:', df['type'].unique())

# Filter the DataFrame based on selected 'type'
filtered_df = df[df['type'] == selected_type]

# Dropdown for selecting 'title'
selected_title = st.sidebar.selectbox('Select Title:', filtered_df['title'])

# Display information based on the selected 'title'
selected_row = filtered_df[filtered_df['title'] == selected_title].iloc[0]


st.image("logo.png", caption="Disney+ Logo", use_column_width=True)


st.subheader('Details:')
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"**Title:** {selected_row['title']}")
    st.markdown(f"**Duration:** {selected_row['duration']}")
    st.markdown(f"**Genre:** {selected_row['listed_in']}")

with col2:
    st.markdown(f"**Rating:** {selected_row['rating']}")
    st.markdown(f"**Release Year:** {selected_row['release_year']}")
    st.markdown(f"**Description:** {selected_row['description']}")



#Recommendation

st.title("Disney Movies Recommendation System")

df = pre_process(df)


# Dropdown for selecting 'title'
movie = st.selectbox('Select Movie:', df['title'])

if st.button("Get Recommendation"):
    recommendation = recommend_movie(df,movie)

    if recommendation:
        st.success("Here's your recommendation:")
        st.write(recommendation)
    else:
        st.warning("Movie not found in the dataset. Please try another one.")

