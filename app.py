import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(page_title="IMDb 2024 Analytics")
st.title("🎬 IMDb 2024 Movie Explorer")

# Connect to the Database created by the scraper
try:
    conn = sqlite3.connect("imdb_2024.db")
    df = pd.read_sql("SELECT * FROM movies_2024", conn)
    conn.close()

    # Sidebar Filter
    rating_flt = st.sidebar.slider("Minimum Rating", 0.0, 10.0, 5.0)
    filtered_df = df[df['Rating'] >= rating_flt]

    # Metrics
    st.metric("Total Movies", len(filtered_df))

    # Chart
    st.subheader("Top Movies by Rating")
    fig = px.bar(filtered_df.nlargest(10, 'Rating'), x='Rating', y='Title', orientation='h', color='Rating')
    st.plotly_chart(fig)

    # Table
    st.write("### Movie Data", filtered_df)
except:
    st.error("Please run the scraper.py script first to generate the database!")