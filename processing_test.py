import sys
import json
import time
from collections import defaultdict
import logging

import zmq

from random import choice, randint


from processing import *


NUMBER_OF_WALKERS = 10000


class Walker(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.x = randint(0, self.width)
        self.y = randint(0, self.height)

    @property
    def position(self):
        return {'x': self.x, 'y': self.y}

    def step(self):
        direction = choice(['left', 'right', 'forward', 'backward'])
        if direction == 'left':
            self.x -= 1
        elif direction == 'right':
            self.x += 1
        elif direction == 'forward':
            self.y += 1
        elif direction == 'backward':
            self.y -= 1

        if self.x > self.width:
            self.x = self.width
        elif self.x < 0:
            self.x = 0
        if self.y > self.height:
            self.y = self.height
        elif self.y < 0:
            self.y = 0


class RandomWalkers(Sketch):
    width = 1250
    height = 650
    frame_rate = 30

    def setup(self):
        self.walkers = [Walker(self.width, self.height) for i in range(NUMBER_OF_WALKERS)]

    def draw(self):
        data = defaultdict(list)
        for w in self.walkers:
            w.step()
            data['objects'].append(w.position)
        self.frame = data

if __name__ == '__main__':
    sketch = RandomWalkers()
    sketch.run(port=8888)
