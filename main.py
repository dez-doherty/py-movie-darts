from fields import *
from configs.configs import *
from classes.game import *

num_players = int(input("Number of players: "))
players = [Player(input(f"Player {i+1} name: ")) for i in range(num_players)]

print("\nAvailable configs:")
for i, c in enumerate(configs):
    print(f"{i+1}. {c['stat']} — {c['category']}: {c['option']}")

config_index = int(input("Choose config: ")) - 1
config = configs[config_index]

category = categories[config["category"]]
options = category["options"]
option_names = [o["name"] for o in options]
cat_option = options[option_names.index(config["option"])]

game = Game(players, config["stat"], cat_option)
game.run()