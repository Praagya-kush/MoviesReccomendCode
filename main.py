import os
import uvicorn
from fastapi import FastAPI
import movieRecommended  # Ensure this file exists

app = FastAPI()

@app.get("/")
def home():
    return {"message": "FastAPI Movie Recommendation API is running!"}

@app.get("/recommend/{movie_name}")
def recommend(movie_name: str):
    result = movieRecommended.get_movie_recommendations(movie_name)
    return {"recommended_movies": result["recommended_movies"]}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  # Ensure Railway sets the port dynamically
    print(f"Starting server on port {port}")  # Debugging
    uvicorn.run(app, host="0.0.0.0", port=port)
