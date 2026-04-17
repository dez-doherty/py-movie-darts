import os
import requests
from dotenv import load_dotenv

<<<<<<< Updated upstream
API_KEY = ""
=======
load_dotenv()

API_KEY = os.getenv("OMDB_API_KEY")
>>>>>>> Stashed changes

def get_movie(title):
    response = requests.get(f"http://www.omdbapi.com/?t={title}&apikey={API_KEY}")
    return response.json()

def get_stat_value(movie, stat):
    value = movie.get(stat, "")
    value = value.replace(" min", "").replace("$", "").replace(",", "")
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0








