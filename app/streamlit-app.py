
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
    hide_streamlit_widgets()
    """
    #  Traffic Flow Counter :blue_car:  :red_car:
    Upload a video file to track and count vehicles. Don't forget to change parameters to tune the model!

    #### Features to be added in the future:
    + speed measurement
    + traffic density
    + vehicle type distribution
    """

    with st.sidebar:
        """
        ## :floppy_disk: Parameters  

        """
        state.conf, state.nms = parameter_sliders(
            keys, state.enabled, value = [state.conf, state.nms])
        
        st.text("")
        st.text("")
        st.text("")

        """
        #### :desktop_computer: [Source code in Github](https://github.com/aldencabajar/traffic_flow_counter)

        """

    #set model confidence and nms threshold 
    if (state.conf is not None):
        obj_detector.confidence = state.conf/ 100
    if (state.nms is not None):
        obj_detector.nms_threshold = state.nms/ 100 



    upload = st.empty()
    start_button = st.empty()
    stop_button = st.empty()

    with upload:
        f = st.file_uploader('Upload Video file (mpeg/mp4 format)', key = state.upload_key)
    if f is not None:
        tfile  = tempfile.NamedTemporaryFile(delete = True)
        tfile.write(f.read())

        upload.empty()
        vf = cv2.VideoCapture(tfile.name)

        if not state.run:
            start = start_button.button("start")
            state.start = start
        
        if state.start:
            start_button.empty()
            #state.upload_key = str(randint(1000, int(1e6)))
            state.enabled = False
            if state.run:
                tfile.close()
                f.close()
                state.upload_key = str(randint(1000, int(1e6)))
                state.enabled = True
                state.run = False
                ProcessFrames(vf, tracker, obj_detector, stop_button)
            else:
                state.run = True
                trigger_rerun()



def hide_streamlit_widgets():
    """
    hides widgets that are displayed by streamlit when running
    """
    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

def ProcessFrames(vf, tracker, obj_detector,stop): 
    """
        main loop for processing video file:
        Params
        vf = VideoCapture Object
        tracker = Tracker Object that was instantiated 
        obj_detector = Object detector (model and some properties) 
    """

    try:
        num_frames = int(vf.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(vf.get(cv2.CAP_PROP_FPS)) 
        print('Total number of frames to be processed:', num_frames,
        '\nFrame rate (frames per second):', fps)
    except:
        print('We cannot determine number of frames and FPS!')


    frame_counter = 0
    _stop = stop.button("stop")
    new_car_count_txt = st.empty()
    fps_meas_txt = st.empty()
    bar = st.progress(frame_counter)