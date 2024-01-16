from configparser import ConfigParser
import os
import pygame
import traceback


def get_parent_directory_of_pong_py() -> str:
    return os.path.abspath(os.path.dirname(__file__))


def get_settings_filepath() -> str:
    parent_directory = get_parent_directory_of_pong_py()
    return os.path.realpath(parent_directory + "/data/settings.ini")


def load_settings() -> ConfigParser:
    settings_filepath = get_settings_filepath()
    print(f"Loading settings from {settings_filepath}")

    if os.path.isfile(settings_filepath):
        config = ConfigParser()
        config.read(settings_filepath)
        return config
    else:
        raise Exception(f"\n\nFile Not Found:\t{settings_filepath}")

def get_screen_center(width: float, height: float) -> pygame.Vector2:
    return pygame.Vector2(width / 2, height / 2)

class Ball:
    def __init__(self, side_length: int, position: pygame.Vector2, color: str):
        self.side_length = side_length
        self.position = position
        self.color = color

    def get_position(self) -> pygame.Vector2:
        return self.position

    def set_position(self, x: float, y: float):
        self.position = pygame.Vector2(x, y)

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(
            self.position.x - (self.side_length / 2),
            self.position.y - (self.side_length / 2),
            self.side_length,
            self.side_length
        )


class Pong:
    def __init__(self):
        print("[PONG]: Initializing ...")

        self.is_running = False
        self.screen = None
        self.clock = None
        self.settings = load_settings()

        self.initialize_pygame()

        print("[PONG]: Initialization Complete.")

    def __del__(self):
        pygame.quit()

    def initialize_pygame(self):
        print("[pygame]: Initializing ...")

        pygame.init()

        screen_width = self.settings.getint("Screen", "width")
        screen_height = self.settings.getint("Screen", "height")
        print(f"[pygame]: Screen dimensions {screen_width} x {screen_height}")

        self.screen = pygame.display.set_mode((screen_width, screen_height))

        self.clock = pygame.time.Clock()

        print("[pygame]: Initialization Complete.")

    def loop(self):
        print("[PONG]: Game has started.")

        ball = Ball(self.settings.getint("Ball", "side_length"), 
                    get_screen_center(self.settings.getint("Screen", "width"), self.settings.getint("Screen", "height")), 
                    self.settings.get("Ball", "color"))

        self.is_running = True

        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

            self.screen.fill("black")
            pygame.draw.rect(self.screen, ball.color, ball.get_rect())
            pygame.display.flip()

        print("[PONG]: Game has ended.")


def main():
    try:
        game = Pong()
        game.loop()
    except:
        traceback.print_exc()


if __name__ == "__main__":
    main()
