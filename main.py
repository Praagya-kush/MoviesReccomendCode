from fastapi import FastAPI
import movieRecommended  # Import the script

app = FastAPI()

@app.get("/")
def home():
    return {"message": "FastAPI Movie Recommendation API is running!"}

@app.get("/recommend/{movie_name}")
def recommend(movie_name: str):
    return movieRecommended.get_movie_recommendations(movie_name)
