import pygame
import random
from configparser import ConfigParser

config = ConfigParser()
config.read('settings.ini')

# Load Screen Settings
SCREEN_WIDTH = config.getfloat("Screen", "width")
SCREEN_HEIGHT = config.getfloat("Screen", "height")
SCREEN_CENTER_X = SCREEN_WIDTH / 2
SCREEN_CENTER_Y = SCREEN_HEIGHT / 2
FPS = config.getfloat("Screen", "fps")

# Load Environment Settings

# Load Paddle Settings
PADDLE_WIDTH = config.getfloat("Paddle", "width")
PADDLE_HEIGHT = config.getfloat("Paddle", "height")
PADDLE_SPEED = config.getfloat("Paddle", "max_speed_y")
PADDLE_COLOR = config.get("Paddle", "color")
PADDLE_SCREEN_OFFSET = PADDLE_WIDTH

# Load Ball Settings
BALL_SIZE = 5
BALL_SPEED_MAX = 200
BALL_COLOR = config.get("Ball", "color")

# AI
AI_ON = config.getboolean("AI", "on")

# Initialize Players and Ball
p1_pos = pygame.Vector2(PADDLE_SCREEN_OFFSET, SCREEN_HEIGHT / 2)
p2_pos = pygame.Vector2(SCREEN_WIDTH - PADDLE_SCREEN_OFFSET, SCREEN_HEIGHT / 2)
ball_pos = pygame.Vector2(SCREEN_CENTER_X, SCREEN_CENTER_Y)
ball_vel = pygame.Vector2(
    random.uniform(-BALL_SPEED_MAX, BALL_SPEED_MAX),
    random.uniform(-BALL_SPEED_MAX, BALL_SPEED_MAX)
)


def initialize_pygame():
    pygame.init()

    logo = pygame.image.load("logo.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("pong")


def handle_input(keys, dt):

    # player 1
    if keys[pygame.K_w]:
        p1_pos.y -= PADDLE_SPEED * dt
    if keys[pygame.K_s]:
        p1_pos.y += PADDLE_SPEED * dt

    # player 2
    if not AI_ON:
        if keys[pygame.K_UP]:
            p2_pos.y -= PADDLE_SPEED * dt
        if keys[pygame.K_DOWN]:
            p2_pos.y += PADDLE_SPEED * dt
    else:
        chance_roll = random.uniform(0.0, 1.0)

        if p2_pos.y > ball_pos.y:
            if (chance_roll > 0.6):
                p2_pos.y -= PADDLE_SPEED * dt
        if p2_pos.y < ball_pos.y:
            if (chance_roll > 0.6):
                p2_pos.y += PADDLE_SPEED * dt


def update_game(dt):
    global ball_pos

    ball_pos.x += (ball_vel.x * dt)
    ball_pos.y += (ball_vel.y * dt)

    # check if ball is out of bounds (left or right)
    if (ball_pos.x <= 0) or (ball_pos.x >= SCREEN_WIDTH):
        ball_pos = pygame.Vector2(SCREEN_CENTER_X, SCREEN_CENTER_Y)

    # check if ball hit top or bottom of screen
    elif (ball_pos.y <= 0) or (ball_pos.y >= SCREEN_HEIGHT):
        ball_vel.y *= -1

    # check if ball hit paddle 1
    elif ((ball_pos.x >= (p1_pos.x - (PADDLE_WIDTH / 2)) and ball_pos.x <= p1_pos.x + (PADDLE_WIDTH / 2)) and
          (ball_pos.y >= (p1_pos.y - (PADDLE_HEIGHT / 2)) and ball_pos.y <= p1_pos.y + (PADDLE_HEIGHT / 2))):
        ball_vel.x *= -1

    # check if ball hit paddle 2
    elif ((ball_pos.x >= (p2_pos.x - (PADDLE_WIDTH / 2)) and ball_pos.x <= p2_pos.x + (PADDLE_WIDTH / 2)) and
          (ball_pos.y >= (p2_pos.y - (PADDLE_HEIGHT / 2)) and ball_pos.y <= p2_pos.y + (PADDLE_HEIGHT / 2))):
        ball_vel.x *= -1


def render(screen):
    screen.fill("black")

    # left, top, width, height
    p1_paddle = pygame.Rect(
        p1_pos.x - (PADDLE_WIDTH / 2),
        p1_pos.y - (PADDLE_HEIGHT / 2),
        PADDLE_WIDTH,
        PADDLE_HEIGHT
    )

    # left, top, width, height
    p2_paddle = pygame.Rect(
        p2_pos.x - (PADDLE_WIDTH / 2),
        p2_pos.y - (PADDLE_HEIGHT / 2),
        PADDLE_WIDTH,
        PADDLE_HEIGHT
    )

    # left, top, width, height
    ball = pygame.Rect(
        ball_pos.x - (BALL_SIZE / 2),
        ball_pos.y - (BALL_SIZE / 2),
        BALL_SIZE,
        BALL_SIZE
    )

    pygame.draw.rect(screen, PADDLE_COLOR, p1_paddle)
    pygame.draw.rect(screen, PADDLE_COLOR, p2_paddle)
    pygame.draw.rect(screen, BALL_COLOR, ball)

    pygame.display.flip()


def main():

    initialize_pygame()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

    running = True
    while running:

        # quit if we need to
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # take input
        keys = pygame.key.get_pressed()

        # update the game
        handle_input(keys, dt)
        update_game(dt)

        # render
        render(screen)

        # fix the timestep to FPS
        # delta time from clock.tick() is in millis, we want seconds hence div by 1000
        dt = clock.tick(FPS) / 1000

    pygame.quit()


if __name__ == "__main__":
    main()
