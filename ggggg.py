# main.py
import pygame
import pygame_gui
from fields import *
from configs import *
from classes.player import Player
from classes.game import Game
from ui.setup_screen import SetupScreen
from ui.game_screen import GameScreen
from ui.end_screen import EndScreen

pygame.init()

SCREEN_W, SCREEN_H = 800, 600
window_surface = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption('Movie Darts')

manager = pygame_gui.UIManager((SCREEN_W, SCREEN_H), 'ui/theme.json')

setup_screen = SetupScreen(manager)
game_screen = GameScreen(manager)
end_screen = EndScreen(manager)

game = None
active_players = []
current_player_index = 0

SETUP, GAME, END = 'setup', 'game', 'end'
state = SETUP
setup_screen.show()

clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if state == SETUP:
            result = setup_screen.handle_event(event)
            if result:
                players = [Player(name) for name in result["players"]]
                active_players = players.copy()
                current_player_index = 0

                category = categories[result["category"]]
                options = category["options"]
                option_names = [o["name"] for o in options]
                cat_option = options[option_names.index(result["option"])]
                stat = statistics[result["stat"]]

                game = Game(players, stat, cat_option)

                setup_screen.hide()
                state = GAME
                game_screen.show(players, result["stat"], result["category"], result["option"])
                game_screen.set_turn(active_players[current_player_index].name)

        elif state == GAME:
            result = game_screen.handle_event(event)
            if result == 'guess':
                guess = game_screen.get_guess()
                if guess:
                    player = active_players[current_player_index]
                    checkout, message = player.guess(guess, game.stat, game.cat_option)
                    game_screen.set_message(message)
                    game_screen.clear_guess()
                    game_screen.update_scores()

                    current_player_index = (current_player_index + 1) % len(active_players)

                    if current_player_index == 0:
                        in_checkout = [p for p in active_players if 0 <= p.score <= MAX_BUST]
                        if in_checkout:
                            winner_score = min(p.score for p in in_checkout)
                            winners = [p for p in in_checkout if p.score == winner_score]
                            game_screen.hide()
                            state = END
                            end_screen.show(winners, players)

                    if state == GAME:
                        game_screen.set_turn(active_players[current_player_index].name)

            elif result == 'quit':
                player = active_players[current_player_index]
                active_players.remove(player)
                if not active_players:
                    game_screen.hide()
                    state = SETUP
                    setup_screen.show()
                else:
                    current_player_index = current_player_index % len(active_players)
                    game_screen.set_turn(active_players[current_player_index].name)

        elif state == END:
            result = end_screen.handle_event(event)
            if result == 'play_again':
                end_screen.hide()
                state = SETUP
                setup_screen.show()

        manager.process_events(event)

    manager.update(time_delta)
    window_surface.fill((30, 30, 30))
    manager.draw_ui(window_surface)
    pygame.display.update()