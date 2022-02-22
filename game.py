import pygame as pg
import os
import random
from visual_components import Button, Banner
from fill import fill
pg.font.init()


'''
частичный дизайн в окне игры
'''

'''
создание мин
'''

'''
логика победы и поражения
'''


class Cage:
    hint_font = pg.font.SysFont("Georgia", 25)

    close_color = (167, 167, 167)
    open_color = (128, 128, 128)
    mine_color = (255, 50, 50)

    def __init__(self, pos, side_size):
        self.pos = pos
        self.side_size = side_size

        self.flag = pg.transform.scale(pg.image.load(os.path.join(
            "images", "Flags.png")), (self.side_size, self.side_size))

        self.is_mine = False
        self.hint = 0
        self.opened = False
        self.defused = False
        self.rect = (self.side_size * self.pos[0],
                     self.side_size * self.pos[1], self.side_size, self.side_size)
        self.color = self.close_color

    def update(self, open, defuse):
        self.opened = open
        self.defused = defuse

        if open and not self.is_mine:
            self.color = self.mine_color

        elif open:
            self.color = self.open_color


class Mine_field:
    def __init__(self, mines_amount, grid_size, side_size):
        self.field = []
        self.defuse_amount = 0
        self.mines_amount = mines_amount
        self.grid_size = grid_size
        self.side_size = side_size

        # сетка
        for i in range(grid_size):
            self.field.append([])
            for j in range(grid_size):
                self.field[i].append(Cage((i, j), self.side_size))

        # мины
        for _ in range(mines_amount):
            while True:
                x = random.randint(0, grid_size - 1)
                y = random.randint(0, grid_size - 1)
                if self.field[x][y].is_mine == False:
                    self.field[x][y].is_mine = True
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if 0 <= x + i < grid_size and 0 <= y + j < grid_size and (i != 0 or j != 0):
                                self.field[x + i][y + j].hint += 1
                    break
                else:
                    continue

        while True:
            x = random.randint(0, grid_size - 1)
            y = random.randint(0, grid_size - 1)

            if self.field[x][y].hint == 0 and not self.field[x][y].is_mine:
                fill(self, self.field[x][y])
                break

    def update(self, x, y, button):
        if button == 1:
            if not self.field[x][y].opened and not self.field[x][y].defused and self.field[x][y].hint == 0:
                fill(self, self.field[x][y])

            elif not self.field[x][y].defused:
                self.field[x][y].update(True, False)

        elif button == 3:
            if not self.field[x][y].defused:
                self.defuse_amount += 1

                if self.defuse_amount <= self.mines_amount and not self.field[x][y].opened:
                    self.field[x][y].update(False, True)
                else:
                    # сколько обезвреживаниев доступно
                    self.defuse_amount -= 1


            elif self.field[x][y].defused:
                self.defuse_amount -= 1
                self.field[x][y].update(False, False)


class Panel:
    def __init__(self, panel_size, defuse_amount):
        self.panel_size = panel_size
        self.total_def_amount = defuse_amount

        self.end_banner_pos = (panel_size[0] / 2, panel_size[1] / 2)
        banner_pos = (panel_size[0] / 2, panel_size[1] / 5)

        self.text_size = 20
        self.defuse_banner = Banner(banner_pos, f"Флагов осталось: {defuse_amount}",
                                    (0, 0, 0), self.text_size)

        self.victory_label = None

    def update(self, defuse_amount, result):
        if result == 1:
            self.victory_label = pg.font.SysFont(
                "Impact", 25).render("Вы выиграли!", True, (75, 198, 76))
        elif result == -1:
            self.victory_label = pg.font.SysFont(
                "Impact", 25).render("Поражение!", True, (200, 50, 50))

        self.defuse_banner.update(
            f"Флагов осталось: {self.total_def_amount - defuse_amount}")

    def get_rect(self, win_size):
        return (win_size[0], 0, self.panel_size[0], self.panel_size[1])

    def banner_pos(self, win_size):
        return win_size[1] + self.defuse_banner.pos[0], self.defuse_banner.pos[1]


class Game:
    def __init__(self, difficult, win_size):
        mines_amount = difficult * 5

        if difficult == 1:
            self.grid_size = 7
        else:
            self.grid_size = 10
        self.side_size = int(win_size[1] / self.grid_size)

        self.mine_field = Mine_field(
            mines_amount, self.grid_size, self.side_size)
        panel_size = (win_size[0] - win_size[1], win_size[1])
        self.panel = Panel(panel_size, mines_amount)

        self.result = 0

    def update(self, x, y, button):
        self.mine_field.update(x, y, button)
        self.panel.update(self.mine_field.defuse_amount, self.result)

        if button == 1:
            self.defeat_check(x, y)
        elif button == 3:
            self.victory_check()

    def defeat_check(self, x, y):
        if self.mine_field.field[x][y].is_mine and not self.mine_field.field[x][y].defused:
            self.result = -1

            for line in self.mine_field.field:
                for cage in line:
                    cage.opened = True

    def victory_check(self):
        for line in self.mine_field.field:
            for cage in line:
                if cage.is_mine and not cage.defused:
                    return

        self.result = 1

        for line in self.mine_field.field:
            for cage in line:
                cage.opened = True
