from fastapi import FastAPI
import movieRecommended  # Import the script containing the recommendation logic

app = FastAPI()

@app.get("/")
def home():
    return {"message": "FastAPI Movie Recommendation API is running!"}

@app.get("/recommend/{movie_name}")
def recommend(movie_name: str):
    # Call the function from movieRecommended.py and return the result
    result = movieRecommended.get_movie_recommendations(movie_name)
    if "error" in result:
        return {"error": result["error"]}
    return {"recommended_movies": result["recommended_movies"]}
