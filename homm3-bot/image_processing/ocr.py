"""Script containing OCR functions that help us with reading text."""
import cv2
import cv2 as cv
import numpy as np
import pytesseract

# YOU HAVE TO SET YOUR OWN PATH
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def read_text(image, psm=10, battle=False, fml=False):
    """
    It can usually read HOTA font clearly if it's big enough.
    Typically shouldn't be used. read_generic_text should be used for general cases
    :param image: Input image
    :param psm: Page segmentation. Set to 10 by default.
    :param battle: Boolean. Set to true if we are reading text in battle
    :return: text
    """
    result = _check_if_white(image)
    if result:
        return ""
    if battle:
        return pytesseract.image_to_string(image,
                                           config=f'--psm {psm} --oem 3 -c tessedit_char_whitelist=0123456789')
    if fml:
        return pytesseract.image_to_string(image, config=f'--psm {psm} --oem 3')
    return pytesseract.image_to_string(image)


def prepare_text(image, scale, building=False, dilate=False, red_text=False):
    """
    Prepare text for tesseract usage - thresholding and dilation
    :param image: Input image.
    :param scale: Parameter used in resizing windows. Multiplied by height and width
    :param building: Boolean. Set to true if we are operating on the building
    :param dilate: Boolean. Set to true if dilation operation is to be done.
    :param red_text: Boolean. Set to true if we are reading red text.
    :return: mask put on an image
    """
    width = image.shape[1]
    height = image.shape[0]
    img = cv.resize(image, (width * scale, height * scale))
    b, g, r = cv2.split(img)
    if not building:
        search = np.where((b > 140) &
                          (g > 150) &
                          (r > 150))
    else:
        search = np.where((b > 85) &
                          (g > 160) &
                          (r > 170))

    if red_text:
        search = np.where((b > 50) &
                          (g > 55) &
                          (r > 100))

    mask = np.full((height * scale, width * scale, 3), 0, dtype=np.uint8)
    mask[search] = [255, 255, 255]
    kernel = np.ones((3, 3), np.uint8)
    if dilate:
        mask = cv.dilate(mask, kernel, iterations=1)
    mask = 255-mask
    return mask


def read_generic_text(img, scale=4):
    """
    The given image has to contain just one text without the picture
    Bigger scale can make letters unreadable because of pixelation especially if they are small at the beginning
    :param img: Input image
    :param scale: Parameter used in resizing windows
    :return: text
    """
    temp_img = prepare_text(img, scale, False, False)
    result = _check_if_white(temp_img)
    if result:
        return ""
    temp_img_dilated = prepare_text(img, scale, True, True)

    text = read_text(temp_img, True)
    if not text:
        text = read_text(temp_img_dilated, True)
        text = text.strip()

    if not text:
        for psm in range(4, 13):
            if not text:
                text = read_text(temp_img, psm, True)
                text = text.strip()
            else:
                break

    if not text:
        for psm in reversed(range(4, 13)):
            if not text:
                text = read_text(temp_img_dilated, psm, True)
                text = text.strip()

    if not text:
        for psm in range(4, 13):
            if not text:
                text = read_text(img, psm, True)
                text = text.strip()
    text = text.replace('\n', ' ')
    text = text.strip()
    return text


def read_text_faster(img, scale=4):
    """
    Same thing as read_generic_text but fewer checks so used when there can sometimes be no text
    :param img: Input image
    :param scale: Parameter used in resizing windows.
    :return: text
    """
    temp_img = prepare_text(img, scale, False, False)
    result = _check_if_white(temp_img)
    if result:
        return ""
    temp_img_dilated = prepare_text(img, scale, False, True)
    text = read_text(temp_img, battle=True)
    if not text:
        text = read_text(temp_img_dilated, battle=True)
        text = text.strip()

    if not text:
        for psm in range(4, 13):
            if not text:
                text = read_text(temp_img_dilated, psm, True)
                text = text.strip()
            else:
                break
    return text


def read_generic_numbers(img, scale=4, banned_psm=None,redtext = False):
    """
    Eliminates all answers it finds that contain letters
    The given image has to contain just one text without the picture

    :param img: Input image
    :param scale: Parameter used in resizing windows.
    :param banned_psm: Which PSM we do not want to use
    :param redtext: if background of image is red
    :return: text, psm.
    """
    temp_img = prepare_text(img, scale, False, False, red_text=redtext)
    # cv2.imshow("", temp_img)
    # cv2.waitKey()
    result = _check_if_white(temp_img)
    if result:
        return ""
    temp_img_dilated = prepare_text(img, scale, True, False)
    text = read_text(temp_img, True)
    psm = 4
    if (not text or not text.isdigit()) and psm not in banned_psm:
        text = read_text(temp_img, True)
        text = text.strip()

    if not text or not text.isdigit():
        for psm in range(6, 13):
            if psm in banned_psm:
                continue
            if not text or not text.isdigit():
                text = read_text(temp_img, psm, True)
                text = text.strip()
            else:
                psm = psm-1
                break

    if not text or not text.isdigit():
        for psm in reversed(range(4, 13)):
            if psm in banned_psm:
                continue
            if not text or not text.isdigit():
                text = read_text(temp_img_dilated, psm, True)
                text = text.strip()
            else:
                psm = psm-1
                break

    if not text or not text.isdigit():
        for psm in range(4, 13):
            if psm in banned_psm:
                continue
            if not text or not text.isdigit():
                text = read_text(img, psm, True)
                text = text.strip()
            else:
                psm = psm-1
                break
    text = text.replace('\n', ' ')
    text = text.strip()
    return text, psm


def battle_unit_count(img, scale=4, red_unit=False):
    """
    Used in battle - different thresholds only works for red player
    The given image has to contain just one text without the picture
    :param img: Input image
    :param scale: Parameter used in resizing windows.
    :param red_unit: Boolean. Set to true if a unit is red
    :return: text
    """
    temp_img = prepare_text(img, scale, False, False, red_unit)
    result = _check_if_white(temp_img)
    if result:
        return ""
    temp_img_dilated = prepare_text(img, scale, False, True, red_unit)

    text = read_text(temp_img_dilated, battle=True)
    text = text.strip()
    if not text or not text.isdigit():
        text = read_text(temp_img, battle=True)
        text = text.strip()

    if not text or not text.isdigit():
        for psm in reversed(range(4, 13)):
            if not text or not text.isdigit():
                text = read_text(temp_img, psm, True)
                text = text.strip()

    if not text or not text.isdigit():
        for psm in range(4, 13):
            if not text or not text.isdigit():
                text = read_text(temp_img_dilated, psm, True)
                text = text.strip()
            else:
                break

    if not text or not text.isdigit():
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        for psm in range(4, 13):
            if not text or not text.isdigit():
                text = read_text(img, psm, True)
                text = text.strip()
    text = text.replace('\n', ' ')
    text = text.strip()
    return text

def _check_if_white(img):
    """
    Checks if image is fully white
    :param img: Image to be checked
    :return: True or false
    """
    result = np.all(img == 255)
    return result


