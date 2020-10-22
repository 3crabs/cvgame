from cv2 import cv2

faceCascade = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')

gray_h = 90

screen_w = 640
screen_h = 480
board_w = 100
boll_center_x = int(screen_w / 2)
boll_center_y = screen_h - 30
boll_dx = 1
boll_dy = -1
boll_speed = 10
boll_r = 7


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
    global boll_center_x, boll_center_y, boll_dx, boll_dy
    boll_center_x = boll_center_x + boll_speed * boll_dx
    boll_center_y = boll_center_y + boll_speed * boll_dy

    if boll_center_x > screen_w - boll_r or boll_center_x < boll_r:
        boll_dx = -boll_dx

    if boll_center_y < boll_r:
        boll_dy = -boll_dy

    if boll_center_y > screen_h - 20 - boll_r and (left < boll_center_x < right):
        boll_dy = -boll_dy


def work(img):
    try:
        (x, y, w, h) = find_faces(img)[0]
        center = int(x + w / 2)
        cv2.rectangle(img, (center - board_w, screen_h - 20), (center + board_w, screen_h - 20), (255, 255, 255), 4)
        calc_boll_center(center - board_w, center + board_w)
        cv2.circle(img, (boll_center_x, boll_center_y), 7, (255, 255, 255))
    except IndexError as _:
        pass
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
        if boll_center_y > screen_h:
            print('the end...')
            break


if __name__ == '__main__':
    run()
