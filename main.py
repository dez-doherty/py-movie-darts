from darts import Darts

darts_game = Darts({
    "initial_points": 501,
    "bust_threshold": -10,
    "max_score": 1000,
})

darts_game.add_player("Alice")
darts_game.add_player("Bob")
darts_game.start_game()