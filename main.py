import math

from cv2 import cv2

from Board import Board
from Boll import Boll
from find_faces import find_faces

screen_w = 640
screen_h = 480

boll = Boll(screen_w, screen_h)
board_bottom = Board(screen_w)
board_top = Board(screen_w)

boom = False


def calc_boll_center(left, right):
    global boll, boom
    boll.x = int(boll.x + boll.speed * boll.dx)
    boll.y = int(boll.y + boll.speed * boll.dy)

    # правая стенка
    if boll.x > screen_w - boll.r:
        boll.dx = -boll.dx
        boll.x = screen_w - boll.r

    # левая стенка
    if boll.x < boll.r:
        boll.dx = -boll.dx
        boll.x = boll.r

    if boll.dy < 0 and boll.y < boll.r + 20 and left < boll.x < right:
        boll.y = boll.r + 20
        top_bottom_boom(board_top)

    if boll.dy > 0 and boll.y > screen_h - 20 - boll.r and left < boll.x < right:
        boll.y = screen_h - 20 - boll.r
        top_bottom_boom(board_bottom)


def top_bottom_boom(board):
    d = (boll.x - board.old_center_x) / board.r
    boll.dy = -boll.dy
    boll.dx += d
    mod_d = math.sqrt(boll.dx ** 2 + boll.dy ** 2)
    boll.dy /= mod_d
    boll.dx /= mod_d


def work(img):
    global board_bottom
    board_bottom.center = board_bottom.old_center_x
    try:
        (x, y, w, h) = find_faces(img)[0]
        board_bottom.old_center_x = board_bottom.center = int(x + w / 2)
    except IndexError as _:
        pass
    cv2.rectangle(img, (board_bottom.center - board_bottom.r, screen_h - 20),
                  (board_bottom.center + board_bottom.r, screen_h - 20),
                  (255, 255, 255), 4)
    cv2.rectangle(img, (board_bottom.center - board_bottom.r, 20), (board_bottom.center + board_bottom.r, 20),
                  (255, 255, 255), 4)
    calc_boll_center(board_bottom.center - board_bottom.r, board_bottom.center + board_bottom.r)
    cv2.circle(img, (boll.x, boll.y), 7, (255, 255, 255), -1)
    return img


def run():
    cap = cv2.VideoCapture(0)
    while True:
        ret, img = cap.read()
        img = cv2.flip(img, 1)
        img = work(img)
        cv2.imshow("cvgame", img)
        if cv2.waitKey(10) == 27:  # Клавиша Esc
            break
        if boll.y > screen_h or boll.y < 0:
            print('the end...')
            break


if __name__ == '__main__':
    run()
