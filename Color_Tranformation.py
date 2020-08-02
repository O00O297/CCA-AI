import cv2
import numpy as np

def color_transfer(MeanTarget, StdTaget, source_img):
    MeanSource, StdSource = cv2.meanStdDev(source_img)

    Ls, As, Bs = cv2.split(source_img)

    l = Ls - MeanSource[0]
    a = As - MeanSource[1]
    b = Bs - MeanSource[2]

    lP = l * (StdTaget[0] / StdSource[0])
    aP = a * (StdTaget[1] / StdSource[1])
    bP = b * (StdTaget[2] / StdSource[2])

    lP += MeanTarget[0]
    aP += MeanTarget[1]
    bP += MeanTarget[2]

    newL = np.clip(lP, 0, 255)
    newA = np.clip(aP, 0, 255)
    newB = np.clip(bP, 0, 255)

    new_img = cv2.merge((newL, newA, newB))
    new_img = cv2.cvtColor(new_img.astype("uint8"), cv2.COLOR_LAB2BGR)

    return new_img
