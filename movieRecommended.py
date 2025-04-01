import numpy as np
import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
movies_data = pd.read_csv('movies.csv')

# Check if 'index' column exists; if not, create it
if 'index' not in movies_data.columns:
    movies_data.reset_index(inplace=True)

# Select relevant features
selected_features = ['genres', 'keywords', 'tagline', 'cast', 'director']

# Fill missing values with an empty string
for feature in selected_features:
    movies_data[feature] = movies_data[feature].fillna('')

# Combine selected features into a single string
combined_features = movies_data['genres'] + ' ' + movies_data['keywords'] + ' ' + movies_data['tagline'] + ' ' + movies_data['cast'] + ' ' + movies_data['director']

# Convert text data into feature vectors
vectorizer = TfidfVectorizer()
feature_vectors = vectorizer.fit_transform(combined_features)

# Compute similarity scores
similarity = cosine_similarity(feature_vectors)

# Function to get movie recommendations
def get_movie_recommendations(movie_name: str):
    movie_name = movie_name.strip()

    list_of_all_titles = movies_data['title'].tolist()

    # Find close matches (with a cutoff for flexibility in partial matching)
    find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles, n=1, cutoff=0.6)

    # If no close matches are found, display a message
    if not find_close_match:
        return {"error": "No recommendations. Movie not found in the list."}
    else:
        close_match = find_close_match[0]

        # Check if the found close match is sufficiently similar to the input movie name
        if movie_name.lower() not in close_match.lower():  # Case-insensitive partial match
            return {"error": "No recommendations. Movie not found in the list."}
        else:
            # Get the index of the movie
            index_of_the_movie = movies_data[movies_data.title == close_match]['index'].values[0]

            # Get similarity scores for all movies
            similarity_score = list(enumerate(similarity[index_of_the_movie]))

            # Sort movies based on similarity score
            sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)

            recommended_movies = []

            for movie in sorted_similar_movies[:10]:  # Get top 10 recommendations
                index = movie[0]
                title_from_index = movies_data.loc[movies_data.index == index, 'title'].values

                if len(title_from_index) > 0:
                    recommended_movies.append(title_from_index[0])

            return {"recommended_movies": recommended_movies}

# Main function to interact with the user and get recommendations
def main():
    movie_name = input('Enter your favourite movie name: ')

    result = get_movie_recommendations(movie_name)

    if 'error' in result:
        print(result['error'])
    else:
        print('Movies suggested for you:\n')
        for i, movie in enumerate(result['recommended_movies'], 1):
            print(f"{i}. {movie}")

if __name__ == "__main__":
    main()
