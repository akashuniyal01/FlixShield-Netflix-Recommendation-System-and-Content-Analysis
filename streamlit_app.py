import requests
import streamlit as st
import pandas as pd

st.title("🎬 Movie Recommendation System")

movie = st.text_input("Enter Movie Name")

top_n = st.slider("Recommendations", 5, 20, 10)

if st.button("Recommend"):

    response = requests.post(
        "http://127.0.0.1:8000/recommend",
        json={
            "title": movie,
            "top_n": top_n
        }
    )

    if response.status_code == 200:

        data = response.json()

        df = pd.DataFrame(data["Recommendations"])

        st.dataframe(df, use_container_width=True)

    else:
        st.error(response.json()["detail"])