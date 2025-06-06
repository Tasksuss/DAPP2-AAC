import streamlit as st
from PIL import Image

image = Image.open('https://github.com/Tasksuss/DAPP2-AAC/blob/main/streamlit_demo/device_cad_model.jpg')

st.image(image, use_column_width=True)
