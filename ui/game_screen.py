import pygame
import pygame_gui
from ui.base_screen import BaseScreen

class GameScreen(BaseScreen):
    def __init__(self, manager):
        super().__init__(manager)
        self.guess_input = None
        self.message_box = None
        self.turn_label = None
        self.score_labels = []

    def show(self, players, stat, category, option):
        self.score_labels = []

        self.add(pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((50, 20), (700, 30)),
            text=f'{stat} · {category}: {option}', manager=self.manager))

        for i, player in enumerate(players):
            x = 50 + i * 180
            label = self.add(pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((x, 70), (160, 30)),
                text=f'{player.name}: {player.score}', manager=self.manager))
            self.score_labels.append((player, label))

        self.turn_label = self.add(pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((300, 130), (200, 30)),
            text='', manager=self.manager))

        self.add(pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((300, 180), (200, 30)),
            text='Guess a movie:', manager=self.manager))

        self.guess_input = self.add(pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((300, 210), (200, 40)),
            manager=self.manager))

        self.message_box = self.add(pygame_gui.elements.UITextBox(
            html_text='',
            relative_rect=pygame.Rect((300, 260), (200, 60)),
            manager=self.manager))

        self.add(pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((300, 340), (200, 50)),
            text='Guess', manager=self.manager))

        self.add(pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((300, 400), (200, 50)),
            text='Quit', manager=self.manager))

    def hide(self):
        super().hide()
        self.score_labels.clear()

    def set_turn(self, player_name):
        self.turn_label.set_text(f"{player_name}'s turn")

    def set_message(self, message):
        self.message_box.set_text(message)

    def get_guess(self):
        return self.guess_input.get_text().strip()

    def clear_guess(self):
        self.guess_input.set_text('')

    def update_scores(self):
        for player, label in self.score_labels:
            label.set_text(f'{player.name}: {player.score}')

    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element.text == 'Guess':
                return 'guess'
            elif event.ui_element.text == 'Quit':
                return 'quit'
        return None