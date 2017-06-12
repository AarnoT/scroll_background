from collections import deque
import sys

import pygame as pg
#sys.path.insert(0, 'src')
from scroll_background import Vector2, MultiSurfaceBackground

pg.init()


def fps_counter():
    fps = deque(maxlen=100)
    counter = 0
    while True:
        new_fps = yield
        fps.append(new_fps)
        counter = (counter + 1) % 100
        if counter == 0:
            pg.display.set_caption('FPS: {:.2f}'.format(sum(fps) / len(fps)))


class Player:
    def __init__(self, background_size):
        start_pos = (background_size.x//2 - 50, background_size.y//2 - 50)
        self.rect = pg.Rect(start_pos, (100, 100))
        self.image = pg.Surface(self.rect.size)
        self.image.fill((255, 0, 0))
        self.true_pos = Vector2(self.rect.topleft)
        self.max_scroll = background_size - Vector2(self.rect.size)
        self.speed = 5

    def scale(self, factor):
        self.speed *= factor
        self.max_scroll.scale(factor)
        self.true_pos.scale(factor)
        self.rect.topleft = tuple(self.true_pos)
        self.rect.width *= factor
        self.rect.height *= factor
        self.image = pg.Surface(self.rect.size)
        self.image.fill((255, 0, 0))

    def update(self, delta_time):
        if pg.key.get_pressed()[pg.K_LEFT]:
            self.true_pos.x = max(self.true_pos.x - self.speed*delta_time, 0)
        elif pg.key.get_pressed()[pg.K_RIGHT]:
            self.true_pos.x = min(
                self.true_pos.x + self.speed*delta_time, self.max_scroll.x)
        if pg.key.get_pressed()[pg.K_UP]:
            self.true_pos.y = max(self.true_pos.y - self.speed*delta_time, 0)
        elif pg.key.get_pressed()[pg.K_DOWN]:
            self.true_pos.y = min(
                self.true_pos.y + self.speed*delta_time, self.max_scroll.y)
        self.rect = pg.Rect(*self.true_pos, *self.rect.size)


class Game():
    def __init__(self):
        background1 = pg.Surface((1200, 1200))
        background2 = pg.Surface((1200, 1200))
        background3 = pg.Surface((1200, 1200))
        background4 = pg.Surface((1200, 1200))
        display = pg.display.set_mode((900, 900), pg.RESIZABLE)
        background1.fill((150, 0, 0))
        background2.fill((0, 150, 0))
        background3.fill((0, 0, 150))
        background4.fill((100, 0, 100))
        background_list = [[background1, background2],
                           [background3, background4]]
        self.background = MultiSurfaceBackground(
            background_list, display, (0, 0))

        self.player = Player(Vector2(self.background.scrolling_area.size))
        # Display needs to be centered correctly.
        self.background.move_or_center_display()
        self.background.blit(pg.Surface((123, 123)), (300, 300))
        self.background.redraw_display()

        self.clock = pg.time.Clock()
        self.running = True

    def main(self):
        counter = fps_counter()
        next(counter)
        draw_rects = []
        while self.running:
            delta_time = self.clock.tick(60)/1000 * 60
            self.handle_input(delta_time)
            self.player.update(delta_time)
            prev_display_pos = self.background.display_pos
            player_size = Vector2(self.player.rect.size)
            player_size.scale(0.5)
            self.background.center(Vector2(self.player.true_pos) + player_size)
            sprite_rects = self.background.draw_sprites((self.player,))
            if self.background.display_pos != prev_display_pos:
                draw_rects.append(((0, 0), self.background.display.get_size()))
            else:
                draw_rects.extend(sprite_rects)
            counter.send(self.clock.get_fps())
            pg.display.update(draw_rects)
            draw_rects.clear()

    def handle_input(self, delta_time):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                break
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_z:
                    self.scale(2)
                    continue
            elif event.type == pg.KEYUP:
                if event.key == pg.K_z:
                    self.scale(1 / 2)
                    continue
            elif event.type == pg.VIDEORESIZE:
                self.background.display = (
                    pg.display.set_mode(event.size, pg.RESIZABLE))
                self.background.move_or_center_display()
                self.background.redraw_display()

    def scale(self, factor):
        self.background.zoom *= factor
        pg.display.update()
        self.player.scale(factor)


if __name__ == '__main__':
    Game().main()
