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
  InitialValue: num