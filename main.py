import math

import screeninfo
from cv2 import cv2

from Board import Board
from Boll import Boll
from find_faces import find_faces

screen_w = 640
screen_h = 480

boll = Boll(screen_w, screen_h)
board = Board(screen_w)


def calc_boll_center(left, right):
    global boll
    boll.x = int(boll.x + boll.speed * boll.dx)
    boll.y = int(boll.y + boll.speed * boll.dy)

    # правая стенка
    if boll.x > screen_w - boll.r:
        boll.dx = -boll.dx
        boll.x = screen_w - boll.r
        boll.boom()

    # левая стенка
    if boll.x < boll.r:
        boll.dx = -boll.dx
        boll.x = boll.r
        boll.boom()

    if boll.dy < 0 and boll.y < boll.r + 20 and left < boll.x < right:
        boll.y = boll.r + 20
        top_bottom_boom(board)

    if boll.dy > 0 and boll.y > screen_h - 20 - boll.r and left < boll.x < right:
        boll.y = screen_h - 20 - boll.r
        top_bottom_boom(board)


def top_bottom_boom(board):
    d = (boll.x - board.old_center_x) / board.r
    boll.dy = -boll.dy
    boll.dx += d
    mod_d = math.sqrt(boll.dx ** 2 + boll.dy ** 2)
    boll.dy /= mod_d
    boll.dx /= mod_d
    boll.boom()


def work(img):
    global board
    board.center = board.old_center_x
    try:
        (x, y, w, h) = find_faces(img)[0]
        board.old_center_x = board.center = int(x + w / 2)
    except IndexError as _:
        pass
    calc_boll_center(board.center - board.r, board.center + board.r)

    cv2.rectangle(img, (board.center - board.r, screen_h - 20), (board.center + board.r, screen_h - 20), board.color, 4)
    cv2.rectangle(img, (board.center - board.r, 20), (board.center + board.r, 20), board.color, 4)
    cv2.circle(img, (boll.x, boll.y), boll.r, (255, 255, 255), -1)
    cv2.circle(img, (boll.x, boll.y), boll.r - 2, boll.color, -1)
    return img


def run():
    cap = cv2.VideoCapture(0)
    screen = screeninfo.get_monitors()[0]
    window_name = "cvgame"
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.moveWindow(window_name, screen.x - 1, screen.y - 1)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    org = (50, 50)
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 1
    while True:
        ret, img = cap.read()
        img = cv2.flip(img, 1)
        cv2.putText(img, str(boll.count), org, font, fontScale, (255, 255, 255))
        img = work(img)
        cv2.imshow(window_name, img)
        if cv2.waitKey(10) == 27:  # Клавиша Esc
            break
        if boll.y > screen_h or boll.y < 0:
            print('the end...')
            break
    cv2.putText(img, 'Game over.', (50, 100), font, fontScale, (255, 255, 255))
    cv2.imshow(window_name, img)
    cv2.waitKey(10000)


if __name__ == '__main__':
    run()
