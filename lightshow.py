#!/usr/bin/env python

import math
import time
from threading import Thread

import unicornhat as unicorn

unicorn.set_layout(unicorn.AUTO)
unicorn.rotation(0)
unicorn.brightness(0.5)
width,height=unicorn.get_shape()


class LightShow:

    def __init__(self):
        self._running = False

    def start(self):
        self._running = True
        self.thread = Thread(target=self.run)
        self.thread.start()

    def stop(self):
        self._running = False
        time.sleep(0.1)
        unicorn.clear()
        unicorn.show()

    def run(self):
        i = 0.0
        offset = 30
        t_end = time.time() + 20

        while self._running:
            i = i + 0.3
            for y in range(height):
                    for x in range(width):
                            r = 0
                            g = 0
                            r = (math.cos((x+i)/2.0) + math.cos((y+i)/2.0)) * 64.0 + 128.0
                            g = (math.sin((x+i)/1.5) + math.sin((y+i)/2.0)) * 64.0 + 128.0
                            b = (math.sin((x+i)/2.0) + math.cos((y+i)/1.5)) * 64.0 + 128.0
                            r = max(0, min(255, r + offset))
                            g = max(0, min(255, g + offset))
                            b = max(0, min(255, b + offset))
                            unicorn.set_pixel(x,y,int(r),int(g),int(b))
            unicorn.show()
            time.sleep(0.01)
