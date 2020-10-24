import random
from threading import Thread

from pydub import AudioSegment
from pydub.playback import play

filename = 'assets/boom.mp3'
song = AudioSegment.from_mp3(filename)


def music():
    play(song)


class Boll:

    def __init__(self, screen_w: int, screen_h: int):
        self.r = 7
        self.dx = 0
        self.dy = -1
        self.speed = 15
        self.x = int(screen_w / 2)
        self.y = screen_h - 30
        self.color = (255, 255, 255)
        self.count = 0

    def boom(self):
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.count += 1
        Thread(target=music, args=()).start()
