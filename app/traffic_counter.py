
import numpy as np
import cv2
import os
import time
import sys
import palettable
import tqdm
import copy

# load labels from COCO dataset
LABELS = open('darknet/data/coco.names').read().strip().split('\n')

class ObjectDetector:
    def __init__(self, weights, config, confidence, nms_threshold):
        self.net = cv2.dnn.readNetFromDarknet(config, weights)
        self.confidence = confidence
        self.nms_threshold = nms_threshold 

        # identify layers
        ln = self.net.getLayerNames() 
        self.ln = [ln[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

    def ForwardPassOutput(self, frame):
        # create a blob as input to the model
        H, W = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1/255., (416, 416), swapRB=True, crop = False)

        # predict using model
        self.net.setInput(blob)
        layerOutputs = self.net.forward(self.ln)

        # initialize lists for the class, width and height 
        # and x,y coords for bounding box

        class_lst = []
        boxes = []
        confidences = []

        for output in layerOutputs:
            for detection in output:
                # do not consider the frst five values as these correspond to 
                # the x-y coords of the center, width and height of the bounding box,
                # and the objectness score
                scores = detection[5:]

                # get the index with the max score
                class_id = np.argmax(scores)
                conf = scores[class_id]

                if conf >= self.confidence:
                    # scale the predictions back to the original size of image
                    box = detection[0:4] * np.array([W,H]*2) 
                    (cX, cY, width, height) = box.astype(int)

                    # get the top and left-most coordinate of the bounding box
                    x = int(cX - (width / 2))
                    y = int(cY - (height / 2))

                    #update list
                    boxes.append([int(i) for i in [x, y, width, height]])
                    class_lst.append(class_id)
                    confidences.append(float(conf))
        #apply non maximum suppression which outputs the final predictions 
        idx = np.array(cv2.dnn.NMSBoxes(boxes, confidences, self.confidence, self.nms_threshold)).flatten()
        return [LABELS[class_lst[i]] for i in idx], [boxes[i] for i in idx], [confidences[i] for i in idx]


def drawBoxes(frame, labels, boxes, confidences):
    boxColor = (128, 255, 0) # very light green
    TextColor = (255, 255, 255) # white
    boxThickness = 3 
    textThickness = 2

    for lbl, box, conf in zip(labels, boxes, confidences):
        start_coord = tuple(box[:2])
        w, h = box[2:]
        end_coord = start_coord[0] + w, start_coord[1] + h

    # text to be included to the output image
        txt = '{} ({})'.format(', '.join([str(i) for i in DetermineBoxCenter(box)]), round(conf,3))
        frame = cv2.rectangle(frame, start_coord, end_coord, boxColor, boxThickness)
        frame = cv2.putText(frame, txt, start_coord, cv2.FONT_HERSHEY_SIMPLEX, 0.5, TextColor, 2)

    return frame

def DetermineBoxCenter(box):
    cx = int(box[0] + (box[2]/2))
    cy = int(box[1] + (box[3]/2))

    return [cx, cy]