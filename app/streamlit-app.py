
import streamlit as st
import numpy
import sys
import os
import tempfile
sys.path.append(os.getcwd())
import traffic_counter as tc
import cv2 
import time
import utils.SessionState as SessionState
from random import randint
from streamlit import caching
import streamlit.report_thread as ReportThread 
from streamlit.server.server import Server
import copy
from components.custom_slider import custom_slider


# define the weights to be used along with its config file
config =  'darknet/cfg/yolov3.cfg'
wt_file = 'data/yolov3.weights'

# define recommend values for model confidence and nms suppression 
def_values ={'conf': 70, 'nms': 50} 
keys = ['conf', 'nms']

@st.cache(
    hash_funcs={
        st.delta_generator.DeltaGenerator: lambda x: None,
        "_regex.Pattern": lambda x: None,
    },
    allow_output_mutation=True,
)
def load_obj_detector(config, wt_file):
    """
    wrapper func to load and cache object detector 
    """
    obj_detector = tc.ObjectDetector(wt_file, config, confidence = def_values['conf']/100,