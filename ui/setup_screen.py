import pygame
import pygame_gui
from fields import *
from ui.base_screen import BaseScreen

class SetupScreen(BaseScreen):
    def __init__(self, manager):
        super().__init__(manager)
        self.player_inputs = []
        self.stat_dropdown = None
        self.category_dropdown = None
        self.option_dropdown = None

    def show(self):
        self.player_inputs = []

        self.add(pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((300, 20), (200, 40)),
            text='Movie Darts', manager=self.manager))

        self.add(pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((50, 80), (150, 30)),
            text='Statistic:', manager=self.manager))
        self.stat_dropdown = self.add(pygame_gui.elements.UIDropDownMenu(
            options_list=list(statistics.keys()),
            starting_option=list(statistics.keys())[0],
            relative_rect=pygame.Rect((50, 110), (200, 40)),
            manager=self.manager))

        self.add(pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((300, 80), (150, 30)),
            text='Category:', manager=self.manager))
        self.category_dropdown = self.add(pygame_gui.elements.UIDropDownMenu(
            options_list=list(categories.keys()),
            starting_option=list(categories.keys())[0],
            relative_rect=pygame.Rect((300, 110), (200, 40)),
            manager=self.manager))

        self.add(pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((550, 80), (150, 30)),
            text='Option:', manager=self.manager))
        initial_options = self._get_options(list(categories.keys())[0])
        self.option_dropdown = self.add(pygame_gui.elements.UIDropDownMenu(
            options_list=initial_options,
            starting_option=initial_options[0],
            relative_rect=pygame.Rect((550, 110), (200, 40)),
            manager=self.manager))

        self.add(pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((50, 200), (700, 30)),
            text='Player names (fill in to add players, max 4):', manager=self.manager))

        for i in range(4):
            x = 50 + i * 180
            self.add(pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((x, 240), (160, 25)),
                text=f'Player {i+1}', manager=self.manager))
            entry = self.add(pygame_gui.elements.UITextEntryLine(
                relative_rect=pygame.Rect((x, 265), (160, 40)),
                manager=self.manager))
            self.player_inputs.append(entry)

        self.add(pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((300, 350), (200, 50)),
            text='Start Game', manager=self.manager))

    def hide(self):
        super().hide()
        self.player_inputs.clear()

    def handle_event(self, event):
        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == self.category_dropdown:
                self._refresh_options(event.text)

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element.text == 'Start Game':
                return self._get_config()

        return None

    def _get_options(self, category_key):
        return [o["name"] for o in categories[category_key]["options"]]

    def _refresh_options(self, category_key):
        self.elements.remove(self.option_dropdown)
        self.option_dropdown.kill()
        new_options = self._get_options(category_key)
        self.option_dropdown = self.add(pygame_gui.elements.UIDropDownMenu(
            options_list=new_options,
            starting_option=new_options[0],
            relative_rect=pygame.Rect((550, 110), (200, 40)),
            manager=self.manager))

    def _get_config(self):
        players = [p.get_text().strip() for p in self.player_inputs if p.get_text().strip()]
        if not players:
            return None
        return {
            "players": players,
            "stat": self.stat_dropdown.selected_option,
            "category": self.category_dropdown.selected_option,
            "option": self.option_dropdown.selected_option,
        }