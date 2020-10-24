class Boll:

    def __init__(self, screen_w: int, screen_h: int):
        self.r = 7
        self.dx = 0
        self.dy = -1
        self.speed = 15
        self.x = int(screen_w / 2)
        self.y = screen_h - 30
