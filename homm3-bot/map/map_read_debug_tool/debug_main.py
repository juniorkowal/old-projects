import sys
import pygame

from file_reader.MainMapClass import Map
from utils import SelectFrame, MapDataVisualAppVersion2


class PyWindow:
    def __init__(self, python_path: str):
        pygame.init()
        self.window = pygame.display.set_mode((1424, 960))
        self.python_map = MapDataVisualAppVersion2(python_path)

    def update(self):
        self.window.fill((0, 0, 0))
        self.python_map.draw(self.window)

        pygame.display.flip()

    def run(self):
        while True:
            self.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                SelectFrame.select(event)


if __name__ == '__main__':
    MAP_H3M_PATH = r"D:/GRY/HoMM3/Maps/random2.h3m"
    app = PyWindow(MAP_H3M_PATH)
    app.run()
