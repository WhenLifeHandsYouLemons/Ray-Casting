import pygame

window_height = 645
window_width = 1250
WIN = pygame.display.set_mode((window_width, window_height))

class Boundary:
    def __init__(self, x1, y1, x2, y2, hidden=False):
        self.start = pygame.Vector2(x1, y1)
        self.end = pygame.Vector2(x2, y2)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.hidden = hidden
        self.show_colour = (255, 255, 255)
        self.hide_colour = (0, 0, 0)
        self.width = 3

    def draw(self):
        if self.hidden:
            pygame.draw.line(WIN, self.hide_colour, self.start, self.end, self.width)
        else:
            pygame.draw.line(WIN, self.show_colour, self.start, self.end, self.width)
