from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import pandas as pd

app = FastAPI(
    title="Movie Recommendation API",
    description="Content-Based Movie Recommendation System using TF-IDF and Cosine Similarity",
    version="1.0"
)

# -------------------------------
# Load Pickle Files
# -------------------------------

with open("movies_df.pkl", "rb") as f:
    df_new = pickle.load(f)

with open("cosine_similarity.pkl", "rb") as f:
    cosine_sim = pickle.load(f)

programme_list = df_new["title"].tolist()

# -------------------------------
# Input Schema
# -------------------------------

class MovieRequest(BaseModel):
    title: str
    top_n: int = 10

# -------------------------------
# Home Route
# -------------------------------

@app.get("/")
def home():
    return {
        "message": "Movie Recommendation API is Running"
    }

# -------------------------------
# Recommendation Route
# -------------------------------

@app.post("/recommend")
def recommend_movie(request: MovieRequest):

    title = request.title
    top_n = request.top_n

    if title not in programme_list:
        raise HTTPException(status_code=404,
                            detail="Movie not found")

    index = programme_list.index(title)

    similarity_scores = list(enumerate(cosine_sim[index]))

    similarity_scores = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )[1:top_n+1]

    recommend_index = [i[0] for i in similarity_scores]

    recommendations = []

    for idx, score in similarity_scores:

        recommendations.append({
            "Title": df_new.iloc[idx]["title"],
            "Rating": df_new.iloc[idx]["rating"],
            "Country": df_new.iloc[idx]["country"],
            "Genre": df_new.iloc[idx]["listed_in"],
            "Similarity Score": round(score,4)
        })

    return {
        "Movie": title,
        "Recommendations": recommendations
    }