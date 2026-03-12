from round import Round

round = Round({
    "initial_points": 501,
    "bust_threshold": -10,
    "max_score": 1000
})

round.add_player("Alice")
round.add_player("Bob")
round.start_game()