import pygame as pg

'''
внешний вид начального экрана
'''


class Button:
    def __init__(self, pos, size, text, color):
        self.pos = pos
        self.size = size
        self.font = pg.font.SysFont("Georgia", 50)
        self.label = self.font.render(text, True, (0, 0, 0))
        self.color = color
        self.status = False
        self.selected = False

        self.rect = (pos[0] - self.size[0]/2, pos[1] - self.size[1]/2,
                     self.size[0], self.size[1])

        self.label_pos = (pos[0] - self.label.get_width()/2,
                          pos[1] - self.label.get_height()/2)


class Banner:
    def __init__(self, pos, text, color, size):
        self.color = color
        self.font = pg.font.SysFont("Georgia", size)
        self.label = self.font.render(text, True, color)

        self.pos = (pos[0] - self.label.get_width() / 2,
                    pos[1] + self.label.get_height() / 2)

    def update(self, text):
        self.label = self.font.render(
            text, True, self.color)
