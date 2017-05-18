import pygame as pg

from scroll_background import Vector2, ScrollBackground

pg.init()


def draw_grid(surface):
    for x in range(0, surface.get_width(), 50):
        for y in range(0, surface.get_width(), 50):
            pg.draw.rect(surface, (0, 255, 0), (x, y, 50, 50))
    for x in range(0, surface.get_width(), 100):
        for y in range(50, surface.get_width(), 100):
            pg.draw.rect(surface, (0, 0, 255), (x, y, 50, 50))
    for x in range(50, surface.get_width(), 100):
        for y in range(0, surface.get_width(), 100):
            pg.draw.rect(surface, (0, 0, 255), (x, y, 50, 50))


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
        background = pg.Surface((800, 800))
        display = pg.display.set_mode((900, 900), pg.RESIZABLE)
        draw_grid(background)
        self.scroll_bg = ScrollBackground(background, display, (0, 0))

        self.player = Player(Vector2(background.get_size()))
        self.scroll_bg.move_or_center_display()
        self.scroll_bg.blit(pg.Surface((123, 123)), (300, 300))
        self.scroll_bg.redraw_display()

        self.clock = pg.time.Clock()
        self.running = True

    def main(self):
        while self.running:
            delta_time = self.clock.tick(60)/1000 * 60
            self.handle_input(delta_time)
            self.player.update(delta_time)
            self.scroll_bg.center(self.player.rect.center)
            self.scroll_bg.draw_sprites((self.player,))
            pg.display.set_caption('FPS: {:.2f}'.format(self.clock.get_fps()))
            pg.display.update()

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
                self.scroll_bg.display = (
                    pg.display.set_mode(event.size, pg.RESIZABLE))
                self.scroll_bg.move_or_center_display()
                self.scroll_bg.redraw_display()


    def scale(self, factor):
        self.scroll_bg.zoom *= factor
        self.player.scale(factor)


if __name__ == '__main__':
    Game().main()
