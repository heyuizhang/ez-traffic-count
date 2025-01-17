# EZ Traffic Count :vertical_traffic_light:

## Introduction
Hello everyone! This repository houses a work-in-progress application for traffic flow counting designed with urban traffic flow management in mind. It uses the `yolo-v3` computer vision model to detect and track vehicles.

## Setup
To run the application locally, install the necessary python packages with the following command: 

```python
pip install -r requirements.txt
```

For better reproducibility, we recommend setting up a python environment using `virtualenv` or any similar package. 

The app includes a custom slider. To use it, you need to have `npm` installed, and then run the following commands.

```bash
cd components/custom_slider/frontend/
npm install 
```

Subsequently, run `npm run build`

This will recreate the build package for the custom slider. 

Download the necessary models and data by running: 

```
make dependencies 
```

To launch the app, type:

```
streamlit run app/streamlit-app.py
```

## Future Developments
We have many ideas for enhancements to the API, including: 

+ Speed measurement
+ Vehicle distribution measurement
+ Tracking traffic density