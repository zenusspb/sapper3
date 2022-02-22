import pygame as pg

import game
import menu
import view


WIN_SIZE = (1280, 960)
WIN = pg.display.set_mode(WIN_SIZE)
pg.display.set_caption("Сапёр")

'''
отвечает за загрузку окна
'''


def check_buttons(buttons, mouse_pos):
    for button in buttons:
        if button.pos[0] - button.size[0] / 2 <= mouse_pos[0] <= button.pos[0] + button.size[0] / 2\
                and button.pos[1] - button.size[1] / 2 <= mouse_pos[1] <= button.pos[1] + button.size[1] / 2:
            return button

    return -1


def launch_menu():
    start_menu = menu.Start_menu(WIN_SIZE)
    menu_view = view.Menu_view()

    mouse_pressed = False
    difficult = -1

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_pressed = True

        buttons = start_menu.buttons()
        active_button = check_buttons(buttons, pg.mouse.get_pos())

        if active_button == -1:
            for button in buttons:
                start_menu.change_status(button, False)
        else:
            start_menu.change_status(active_button, True)

        if buttons[0].status and mouse_pressed and difficult != -1:
            return difficult

        for i, button in enumerate(buttons[1:]):
            if button.status and mouse_pressed:
                start_menu.select(buttons[i + 1])
                difficult = i + 1

        menu_view.update(WIN, start_menu)
        mouse_pressed = False


def launch_game(difficult):
    sapper_game = game.Game(difficult, WIN_SIZE)
    game_view = view.Field_view()
    panel_view = view.Panel_view()
    clock = pg.time.Clock()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

            mouse_pos = pg.mouse.get_pos()
            if mouse_pos[0] < WIN_SIZE[1] and event.type == pg.MOUSEBUTTONDOWN:
                x = int(mouse_pos[0]//sapper_game.side_size)
                y = int(mouse_pos[1]//sapper_game.side_size)

                sapper_game.update(x, y, event.button)

        if sapper_game.result != 0:
            game_view.update(WIN, WIN_SIZE, sapper_game.mine_field)
            sapper_game.panel.update(
                sapper_game.mine_field.defuse_amount, sapper_game.result)
            panel_view.update(WIN, WIN_SIZE, sapper_game.panel)

            pg.display.update()

            while True:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        quit()
                    if event.type == pg.MOUSEBUTTONDOWN:
                        return True

        game_view.update(WIN, WIN_SIZE, sapper_game.mine_field)
        panel_view.update(WIN, WIN_SIZE, sapper_game.panel)

        pg.display.update()


while True:
    if launch_game(launch_menu()):
        continue
