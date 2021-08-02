
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