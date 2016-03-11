import pygame, sys
from pygame.locals import *

STICK_WIDTH = 50
BALL_WIDTH = 25
BALL_SLOWNESS = 6

SCREEN_Y_MARGIN = 60
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class MovingObject(object):
    def __init__(self, surface, x, y, image):
        self.x = x
        self.y = y
        self.surface = surface
        self.image = image

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def draw(self):
        self.surface.blit(self.image, (self.x, self.y))


class Stick(MovingObject):
    def __init__(self, surface, x, y, image):
        super().__init__(surface, x, y, image)

    def move(self, dx, dy):
        super().move(dx, dy)
        if self.x + STICK_WIDTH > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - STICK_WIDTH
        if self.x < 0:
            self.x = 0

    def draw(self):
        super().draw()

    def close_to(self, ball):
        if abs(self.x - ball.x) < STICK_WIDTH and abs(self.y - ball.y) < BALL_WIDTH and not ball.was_last_bounced:
            return True
        else:
            return False


class Ball(MovingObject):
    def __init__(self, surface, x, y, image):
        super().__init__(surface, x, y, image)
        self.direction_x = 1
        self.direction_y = 1
        self.was_last_bounced = False
        self.last_bounce_count = 0

    def move(self):
        super().move(self.direction_x, self.direction_y)
        if self.x + BALL_WIDTH > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - BALL_WIDTH
            self.direction_x *= -1
        if self.x < 0:
            self.x = 0
            self.direction_x *= -1
        if self.y + BALL_WIDTH > SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - BALL_WIDTH
            self.direction_y *= -1
        if self.y < 0:
            self.y = 0
            self.direction_y *= -1
        if self.was_last_bounced:
            self.last_bounce_count += 1
            if self.last_bounce_count > BALL_WIDTH + 1:
                self.was_last_bounced = False

    def bounce(self):
        if self.was_last_bounced:
            return
        self.was_last_bounced = True
        self.last_bounce_count = 1
        self.direction_y *= -1

    def draw(self):
        super().draw()


def the_end():
    pygame.quit()
    sys.exit()


def main():
    sticks = []
    balls = []
    pygame.init()
    window_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

    pygame.display.set_caption('Simple pong!')
    WHITE = (255, 255, 255)

    window_surface.fill(WHITE)
    stick_image = pygame.image.load('stick.png')
    upper_stick = Stick(window_surface, SCREEN_WIDTH / 2 - STICK_WIDTH / 2, SCREEN_Y_MARGIN, stick_image)
    lower_stick = Stick(window_surface, SCREEN_WIDTH / 2 - STICK_WIDTH / 2, SCREEN_HEIGHT - SCREEN_Y_MARGIN,
                        stick_image)
    sticks.append(upper_stick)
    sticks.append(lower_stick)

    ball_image = pygame.image.load('ball.png')
    balls.append(Ball(window_surface, SCREEN_WIDTH / 2, SCREEN_Y_MARGIN, ball_image))
    balls.append(Ball(window_surface, SCREEN_WIDTH / 2, SCREEN_HEIGHT - SCREEN_Y_MARGIN, ball_image))

    for stick in sticks:
        stick.draw()
    # pygame.draw.circle(window_surface, BLUE, (300, 50), 20, 0)
    # pygame.draw.ellipse(window_surface, RED, (300, 250, 40, 80), 1)
    pygame.display.update()
    tick_count = 0
    ticker = pygame.time.Clock()
    while True:
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            print("Esc")
            the_end()
        update = False
        tick_count += ticker.tick()
        if tick_count > BALL_SLOWNESS:
            for ball in balls:
                ball.move()
            update = True
            tick_count = 0
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            update = True
            lower_stick.move(-1, 0)

        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            update = True
            lower_stick.move(1, 0)

        if pygame.key.get_pressed()[pygame.K_a]:
            update = True
            upper_stick.move(-1, 0)

        if pygame.key.get_pressed()[pygame.K_d]:
            update = True
            upper_stick.move(1, 0)

        if update:
            for stick in sticks:
                for ball in balls:
                    if stick.close_to(ball):
                        ball.bounce()
            for stick in sticks:
                stick.draw()
            for ball in balls:
                ball.draw()
            pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                the_end()


if __name__ == "__main__":
    main()
