import pygame_gui

class BaseScreen:
    def __init__(self, manager):
        self.manager = manager
        self.elements = []

    def hide(self):
        for e in self.elements:
            e.kill()
        self.elements.clear()

    def add(self, element):
        self.elements.append(element)
        return element

    def handle_event(self, event):
        return None