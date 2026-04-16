import pygame
import pygame_gui
from ui.base_screen import BaseScreen

class EndScreen(BaseScreen):
    def __init__(self, manager):
        super().__init__(manager)

    def show(self, winners, players):
        if len(winners) == 1:
            title = f'{winners[0].name} wins!'
            subtitle = f'Checked out with a score of {winners[0].score}'
        else:
            names = ', '.join(w.name for w in winners)
            title = f'Tie — {names}!'
            subtitle = f'Both checked out with a score of {winners[0].score}'

        self.add(pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((300, 150), (200, 40)),
            text=title, manager=self.manager))
        self.add(pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((200, 200), (400, 30)),
            text=subtitle, manager=self.manager))

        for i, player in enumerate(players):
            self.add(pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((300, 260 + i * 35), (200, 30)),
                text=f'{player.name}: {player.score}', manager=self.manager))

        self.add(pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((300, 450), (200, 50)),
            text='Play Again', manager=self.manager))

    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element.text == 'Play Again':
                return 'play_again'
        return None