import biomes
from colours import Colours

import random
import cv2
import numpy as np
import threading

import time


def hex_to_rgb(hex):
    # CV2 uses BGR instead of RGB
    hex = hex.lstrip('#')
    return tuple(int(hex[i:i+2], 16) for i in (4, 2, 0))


class Island:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = [[None for _ in range(width)] for _ in range(height)]
        self._generate_standard()
        self.tempMap = None

    def _generate_standard(self):
        for y in range(self.height):
            for x in range(self.width):
                # If the tile is within the elipse of the island, it is land, accounting for a 10% border around the edge
                if (x - self.width / 2) ** 2 / (self.width / 2 * 0.9) ** 2 + (y - self.height / 2) ** 2 / (self.height / 2 * 0.9) ** 2 <= 1:
                    # If it is in the outer 10% of the island, it is more likely to be a cliff or desert
                    if 1 <= (x - self.width / 2) ** 2 / (self.width / 2 * 0.9) ** 2 + (y - self.height / 2) ** 2 / (self.height / 2 * 0.9) ** 2 <= 1.1:
                        self.tiles[y][x] = random.choices([biomes.Cliff, biomes.Desert], [0.2, 0.8])[0]()
                    else:
                        self.tiles[y][x] = random.choice(biomes.allBiomes)
                else:
                    self.tiles[y][x] = biomes.Ocean()

    def _is_on_edge(self, x, y) -> bool:
        if x == 0 or x == self.width - 1 or y == 0 or y == self.height - 1:
            return True
        return False

    def _nearest_neighbour_thread(self, y):
        for x in range(self.width):
            neighbours = [self.tiles[y][x]]
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if 0 <= x + i < self.width and 0 <= y + j < self.height:
                        neighbours.append(self.tiles[y + j][x + i])
            # Create a dictionary of the neighbours and their frequencies
            neighbourDict = {}
            for neighbour in neighbours:
                if neighbour in neighbourDict:
                    neighbourDict[neighbour] += 1
                else:
                    neighbourDict[neighbour] = 1
            # Square the frequencies to make them more important
            for neighbour in neighbourDict:
                neighbourDict[neighbour] **= 2
            # Choose a random neighbour based on the frequencies
            self.tempMap[y][x] = random.choices(list(neighbourDict.keys()), neighbourDict.values())[0]

    def nearest_neighbour(self):
        self.tempMap = [[None for _ in range(self.width)] for _ in range(self.height)]
        # For each row, create a thread to calculate the nearest neighbour
        threads = []
        for y in range(self.height):
            thread = threading.Thread(target=self._nearest_neighbour_thread, args=(y,))
            threads.append(thread)
            thread.start()
        # Wait for all threads to finish
        for thread in threads:
            thread.join()
        self.tiles = self.tempMap

    def _remove_isolated_tiles_thread(self, y):
        for x in range(self.width):
            # If all 4 tiles around the current tile are the same, set the current tile to that tile
            neighbours = []
            if not self._is_on_edge(x, y):
                neighbours.append(self.tiles[y - 1][x])
                neighbours.append(self.tiles[y + 1][x])
                neighbours.append(self.tiles[y][x - 1])
                neighbours.append(self.tiles[y][x + 1])

                if all(neighbour == neighbours[0] for neighbour in neighbours):
                    self.tempMap[y][x] = neighbours[0]
                else:
                    self.tempMap[y][x] = self.tiles[y][x]
            else:
                self.tempMap[y][x] = self.tiles[y][x]

    def remove_isolated_tiles(self):
        # Convert the code above to threading like the other function
        self.tempMap = [[None for _ in range(self.width)] for _ in range(self.height)]
        # For each row, create a thread to calculate the nearest neighbour
        threads = []
        for y in range(self.height):
            thread = threading.Thread(target=self._nearest_neighbour_thread, args=(y,))
            threads.append(thread)
            thread.start()
        # Wait for all threads to finish
        for thread in threads:
            thread.join()
        self.tiles = self.tempMap


    def render(self):
        img = np.zeros((self.height, self.width, 3), np.uint8)
        for y in range(self.height):
            for x in range(self.width):
                img[y][x] = hex_to_rgb(self.tiles[y][x].colour)
        img = cv2.resize(img, (1000, int(1000 * self.height / self.width)), interpolation=cv2.INTER_NEAREST)
        cv2.imshow('Island', img)
        print(Colours().Green, "Rendering")
        cv2.waitKey(0)


def generate_loading_bar(low, high, current):
    bar = '['
    for i in range(low, high):
        if i < current:
            bar += '='
        elif i == current:
            bar += '>'
        else:
            bar += ' '
    return bar + ']'


island = Island(100, 100)

nearest_neighbour = 15
remove_isolated_tiles = 20
for x in range(nearest_neighbour):
    island.nearest_neighbour()
    col = Colours().Yellow if x < nearest_neighbour - 1 else Colours().Green
    print(col, "Running nearest neighbour", generate_loading_bar(0, 100, ((x + 1)*100)//nearest_neighbour), end='\r')
print()
for x in range(remove_isolated_tiles):
    island.remove_isolated_tiles()
    col = Colours().Yellow if x < nearest_neighbour - 1 else Colours().Green
    print(col, "Removing isolated tiles  ", generate_loading_bar(0, 100, ((x + 1)*100)//remove_isolated_tiles), end='\r')
print()
print(Colours().Red, "Rendering", end='\r')
island.render()