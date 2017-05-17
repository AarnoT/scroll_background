import pygame as pg

from scroll_background import ScrollBackground

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
        display_rect = pg.Rect((0, 0), self.display.get_size())
        display_rect.clamp_ip((0, 0), self.background.get_size())
        display_pos = display_rect.topleft
        draw_grid(self.background)
        self.scroll_bg = ScrollBackground(
            self.background, self.display, display_pos)
        self.scroll_bg.blit(pg.Surface((123, 123)), (300, 300))
        self.display.blit(
            self.scroll_bg.background, (0, 0),
            pg.Rect(display_pos, self.display.get_size()))

        self.player_rect = pg.Rect(
            self.background.get_width()//2 - 50,
            self.background.get_width()//2 - 50, 100, 100)
        self.true_x_pos, self.true_y_pos = self.player_rect.topleft
        self.max_scroll = self.background.get_width() - self.player_rect.width
        self.x_size, self.y_size = self.player_rect.size
        self.speed = 5
        self.clock = pg.time.Clock()
        self.running = True

    def main(self):
        while self.running:
            delta_time = self.clock.tick(60)/1000 * 60
            prev_player_rect = self.player_rect.copy()
            prev_player_rect.x -= self.scroll_bg.scrolling_area.x
            prev_player_rect.y -= self.scroll_bg.scrolling_area.y
            self.handle_input(delta_time)
            self.scroll_bg.center((self.true_x_pos + self.x_size/2,
                                   self.true_y_pos + self.y_size/2))
            clear_rect = (prev_player_rect.x +
                          self.scroll_bg.scrolling_area.x -
                          self.scroll_bg.display_pos.x,
                          prev_player_rect.y +
                          self.scroll_bg.scrolling_area.y -
                          self.scroll_bg.display_pos.y,
                          *prev_player_rect.size)
            self.player_rect = pg.Rect(
                self.true_x_pos + self.scroll_bg.scrolling_area.x,
                self.true_y_pos + self.scroll_bg.scrolling_area.y,
                self.x_size,
                self.y_size)
            draw_rect = (
                self.player_rect.left - self.scroll_bg.display_pos.x,
                self.player_rect.top - self.scroll_bg.display_pos.y,
                self.x_size,
                self.y_size)
            self.display.blit(
                self.scroll_bg.background,
                clear_rect,
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
                    self.scroll_bg.zoom = 1 / 3
                    self.true_x_pos /= 3
                    self.true_y_pos /= 3
                    self.x_size /= 3
                    self.y_size /= 3
                    self.max_scroll /= 3
                    self.speed /= 3
                    continue
            elif event.type == pg.KEYUP:
                if event.key == pg.K_z:
                    self.scroll_bg.zoom = 1.0
                    self.true_x_pos *= 3
                    self.true_y_pos *= 3
                    self.x_size *= 3
                    self.y_size *= 3
                    self.max_scroll *= 3
                    self.speed *= 3
                    continue
        if pg.key.get_pressed()[pg.K_LEFT]:
            self.true_x_pos = max(self.true_x_pos - self.speed*delta_time, 0)
        elif pg.key.get_pressed()[pg.K_RIGHT]:
            self.true_x_pos = min(
                self.true_x_pos + self.speed*delta_time, self.max_scroll)
        if pg.key.get_pressed()[pg.K_UP]:
            self.true_y_pos = max(self.true_y_pos - self.speed*delta_time, 0)
        elif pg.key.get_pressed()[pg.K_DOWN]:
            self.true_y_pos = min(
                self.true_y_pos + self.speed*delta_time, self.max_scroll)


if __name__ == '__main__':
    Game().main()
