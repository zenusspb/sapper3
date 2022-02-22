import pygame as pg

'''
отвечает за дизайн окона игры
'''


class Menu_view:
    def update(self, win, menu):
        win.fill((255, 255, 255))
        self.draw_banner(win, menu.name_banner)
        self.draw_button(win, menu.start_button)

        # кнопки выбора сложности
        self.draw_button(win, menu.low_dif_button)
        self.draw_button(win, menu.med_dif_button)
        self.draw_button(win, menu.high_dif_button)

        pg.display.update()

    @staticmethod
    def draw_banner(win, banner):
        win.blit(banner.label, banner.pos)

    @staticmethod
    def draw_button(win, button):
        if button.selected:
            pg.draw.rect(win, button.color[1], button.rect)
        else:
            pg.draw.rect(win, button.color[button.status], button.rect)
        win.blit(button.label, button.label_pos)


class Field_view:
    def update(self, win, win_size, field):
        win.fill((192, 192, 192))

        for line in field.field:
            for cage in line:
                self.draw_cage(win, cage)

        for i in range(field.grid_size):
            pg.draw.line(win, (128, 128, 128),
                         (0, i * field.side_size), (win_size[1] - 3, i * field.side_size), 3)
            pg.draw.line(win, (128, 128, 128),
                         (i * field.side_size, 0), (i * field.side_size, win_size[1]), 3)

    @staticmethod
    def draw_cage(win, cage):
        # разминированные клетки
        if cage.defused:
            if cage.opened and cage.is_mine:
                color = (230, 117, 115)
                pg.draw.rect(win, color, cage.rect)
            else:
                color = cage.close_color
                pg.draw.rect(win, color, cage.rect)
            win.blit(cage.flag, (cage.rect[0], cage.rect[1]))
            return

        # цвет мин и пустых клеток

        color = (192, 192, 192)
        if cage.is_mine and cage.opened:
            color = (230, 117, 115)
        if cage.opened and not cage.is_mine:
            color = (220, 220, 220)

        pg.draw.rect(win, color, cage.rect)

        if cage.opened and not cage.is_mine:
            hint_label = cage.hint_font.render(
                f'{cage.hint}', True, (0, 0, 0))
            win.blit(
                hint_label, (cage.rect[0] + (cage.side_size - hint_label.get_width()) / 2, cage.rect[1] + (cage.side_size - hint_label.get_height()) / 2))


class Panel_view:
    def update(self, win, win_size, panel):
        pg.draw.rect(win, (0, 0, 0), panel.get_rect(win_size))

        banner_pos = panel.banner_pos(win_size)
        self.draw_banner(win, panel.defuse_banner.label, banner_pos)

        if panel.victory_label != None:
            win.blit(panel.victory_label, (win_size[1] + panel.end_banner_pos[0] - panel.victory_label.get_width() / 2,
                                           (win_size[1] - panel.victory_label.get_height()) / 2))

    @staticmethod
    def draw_banner(win, label, pos):
        win.blit(label, pos)
