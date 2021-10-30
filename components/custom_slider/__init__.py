import os
import streamlit.components.v1 as components

root_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(root_dir, 'frontend/build')

# Toggle between dev and production mode
_RELEASE = True

if _RELEASE:
    _component_func = components.declare_component(
        "custom_slider",
        path = build_dir
    )


else:
    _component_func = components.declare_component(
        "custom_slider",
        url="http://localhost:3001",
    )


def custom_slider(label: str, minVal: int, maxVal: int, enabled: bool,  
                    InitialValue: int = 0, key = None):
    return(_component_func(label = label, minVal = minVal, maxVal = maxVal,
                              enabled = enabled, InitialValue= InitialValue, key = key))


# Add some t