import pygame
import pygame_gui

from fields import categories, statistics
from classes.player import Player
from configs.configs import MAX_BUST
from ui.setup_screen import SetupScreen
from ui.game_screen import GameScreen
from ui.end_screen import EndScreen

WIDTH, HEIGHT = 800, 550
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Movie Darts")

manager = pygame_gui.UIManager((WIDTH, HEIGHT), 'ui/theme.json')

setup_screen = SetupScreen(manager)
game_screen = GameScreen(manager)
end_screen = EndScreen(manager)

# State
state = "setup"
players = []
active_players = []
current_player_idx = 0
stat_key = ""
cat_option = None

def start_setup():
    global state
    state = "setup"
    setup_screen.show()

def start_game(config):
    global state, players, active_players, current_player_idx, stat_key, cat_option

    players = [Player(name) for name in config["players"]]
    active_players = players.copy()
    current_player_idx = 0

    stat_display = config["stat"]
    # pygame_gui returns tuples like (text, id) for dropdown selections
    if isinstance(stat_display, tuple):
        stat_display = stat_display[0]
    stat_key = statistics[stat_display]

    cat_name = config["category"]
    if isinstance(cat_name, tuple):
        cat_name = cat_name[0]
    option_name = config["option"]
    if isinstance(option_name, tuple):
        option_name = option_name[0]

    category = categories[cat_name]
    options = category["options"]
    option_names = [o["name"] for o in options]
    cat_option = options[option_names.index(option_name)]

    state = "game"
    game_screen.show(players, stat_display, cat_name, option_name)
    game_screen.set_turn(active_players[current_player_idx].name)

def handle_guess():
    global current_player_idx

    guess_text = game_screen.get_guess()
    if not guess_text:
        return

    player = active_players[current_player_idx]
    _, message = player.guess(guess_text, stat_key, cat_option)
    game_screen.set_message(message)
    game_screen.update_scores()
    game_screen.clear_guess()

    advance_turn()

def handle_quit_player():
    global current_player_idx

    player = active_players[current_player_idx]
    active_players.remove(player)
    game_screen.set_message(f"{player.name} has left the game!")

    if not active_players:
        end_no_winner()
        return

    if current_player_idx >= len(active_players):
        current_player_idx = 0
        check_round_end()
    else:
        game_screen.set_turn(active_players[current_player_idx].name)

def advance_turn():
    global current_player_idx

    current_player_idx += 1
    if current_player_idx >= len(active_players):
        current_player_idx = 0
        check_round_end()
    else:
        game_screen.set_turn(active_players[current_player_idx].name)

def check_round_end():
    in_checkout = [p for p in active_players if 0 <= p.score <= MAX_BUST]

    if in_checkout:
        winner_score = min(p.score for p in in_checkout)
        winners = [p for p in in_checkout if p.score == winner_score]
        show_end(winners)
    else:
        game_screen.set_turn(active_players[current_player_idx].name)

def show_end(winners):
    global state
    game_screen.hide()
    state = "end"
    end_screen.show(winners, players)

def end_no_winner():
    global state
    game_screen.hide()
    state = "end"
    end_screen.show([], players)

# Patch EndScreen.show to handle empty winners list gracefully
_original_end_show = EndScreen.show
def _patched_end_show(self, winners, players):
    if not winners:
        self.add(pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((250, 150), (300, 40)),
            text='No players remaining!', manager=self.manager))
        self.add(pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((200, 200), (400, 30)),
            text='Game over — nobody checked out.', manager=self.manager))
        for i, player in enumerate(players):
            self.add(pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((300, 260 + i * 35), (200, 30)),
                text=f'{player.name}: {player.score}', manager=self.manager))
        self.add(pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((300, 450), (200, 50)),
            text='Play Again', manager=self.manager))
    else:
        _original_end_show(self, winners, players)
EndScreen.show = _patched_end_show

# --- Main loop ---
start_setup()
clock = pygame.time.Clock()
running = True

while running:
    dt = clock.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        manager.process_events(event)

        if state == "setup":
            result = setup_screen.handle_event(event)
            if result:
                setup_screen.hide()
                start_game(result)

        elif state == "game":
            result = game_screen.handle_event(event)
            if result == "guess":
                handle_guess()
            elif result == "quit":
                handle_quit_player()

        elif state == "end":
            result = end_screen.handle_event(event)
            if result == "play_again":
                end_screen.hide()
                start_setup()

    manager.update(dt)
    screen.fill((30, 30, 30))
    manager.draw_ui(screen)
    pygame.display.update()

pygame.quit()
