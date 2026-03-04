from enum import Enum

BUST_POINTS = -10
MAX_SCORE = 180

class GuessResult(Enum):
    VALID = 1
    FINISH = 2
    BUST = 3

class Player:
    def __init__(self, name, round):
        self.name = name
        self.round = round
        self.points = round.initial_points
        self.turns = 0
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
        
        if score > MAX_SCORE or new_points < BUST_POINTS:
            return 0, GuessResult.BUST
        elif new_points <= 0:
            return score, GuessResult.FINISH
        else:            
            return score, GuessResult.VALID
        
    def is_playing(self):
        return self == self.round.current_player