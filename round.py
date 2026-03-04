from player import Player, GuessResult, BUST_POINTS

class Round:
    def __init__(self, initial_points):
        self.players = {}
        self.current_player = None
        self.initial_points = initial_points
        self.rounds = 0
        self.winner = {"player": None, "points": BUST_POINTS}

    def add_player(self, name):
        self.players[name] = Player(name, self)

    def set_turn(self, player):
        self.current_player = player
        player.turns += 1

        answer = input(f"{player.name}'s turn. Enter your answer: ")
        score, status = self.current_player.guess(answer)

        print(f"{self.name}: '{answer}' = {score};", end = " ")

        if status == GuessResult.FINISH:
            print("checked out")

            if player.points > self.winner["points"]:
                if player.points == 0:
                    self.declare_winner(player)
                else:
                    self.winner = {"player": player, "points": player.points}
                    print(f"between 0 and {player.points + 1} points needed to win")

        elif status == GuessResult.VALID:
            print(f"{self.points} remaining")
        elif status == GuessResult.BUST:
            print(f"remains at {self.points}")
            
    def start(self):
        while True:
            self.rounds += 1
            for name, player in self.players.items():
                self.set_turn(player)
            self.end_round()
        
    def end_round(self):
        winner = self.winner["player"]
        if winner:
            self.declare_winner(winner)
            print(f"{winner.name} won the game with {winner.points} points")


    def declare_winner(self, player):
        print(f"Game over! {player.name} wins!")

    def get_player(self, name):
        return self.players[name]