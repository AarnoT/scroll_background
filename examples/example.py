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


class Game():

    def __init__(self):
        self.background = pg.Surface((800, 800))
        self.display = pg.display.set_mode((600, 600))
        draw_grid(self.background)
        background_width, background_height = self.background.get_size()
        start_pos = (background_width//2 - 50, background_height//2 - 50)
        self.player_rect = pg.Rect(start_pos, (100, 100))
        self.scroll_bg = ScrollBackground(self.background, self.display, (0, 0))
        centered_pos = self.scroll_bg.centered_pos(self.player_rect.center)
        self.scroll_bg.display_pos = centered_pos
        self.scroll_bg.blit(pg.Surface((123, 123)), (300, 300))
        self.scroll_bg.redraw_display()

        self.speed = 5
        self.true_pos = Vector2(*self.player_rect.topleft)
        self.max_scroll = self.background.get_width() - self.player_rect.width
        self.clock = pg.time.Clock()
        self.running = True

    def main(self):
        while self.running:
            delta_time = self.clock.tick(60)/1000 * 60
            prev_player_rect = self.player_rect.copy()
            self.handle_input(delta_time)
            self.scroll_bg.center(self.player_rect.center)
            self.player_rect = pg.Rect(*self.true_pos, *self.player_rect.size)
            player_pos = Vector2(*self.player_rect.topleft)
            prev_player_pos = Vector2(*prev_player_rect.topleft)
            clear_rect = (tuple(prev_player_pos - self.scroll_bg.display_pos),
                          prev_player_rect.size)
            draw_rect = (tuple(player_pos - self.scroll_bg.display_pos),
                         self.player_rect.size)
            self.display.blit(self.scroll_bg.background, clear_rect,
                              prev_player_rect)
            pg.draw.rect(self.display, (255, 0, 0), draw_rect)
            pg.display.set_caption('FPS: {:.2f}'.format(self.clock.get_fps()))
            pg.display.update()

    def handle_input(self, delta_time):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                break
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_z:
                    self.scale(1 / 3)
                    continue
            elif event.type == pg.KEYUP:
                if event.key == pg.K_z:
                    self.scale(3)
                    continue
        if pg.key.get_pressed()[pg.K_LEFT]:
            self.true_pos.x = max(self.true_pos.x - self.speed*delta_time, 0)
        elif pg.key.get_pressed()[pg.K_RIGHT]:
            self.true_pos.x = min(
                self.true_pos.x + self.speed*delta_time, self.max_scroll)
        if pg.key.get_pressed()[pg.K_UP]:
            self.true_pos.y = max(self.true_pos.y - self.speed*delta_time, 0)
        elif pg.key.get_pressed()[pg.K_DOWN]:
            self.true_pos.y = min(
                self.true_pos.y + self.speed*delta_time, self.max_scroll)

    def scale(self, factor):
        self.scroll_bg.zoom *= factor
        self.true_pos.scale(factor)
        self.player_rect.width *= factor
        self.player_rect.height *= factor
        self.max_scroll *= factor
        self.speed *= factor


if __name__ == '__main__':
    Game().main()
