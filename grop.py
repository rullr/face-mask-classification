import numpy as np
import cv2

from timed import *


def gres(ttss: np.ndarray, put: np.ndarray, counts: int, th_notifikasi=2.0) -> np.ndarray:  # (BX, BY) ##
    for i in range(len(ttss)):
        rect, ID, cx, cy, class_id = ttss[i]
        print(rect)
        cv2.putText(put, "ID {}".format(ID), (cx - 10, cy - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 2)
        if class_id == 2:
            timer(ID, 'b', 25)
            cv2.rectangle(put, (int(rect[0]), int(rect[1])), (int(
                rect[2]), int(rect[3])), (0, 0, 255), thickness=2)
            cv2.putText(put, 'NoMask', (int(rect[0]), int(
                rect[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        elif class_id == 3:
            timer(ID, 'c', 25)
            cv2.rectangle(put, (int(rect[0]), int(rect[1])), (int(
                rect[2]), int(rect[3])), (23, 230, 210), thickness=2)
            cv2.putText(put, 'ImproperlyMask', (int(rect[0]), int(
                rect[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (23, 230, 210), 2)
        else:
            del_time(ID, 'b')
            del_time(ID, 'c')
            cv2.rectangle(put, (int(rect[0]), int(rect[1])), (int(
                rect[2]), int(rect[3])), (0, 255, 0), thickness=2)
            cv2.putText(put, 'Mask', (int(rect[0]), int(
                rect[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    check_time(th_notifikasi)
    return put
