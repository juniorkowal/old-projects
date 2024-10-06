"""Script containing okay button detection, which helps us with handling windows"""
import time
import numpy as np
import cv2 as cv
import pyautogui


def compare(result, result_image, image):
    """
    Single function to detect if the best match image is exact same as we need
    :param result: image of the best match
    :param result_image: stock image (e.g. battle_result.png)
    :param image: screenshot
    :return: returning 1 if its exact the same
    """
    is_on_image = 0
    mn, _, mnLoc, _ = cv.minMaxLoc(result)
    MPx, MPy = mnLoc
    trows, tcols = result_image.shape[:2]
    ok_compare = image[MPy:MPy + trows, MPx:MPx + tcols]

    # comparing to the normal icon image
    compare1 = cv.compare(result_image, ok_compare, 0)
    if compare1.all():
        is_on_image = 1
    return is_on_image


def check_ok(x=None,y=None,x1=None,y1=None):
    """
    Function responsible for detecting if there is an okay on the screen. Crucial in window handling.
    :return: 0 - no okay button, 1 - green okay button, 2 - grey okay button, 3 - skill okay button, 4 - city okay button
    """
    # return 0 if there is no okay button
    # return 1 if there is normal (green) okay button
    # return 2 if there is grey okay button
    # return 3 if there is skill grey okay
    # return 4 if there is city okay
    which_okay = 0
    # getting screenshot, okay icon and grey okay icon
    ok_image = cv.imread(r'.\image_processing\okey.png')
    ok_image_grey = cv.imread(r'.\image_processing\okey_grey.png')
    ok_image_grey_skill = cv.imread(r'.\image_processing\okey_skill_grey.png')
    ok_city = cv.imread(r'.\image_processing\okey_city.png')
    print(ok_image.shape)
    timeout = time.time() + 4

    while not which_okay:
        if time.time() > timeout:
            break
        image = pyautogui.screenshot()
        image = cv.cvtColor(np.array(image), cv.COLOR_RGB2BGR)

        if x is not None and y is not None and x1 is not None and y1 is not None:
            image = image[y:y1, x:x1]
        elif x is not None and y is None and y1 is None and x1 is not None:
            image = image[:, x:x1]

        # matching with the original image
        method = cv.TM_SQDIFF_NORMED
        result_normal = cv.matchTemplate(ok_image, image, method)
        result_grey = cv.matchTemplate(ok_image_grey, image, method)
        result_grey_skill = cv.matchTemplate(ok_image_grey_skill, image, method)
        result_city = cv.matchTemplate(ok_city, image, method)

        a = compare(result_normal, ok_image, image)
        b = compare(result_grey, ok_image_grey, image)
        c = compare(result_grey_skill, ok_image_grey_skill, image)
        d = compare(result_city, ok_city, image)

        if a == 1:
            which_okay = 1
        elif b == 1:
            which_okay = 2
        elif c == 1:
            which_okay = 3
        elif d == 1:
            which_okay = 4

    return which_okay


if __name__ == "__main__":
    """
    Testing facility boys
    """
    import os
    print(os.getcwd())
    time.sleep(5)
    okay = check_ok(x=830, x1=1060)# zmienic sciezki dla tego folderu ;)
    if okay:
        print("OK")
    else:
        print("not ok")

