from enum import Enum

class GuessResult(Enum):
    SCORE = 1
    CHECK_OUT = 2
    BUST = 3
    ILLEGAL = 4

class Player:
    def __init__(self, name, round):
        self.name = name
        self.round = round
        self.points = round.config["initial_points"]
        self.visits = 0
        self.history = []

    def guess(self, answer):
        value = int(answer)
        new_score, status = self.validate_score(value)
        self.points -= new_score

        guess = { 
            "answer": answer, 
            "status": status,
            "score": new_score,
            "points": self.points
        }

        self.history.append(guess)
        return new_score, status

    def validate_score(self, score):
        new_points = self.points - score
        config = self.round.config

        if score > config["max_score"]:
            return 0, GuessResult.ILLEGAL
        elif new_points < config["bust_threshold"]:
            return 0, GuessResult.BUST
        elif new_points <= 0:
            return score, GuessResult.CHECK_OUT
        else:            
            return score, GuessResult.SCORE
        
    def is_playing(self):
        return self == self.round.current_visitor