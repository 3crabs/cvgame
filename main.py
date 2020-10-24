import math

from cv2 import cv2

from Boll import Boll

faceCascade = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')

gray_h = 90

screen_w = 640
screen_h = 480
board_w = 100
board_old_center_x = screen_w / 2
boom = False

boll = Boll(screen_w, screen_h)


def find_faces(img):
    return faceCascade.detectMultiScale(
        img,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(20, 20))


def norm(a, min_a, max_a):
    ret = a
    if ret < min_a:
        ret = min_a
    if ret > max_a:
        ret = max_a
    return ret


def calc_boll_center(left, right):
    global boll, boom
    boll.x = int(boll.x + boll.speed * boll.dx)
    boll.y = int(boll.y + boll.speed * boll.dy)

    if boll.x > screen_w - boll.r:
        boll.dx = -boll.dx
        boll.x = screen_w - boll.r

    if boll.x < boll.r:
        boll.dx = -boll.dx
        boll.x = boll.r

    if boll.y < boll.r:
        boll.dy = -boll.dy
        boll.y = boll.r

    if boll.y > screen_h - 20 - boll.r and left < boll.x < right:
        if not boom:
            boom = True
            d = (boll.x - board_old_center_x) / board_w
            boll.dy = -boll.dy
            boll.dx += d
            mod_d = math.sqrt(boll.dx ** 2 + boll.dy ** 2)
            boll.dy /= mod_d
            boll.dx /= mod_d
    else:
        boom = False


def work(img):
    global board_old_center_x
    center = board_old_center_x
    try:
        (x, y, w, h) = find_faces(img)[0]
        board_old_center_x = center = int(x + w / 2)
    except IndexError as _:
        pass
    cv2.rectangle(img, (center - board_w, screen_h - 20), (center + board_w, screen_h - 20), (255, 255, 255), 4)
    calc_boll_center(center - board_w, center + board_w)
    cv2.circle(img, (boll.x, boll.y), 7, (255, 255, 255), -1)
    return img


def run():
    cap = cv2.VideoCapture(0)
    while True:
        ret, img = cap.read()
        img = cv2.flip(img, 1)
        img = work(img)
        cv2.imshow("camera", img)
        if cv2.waitKey(10) == 27:  # Клавиша Esc
            break
        if boll.y > screen_h:
            print('the end...')
            break


if __name__ == '__main__':
    run()
