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
    print(f"[PONG]: Loading settings from {settings_filepath}")

    if os.path.isfile(settings_filepath):
        config = ConfigParser()
        config.read(settings_filepath)
        return config
    else:
        raise Exception(f"\n\nFile Not Found:\t{settings_filepath}")


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

        # pygame initialization goes here

        # Quiz 2 - Getting a value from settings.ini
        # screen_width = (value from settings.ini)
        # screen_height = (value from settings.ini)
        # print(f"[pygame]: Screen dimensions {screen_width} x {screen_height}")

        print("[pygame]: Initialization Complete.")

    def loop(self):
        print("[PONG]: Game has started.")

        # Quiz 3: Starting the Game Loop
        # game loop goes here

        print("[PONG]: Game has ended.")


def main():
    try:
        game = Pong()
        game.loop()
    except:
        traceback.print_exc()


if __name__ == "__main__":
    main()
