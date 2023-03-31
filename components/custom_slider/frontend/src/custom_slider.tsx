import { Slider, withStyles, styled } from "@material-ui/core"
import { 
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection
} from "streamlit-component-lib";
import React, { ReactNode } from "react";

interface pythonArgs {
  label: string
  minVal: number
  maxVal: number
  InitialValue: number
  enabled: boolean


}

const styles = {
  color: "#f0f2f6",
  stPrimary: "#f63366",
};

const StyledSlider = withStyles({
  root: {
    color: styles.stPrimary,
    background: styles.color,
    marginTop: 15,
    marginLeft: 15,
    width: 265,

  },
  thumb: {
    height: 24,
    width: 24,
    backgroundColor: '#fff',
    border: '2px solid currentColor',
    marginTop: -8,
    marginLeft: -12,
    '&:focus,&:hover,&$active': {
      boxShadow: 'inherit',
    },
  },
  active: {},
  valueLabel: {
    left: 'calc(-50% + 4px)',
  },
  track: {
    height: 3