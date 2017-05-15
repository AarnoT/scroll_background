import pygame as pg

from scroll_background import ScrollBackground

pg.init()

if __name__ == '__main__':
    background = pg.Surface((2000, 2000))
    display = pg.display.set_mode((800, 800))
    display_pos = ((600, 600))

    # Drawing the background grid.
    for x in range(0, 2001, 50):
        for y in range(0, 2001, 50):
            pg.draw.rect(background, (0, 255, 0), (x, y, 50, 50))
    for x in range(0, 2001, 100):
        for y in range(50, 2001, 100):
            pg.draw.rect(background, (0, 0, 255), (x, y, 50, 50))
    for x in range(50, 2001, 100):
        for y in range(0, 2001, 100):
            pg.draw.rect(background, (0, 0, 255), (x, y, 50, 50))

    scroll_bg = ScrollBackground(background, display, display_pos)
    display.blit(
            scroll_bg.background,
            pg.Rect(0, 0, 800, 800),
            pg.Rect(display_pos, display.get_size()))

    player_rect = pg.Rect(950, 950, 100, 100)
    true_x_pos, true_y_pos = player_rect.topleft
    max_scroll = 1900
    x_size, y_size = player_rect.size
    clock = pg.time.Clock()
    running = True

    while running:
        delta_time = clock.tick(60)/1000 * 60
        prev_player_rect = player_rect.copy()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                break
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_z:
                    scroll_bg.zoom = 2.0
                    true_x_pos *= 2.0
                    true_y_pos *= 2.0
                    x_size *= 2.0
                    y_size *= 2.0
                    max_scroll *= 2.0
                    prev_player_rect.x *= 2.0
                    prev_player_rect.y *= 2.0
                    prev_player_rect.width *= 2.0
                    prev_player_rect.height *= 2.0
                    continue
            elif event.type == pg.KEYUP:
                if event.key == pg.K_z:
                    scroll_bg.zoom = 1.0
                    true_x_pos /= 2.0
                    true_y_pos /= 2.0
                    x_size /= 2.0
                    y_size /= 2.0
                    max_scroll /= 2.0
                    prev_player_rect.x /= 2.0
                    prev_player_rect.y /= 2.0
                    prev_player_rect.width /= 2.0
                    prev_player_rect.height /= 2.0
                    continue
        speed = 3
        if pg.key.get_pressed()[pg.K_LEFT]:
            true_x_pos = max(true_x_pos - speed*delta_time, 0)
        elif pg.key.get_pressed()[pg.K_RIGHT]:
            true_x_pos = min(true_x_pos + speed*delta_time, max_scroll)
        if pg.key.get_pressed()[pg.K_UP]:
            true_y_pos = max(true_y_pos - speed*delta_time, 0)
        elif pg.key.get_pressed()[pg.K_DOWN]:
            true_y_pos = min(true_y_pos + speed*delta_time, max_scroll)

        player_rect = pg.Rect(true_x_pos, true_y_pos, x_size, y_size)
        scroll_bg.center((true_x_pos + x_size/2, true_y_pos + y_size/2))
        clear_pos = (
            prev_player_rect.left - scroll_bg.display_pos.x,
            prev_player_rect.top - scroll_bg.display_pos.y)
        draw_rect = (
            player_rect.left - scroll_bg.display_pos.x,
            player_rect.top - scroll_bg.display_pos.y,
            x_size,
            y_size)
        display.blit(
            scroll_bg.background,
            clear_pos,
            prev_player_rect)
        pg.draw.rect(display, (255, 0, 0), draw_rect)
        pg.display.set_caption('FPS: {:.2f}'.format(clock.get_fps()))
        pg.display.update()
