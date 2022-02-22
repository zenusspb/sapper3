import pygame as pg
from visual_components import Button, Banner

'''
кнопки на начальном экране и их внешний вид
'''


class Start_menu:
    def __init__(self, win_size):
        banner_pos = (win_size[0] / 2, win_size[1] / 14)
        banner_color = (0, 0, 0)
        banner_text = "Сапёр"

        # кнопка старта
        button_pos = (win_size[0] / 2, win_size[1] / 2)
        button_size = (250, 100)
        button_text = "Начать"
        button_color = ((180, 180, 180), (220, 220, 220))

        # кнопки выбора сложности
        dif_size = (200, 100)
        low_dif_color = ((180, 180, 180), (220, 220, 220))
        med_dif_color = ((180, 180, 180), (220, 220, 220))
        high_dif_color = ((180, 180, 180), (220, 220, 220))
        gap = win_size[0]/100

        low_dif_pos = (win_size[0] / 2 - dif_size[0] - gap, win_size[1] * 11 / 14)
        med_dif_pos = (win_size[0] / 2,  win_size[1] * 11 / 14)
        high_dif_pos = (win_size[0] / 2 + dif_size[0] + gap, win_size[1] * 11 / 14)

        self.name_banner = Banner(banner_pos, banner_text, banner_color, 100)

        self.start_button = Button(button_pos, button_size,
                                   button_text, button_color)

        self.low_dif_button = Button(
            low_dif_pos, dif_size, "Легко", low_dif_color)
        self.med_dif_button = Button(
            med_dif_pos, dif_size, "Средне", med_dif_color)
        self.high_dif_button = Button(
            high_dif_pos, dif_size, "Сложно", high_dif_color)

    def change_status(self, button, status):
        button.status = status

    def select(self, cur_button):
        for button in self.buttons():
            button.selected = False
        cur_button.selected = True

    def buttons(self):
        return (self.start_button, self.low_dif_button,
                self.med_dif_button, self.high_dif_button)
