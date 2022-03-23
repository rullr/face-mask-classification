import argparse
import cv2
import numpy as np
import time
import PySimpleGUI as sg

from tracker import TRACKER
from grop import *
from forms import *

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="Video path, stream URI, or camera ID ",
                    default="videos/video_test.mp4")
parser.add_argument("-t", "--threshold", type=float,
                    default=0.3, help="Minimum score to consider")
parser.add_argument("-m", "--mode", choices=['detection'],
                    help="Either detection or tracking mode", default='detection')

args = parser.parse_args()
curr_pnts = []
rois_shps = []
ct = TRACKER()

if args.input.isdigit():
    args.input = int(args.input)

BOX_COLOR = (23, 230, 210)
TEXT_COLOR = (255, 255, 255)
INPUT_SIZE = (224, 224)
TRACKED_CLASSES = ['Mask', 'NoMask', 'ImproperlyMask']

# Read Faster R-CNN model
config = "./trained_weight/graph.pbtxt"
model = "./trained_weight/pb.pb"
detector = cv2.dnn.readNetFromTensorflow(model, config)

imgs = np.ndarray
sgmi = np.ndarray

ix = -1
iy = -1
coor = []
drag = False


def getMouseDrag(event, x, y, flags, param):
    global ix, iy, drag, imgs, sgmi
    if event == cv2.EVENT_LBUTTONDOWN:
        drag = True
        ix = x
        iy = y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drag == True:
            img2 = sgmi.copy()
            cv2.rectangle(img2, (ix, iy), (x, y), (255, 0, 0), 5)
            imgs = img2

    elif event == cv2.EVENT_LBUTTONUP:
        drag = False
        img2 = sgmi.copy()
        cv2.rectangle(img2, (ix, iy), (x, y), (255, 0, 0), 5)
        imgs = img2
        coor.append([2*ix, 2*iy, 2*x, 2*y])


def illustrate_detections(dets: np.ndarray, frame: np.ndarray, counts: int, th_notifikasi) -> np.ndarray:
    bbs_objects_ids = []
    bbs_ids = {}
    boxeds = []
    objects = {}

    class_ids, scores, boxes = dets[:, 0], dets[:, 1], dets[:, 2:6]

    for class_id, score, box in zip(class_ids, scores, boxes):
        box2D = box.reshape((2, 2)) * np.array([rois_shps[1], rois_shps[0]])
        box1D = box2D.reshape(-1)

        bbs_objects_ids.append(box1D)
        boxeds.append((box1D, class_id))

    objects = ct.update(bbs_objects_ids)
    ttss = forms(boxeds, objects.items())

    put = gres(ttss, frame, counts, th_notifikasi)
    return put


cap = cv2.VideoCapture(args.input)
font = cv2.FONT_HERSHEY_PLAIN
times = time.time()

cv2.namedWindow("roi", cv2.WINDOW_NORMAL)
cv2.resizeWindow("roi", 960, 540)
cv2.setMouseCallback("roi", getMouseDrag)


def main():
    sg.theme("Dark Amber 5")
    counts = 0
    layout = [
        [sg.Text("Demo", size=(60, 1), justification="center")],
        [sg.Image(filename="", key="-IMAGE-")],
        [
            sg.Text("Notifikasi (Detik)", size=(
                40, 1), justification="center"),
            sg.Slider(
                (1, 5),
                3,
                0.5,
                orientation="h",
                size=(40, 15),
                key="-Notifikasi-",
            ),
        ],
        [sg.Button("Exit", size=(10, 1))],
    ]

    window = sg.Window("Monitoring Pemakaian Masker",
                       layout, location=(450, 150))

    while True:
        ret, frame = cap.read()

        if counts == 0:
            global sgmi, imgs
            imgs = cv2.resize(frame, (960, 540))
            sgmi = cv2.resize(frame, (960, 540))
            while True:
                cv2.imshow("roi", imgs)
                cv2.waitKey(1)
                if len(coor) != 0:
                    cv2.destroyWindow("roi")
                    break
                first_frame_display = False

        event, values = window.read(timeout=20)
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        roi = frame[coor[0][1]:coor[0][3], coor[0][0]:coor[0][2]]
        cv2.rectangle(frame, (coor[0][0], coor[0][1]), (coor[0][2], coor[0][3]), color=(
            255, 0, 0), thickness=3)
        rois_shps.append(roi.shape[0])
        rois_shps.append(roi.shape[1])

        pict = roi
        detector.setInput(cv2.dnn.blobFromImage(
            pict, size=INPUT_SIZE, swapRB=True, crop=False))
        detections = detector.forward()[0, 0, :, 1:]
        scores = detections[:, 1]
        detections = detections[scores > 0.3]

        timet = time.time() - times
        fps = counts/timet
        cv2.putText(frame, "FPS" + str(round(fps, 2)),
                    (10, 50), font, 2, (255, 0, 0), 2)

        if len(detections) != 1:
            run = illustrate_detections(detections, roi, counts, float(values["-Notifikasi-"]))
            frame[coor[0][1]:coor[0][3], coor[0][0]:coor[0][2]] = run
            cv2.putText(frame, "FE {}".format(counts), (1800, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, TEXT_COLOR, 1)

        counts += 1

        resized_image = cv2.resize(frame, (640, 480))
        imgbytes = cv2.imencode(".png", resized_image)[1].tobytes()
        window["-IMAGE-"].update(data=imgbytes)

    window.close()


main()
