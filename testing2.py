import streamlit as st
import os

text = st.text_area(value = "Hello, World", label="Enter text here!")

if st.button("click here"):
    print(type(text))
    st.write("asdsa")