import numpy as np
from typing import OrderedDict


def forms(boxeds: np.ndarray, ordis: OrderedDict) -> np.array:
    arra = []

    for (ID, centroid) in ordis:
        for (boxed, class_id) in boxeds:
            cX = int((boxed[0] + boxed[2]) / 2.0)
            cY = int((boxed[1] + boxed[3]) / 2.0)
            if cX == centroid[0] and cY == centroid[1]:
                arra.append([boxed, ID, centroid[0], centroid[1], class_id])
    return np.array(arra)
