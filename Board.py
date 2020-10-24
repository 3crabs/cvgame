class Board:

    def __init__(self, screen_w: int):
        self.r = 80
        self.old_center_x = screen_w / 2
        self.center = 0
        self.color = (255, 255, 255)
