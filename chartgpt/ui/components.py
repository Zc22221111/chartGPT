import time
import streamlit as st

def tag(key: str, value: str, start: float):
    return st.caption(
        f'<p><span style="color: rgb(21, 130, 55);"><b>{key}</b></span>: {value}, ' + \
        f'<span style="color: rgb(21, 130, 55);"><b>cost</b></span>: {int(time.time() - start)}s</p>',
        unsafe_allow_html=True,
    )