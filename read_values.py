import numpy as np
import pytesseract
import threading

import cv2
import sys


# some information:
# Script for reading data from Formula 1 onboard graphics (2018 style)
# - halo graphic is not supported
# - this is a work in progress !
# - I try to write this script in a way, so that it works with different resolutions easily
#       --> some code may not look that straight forward because coordinates are not hardcoded
#           but rather calculated based on experimental factors and the selection size
# - in OpenCV x=0, y=0 is at the TOP-LEFT corner!

# ### settings ### #

# define what is considered the beginning of the throttle/break bar
LINEARIZE_THROTTLE_SUM_THRESHOLD = 1500

# set factors to calculate inner/outer radius of throttle/break bars
BAR_OUTER_CIRCLE_FACTOR = 0.3659
BAR_INNER_CIRCLE_FACTOR = 0.311

# ################ #

# selected part of the image; default values
selection = [162, 359, 82]  # x, y, radius

base_image = cv2.imread('testfiles/test5.png', 1)  # input image
video = 'testfiles/test1.mp4'


def set_x_selection(val):
    selection[0] = val


def set_y_selection(val):
    selection[1] = val


def set_selection_size(val):
    selection[2] = val


def select_roi(img):
    cv2.namedWindow('preview', cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow('controls', cv2.WINDOW_NORMAL)

    # create trackbars for circle pos and size
    cv2.createTrackbar('x', 'controls', 0, img.shape[1], set_x_selection)
    cv2.createTrackbar('y', 'controls', 0, img.shape[1], set_y_selection)
    cv2.createTrackbar('size', 'controls', 0, img.shape[0], set_selection_size)
    cv2.imshow('controls', np.zeros((2, 2, 3), np.uint8))

    while True:
        prev_img = np.copy(img)
        cv2.circle(prev_img, (selection[0], selection[1]), selection[2], (0, 0, 255), 1)  # outer circle
        cv2.circle(prev_img, (selection[0], selection[1]), 3, (0, 0, 255), -1)  # center point

        cv2.imshow('preview', prev_img)
        key = cv2.waitKey(1)
        if key == 27:
            accept = False
            break
        elif key == 13:
            accept = True
            break

    cv2.destroyAllWindows()

    return accept


def isolate_throttle_bar(img, size, mask2):
    # mask2 is the mask for label subtraction

    # get different image channels
    b, g, r = cv2.split(img)
    # threshold to get the really green (and white) regions
    ret, thresh = cv2.threshold(g, 130, 255, cv2.THRESH_BINARY)  # was 95 now 115

    # draw a white ring by drawing a white circle and adding a black inner circle
    mask1 = np.zeros((size, size, 1), np.uint8)  # create empty array
    # BAR_*****_CIRCLE_FACTOR are constants to calculate the circle's radius from the img size
    # img, (x, y), radius, (color1,), line_width
    cv2.circle(mask1, (int(size / 2), int(size / 2)), int(round(size * BAR_OUTER_CIRCLE_FACTOR, 0)),
               (255, ), -1)  # white circle
    cv2.circle(mask1, (int(size / 2), int(size / 2)), int(round(size * BAR_INNER_CIRCLE_FACTOR, 0)),
               (0,), -1)  # black inner circle

    # bitwise_and operation with ring and thresholded image
    # results in only those values which are on the ring
    img2 = cv2.bitwise_and(thresh, thresh, mask=mask1)
    img2 = cv2.bitwise_and(img2, img2, mask=mask2)

    # rotate the whole image counterclockwise by 38 degree
    # throttle animation now takes up the left half
    M = cv2.getRotationMatrix2D((size / 2, size / 2), 38, 1)
    img2 = cv2.warpAffine(img2, M, (size, size))
    # by drawing a rectangle over the right half + 4 pixels we get
    # rid of the break graph and other stuff remaining there (just to be sure)
    cv2.rectangle(img2, (int((size / 2) - 4), 0), (size, size), (0,), -1)

    # cv2.imshow('threshold_throttle', img2)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return img2


def linearize_throttle(img, size):
    # this function takes the image of the isolated throttle bar and converts it to a value in percent
    # for this the isolated arc is reduced to a single 1D-Column by summing up each row
    # now it is relatively easy to determine where the top position is by looking for the highest value
    # which is above a certain threshold (LINEARIZE_THROTTLE_SUM_THRESHOLD)
    ############################################

    # sums up all rows, thereby "projecting the arc of the throttle onto the y-axis"
    linear = np.zeros((size, 1))
    for n in range(0, size):
        linear[n] = np.sum(img[n])

    # check for the value which is the furthes "up" i.e. the top end of the graphic bar
    # therefore we iterate throug the 1D Matrix from "top" to "bottom"
    # when a value is non-zero we check whether the sum of the next five is bigger than a threshold
    position = size
    for y in range(4, size, 1):
        if linear[y] != 0:
            if np.sum(linear[y:y+5]) > LINEARIZE_THROTTLE_SUM_THRESHOLD:
                position = y
                break

    # invert pos (i.e. ~y-axis), so that zero is bottom, not top as opencv does it (guess I cant think upside down)
    pos = size - position
    #  !!! keep in mind that these calculations are based on a rotated version of the original graph !!!
    #     -->  see isolate_throttle_bar function
    # rotated by 38 degree counterclockwise so brake/throttle bars end in the center
    # some trigonometric calculations are necessary to get linear values out of the projected arc
    center = int(size / 2)
    highest = center + size * BAR_OUTER_CIRCLE_FACTOR
    lowest = center - size * BAR_OUTER_CIRCLE_FACTOR
    outer_radius = size * BAR_OUTER_CIRCLE_FACTOR
    # inner_radius = size * BAR_INNER_CIRCLE_FACTOR

    # calculates throttle position in percent
    if pos >= highest:
        alpha = np.pi
    elif center < pos < highest:
        # bar is in upper half; calculate angle from zero to pos
        # what we have basically is: y-position on arc (pos), center point, radius
        alpha = np.arcsin((pos-center)/outer_radius) + (np.pi / 2)
    elif pos == center:
        #  exactly center, therefore 50 percent throttle
        alpha = np.pi / 2
    elif lowest < pos < center:
        # bar is in lower half; similar to upper half
        alpha = np.pi / 2 - np.arcsin((center-pos) / outer_radius)
    else:
        alpha = 0

    # calculate percent of maximum angle (180 degree or pi)
    return round(alpha / np.pi * 100, 0), position


def read_throttle(img, size, mask, data, index):
    # this function just combines the execution of two functions
    # allows for easier multithreading
    # (these to need to be done after each other)
    throttle_isolated = isolate_throttle_bar(img, size, mask)
    throttle_value, throttle_pos = linearize_throttle(throttle_isolated, size)

    # debug for printing recognized throttle position in image
    # M = cv2.getRotationMatrix2D((roi_image_size / 2, roi_image_size / 2), 38, 1)
    # roi_img_rot = cv2.warpAffine(roi_img, M, (roi_image_size, roi_image_size))
    # cv2.line(roi_img_rot, (0, throttle_pos), (roi_image_size, throttle_pos), (0, 255, 0), 2)
    # roi_img_rot = cv2.resize(roi_img_rot, (600, 600))
    # cv2.imshow('test', roi_img_rot)
    # cv2.waitKey(30)

    data[index] = throttle_value


def read_brake(img, img_size, data, index):
    # extract a 10x10 pixel region from within the brake bar
    roi_lower = int(img_size / 2 + 0.95 * BAR_OUTER_CIRCLE_FACTOR * img_size * np.sin(np.pi/4))
    roi_left = int(img_size / 2 + 0.95 * BAR_OUTER_CIRCLE_FACTOR * img_size * np.cos(np.pi/4))
    brake_roi = img[roi_lower-10:roi_lower, roi_left:roi_left+10]

    # get the red channel and apply threshold
    blue, green, red = cv2.split(brake_roi)
    ret, red_binary = cv2.threshold(red, 130, 255, cv2.THRESH_BINARY)

    # cv2.imshow('brake', red_binary)
    # cv2.waitKey(30)

    # interpret as breaking if we have at least half of the pixels with non zero value
    if cv2.countNonZero(red_binary) > 50:
        data[index] = 1
    else:
        data[index] = 0


def create_label_masks(img):
    # convert to grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # create one mask and invert it to do ocr on
    ret, ocr_mask = cv2.threshold(gray_img, 150, 255, cv2.THRESH_BINARY)  # 190
    ocr_mask = cv2.bitwise_not(ocr_mask)

    # create a second mask of the labels whithin the diagram to later subtract them from the
    # bars for removing text within them. Because thresholding the bars always leaves
    # the white text, this leads to false detection of the bars position if not subtracting the text
    # this mask is intentionally not very crisp but rather a bit blury to improve subtraction results
    ret, white_only_img = cv2.threshold(gray_img, 135, 255, cv2.THRESH_BINARY)  # 190

    # blure and threshold again to increase the size of the letters in the mask
    # blured = cv2.blur(white_only_img, (1, 1))  # 3, 3
    # ret, blured_white_only = cv2.threshold(blured, 30, 255, cv2.THRESH_BINARY)  # 40
    # invert mask for easier subtraction
    subtraction_mask = cv2.bitwise_not(white_only_img)
    # cv2.imshow('label_mask', subtraction_mask)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return subtraction_mask, ocr_mask


# ## OCR Functions
# info on tesseract settings:
# --psm 8: treat image as single word
# --psm 10: treat image as single character
# -l Formula1: use special training data for F1 font
# -c tessedit_char_whitelist=0123456789 : only allow numbers

def do_ocr_speed(img, data, index):
    ocr_speed_roi = img[int(0.75*roi_image_size):int(0.95*roi_image_size),
                        int(0.3*roi_image_size):int(0.7*roi_image_size)]
    value = pytesseract.image_to_string(ocr_speed_roi,
                                        config='--psm 8 -c tessedit_char_whitelist=0123456789')
    data[index] = value


def do_ocr_rpm(img, data, index):
    ocr_rpm_roi = img[int(0.6*roi_image_size):int(0.7*roi_image_size),
                      int(0.3*roi_image_size):int(0.7*roi_image_size)]

    value = pytesseract.image_to_string(ocr_rpm_roi,
                                        config='--psm 8 -c tessedit_char_whitelist=0123456789')

    # if int(value) > 100000:
    #     cv2.imshow('rpm', ocr_rpm_roi)
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()

    data[index] = value


def do_ocr_gear(img, data, index):
    ocr_gear_roi = img[int(0.35*roi_image_size):int(0.57*roi_image_size),
                       int(0.4*roi_image_size):int(0.6*roi_image_size)]
    value = pytesseract.image_to_string(ocr_gear_roi,
                                        config='--psm 10 -c tessedit_char_whitelist=0123456789')
    data[index] = value


# if not select_roi(base_image):
#     sys.exit()

# create roi image

x1 = selection[0] - selection[2]
x2 = selection[0] + selection[2]
y1 = selection[1] - selection[2]
y2 = selection[1] + selection[2]
roi_image_size = selection[2] * 2  # roi image is always a square so x = y in terms of size

# roi_img = base_image[y1:y2, x1:x2]

cap = cv2.VideoCapture(video)

for i in range(300):
    ret, frame = cap.read()
    # print(i)

# csv_file = open('results/out.csv', "w")

frame_n = 0

while True:
    ret, frame = cap.read()

    if ret:
        roi_img = frame[y1:y2, x1:x2]

        label_subtraction_mask, label_ocr_mask = create_label_masks(roi_img)

        # do recognition threaded
        ocr_values = [0, 0, 0, 0, 0]
        t1 = threading.Thread(target=do_ocr_speed, args=[label_ocr_mask, ocr_values, 0])
        t2 = threading.Thread(target=do_ocr_rpm, args=[label_ocr_mask, ocr_values, 1])
        t3 = threading.Thread(target=do_ocr_gear, args=[label_ocr_mask, ocr_values, 2])
        t4 = threading.Thread(target=read_brake, args=[roi_img, roi_image_size, ocr_values, 3])
        t5 = threading.Thread(target=read_throttle,
                              args=[roi_img, roi_image_size, label_subtraction_mask, ocr_values, 4])
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()
        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()

        speed_value = ocr_values[0]
        rpm_value = ocr_values[1]
        gear_value = ocr_values[2]

        # print(speed_value, throttle_value, brake_value, rpm_value, gear_value)
        #

        # csv_file.write(str(speed_value) + ";"
        #                + str(throttle_value) + ";"
        #                + str(brake_value) + ";"
        #                + str(rpm_value) + ";"
        #                + str(gear_value) + ";"
        #                + str(frame_n) + "\n")
        frame_n += 1
        print(frame_n)

    else:
        break

cv2.destroyAllWindows()
# csv_file.close()
