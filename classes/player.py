from api.movie import *
from configs.configs import *

class Player:
    def __init__(self, name):
        self.name = name
        self.score = INITIAL_SCORE

    def guess(self, guess, stat, cat_option):
        movie = get_movie(guess)
        if "Error" in movie:
            return False, f"{guess} is not a valid movie!"

        movie_title = movie.get("Title", guess)
        category = cat_option["category"]

        if not category["function"](movie, cat_option["name"]):
            return False, f"{movie_title} does not match! {category['attribute']} does not contain {cat_option['name']}"

        value = int(get_stat_value(movie, stat))
        remaining = self.score - value

        if value == 0:
            return False, f"{movie_title} is a bust! No data."
        elif value > MAX_PER_VISIT:
            return False, f"{movie_title} is a bust! Too high — {value}"
        elif remaining < 0:
            return False, f"{movie_title} is a bust! Would go below zero."
        elif 0 <= remaining <= MAX_BUST:
            self.score = remaining
            return True, f"{movie_title} — Checkout! Score: {self.score}"
        else:
            self.score = remaining
            return False, f"{movie_title} scores! {value} — Remaining: {self.score}"