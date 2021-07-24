
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
     nms_threshold=def_values['nms']/100)

    return obj_detector
    
    

def parameter_sliders(key, enabled = True, value = None):
    conf = custom_slider("Model Confidence", 
                        minVal = 0, maxVal = 100, InitialValue= value[0], enabled = enabled,
                        key = key[0])
    nms = custom_slider('Overlapping Threshold', 
                        minVal = 0, maxVal = 100, InitialValue= value[1], enabled = enabled,
                        key = key[1])

        
    return(conf, nms)


def trigger_rerun():
    """
    mechanism in place to force resets and update widget states
    """
    session_infos = Server.get_current()._session_info_by_id.values() 
    for session_info in session_infos:
        this_session = session_info.session
    this_session.request_rerun()

def main():
    st.set_page_config(page_title = "Traffic Flow Counter", 
    page_icon=":vertical_traffic_light:")

    obj_detector = load_obj_detector(config, wt_file)
    tracker = tc.CarsInFrameTracker(num_previous_frames = 10, frame_shape = (720, 1080))

    state = SessionState.get(upload_key = None, enabled = True, 
    start = False, conf = 70, nms = 50, run = False)