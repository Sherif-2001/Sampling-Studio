import streamlit as st
import pandas as pd
import plost
import numpy as np



st.set_page_config(layout='wide', initial_sidebar_state='expanded')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
st.sidebar.header('Sampling Studio')

st.sidebar.subheader('Opend Shart')
# time_hist_color = st.sidebar.selectbox('Color by') 

st.sidebar.subheader('Created Shart')
donut_theta = st.sidebar.slider('Amplitude', 0,10,1)
donut_theta = st.sidebar.slider('Frequancy',0,100,10 )




st.sidebar.subheader('Final chart parameters')
plot_height = st.sidebar.slider('SNR ', 200, 500, 250)

st.sidebar.markdown('''
---
Created with ❤️ by SBME Students.
''')



