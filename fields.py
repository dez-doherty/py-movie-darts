def create_category(attribute, options, function):
    category = {
        "attribute": attribute,
        "function": function
    }
    category["options"] = [{"name": o, "category": category} for o in options]
    return category

statistics = {
    "Box Office": "BoxOffice",
    "Metascore": "Metascore",
    "IMDb Rating": "imdbRating",
    "Runtime": "Runtime",
    "Awards": "Awards"
}

categories = {
    "Genre":    create_category("Genre",    ["Action", "Sci-Fi", "Drama", "Horror", "Comedy"],
                    lambda movie, option: option in movie.get("Genre", "")),
    "Director": create_category("Director", ["Christopher Nolan", "Steven Spielberg", "Quentin Tarantino", "Martin Scorsese", "James Cameron"],
                    lambda movie, option: option in movie.get("Director", "")),
    "Writer":   create_category("Writer",   ["Christopher Nolan", "Steven Spielberg", "Quentin Tarantino", "Martin Scorsese", "James Cameron"],
                    lambda movie, option: option in movie.get("Writer", "")),
    "Actors":   create_category("Actors",   ["Leonardo DiCaprio", "Tom Hanks", "Meryl Streep", "Robert De Niro", "Morgan Freeman"],
                    lambda movie, option: option in movie.get("Actors", "")),
}