import streamlit as st
import sampling_studio_functions as functions
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components


result=(components.html("""
  <input type="text" id="fname" name="fname" value="John"> 
  """))

print(result)
st.write(" ##   ")

# # horizontal Menu
selected = option_menu(None, ["Home", "Upload"], 
    icons=['house', 'cloud-upload'], 
    menu_icon="cast", default_index=0, orientation="horizontal")
    
if selected == 'Upload':
    uploaded_file = st.file_uploader("Choose a file")
# st.set_page_config(layout='wide', initial_sidebar_state='expanded')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Sidebar header
st.sidebar.header('Sampling Studio')

# Browsing a file
st.sidebar.subheader('Opened Chart')
# time_hist_color = st.sidebar.selectbox('Color by') 

st.sidebar.subheader('Generate Sine Wave')
sine_amplitude = st.sidebar.slider('Amplitude', 0.0,1.0,1.0,0.01)
sine_frequancy = st.sidebar.slider('Frequancy',0.5,20.0,10.0,0.1)

st.sidebar.subheader('Generate Noise')
noise_flag = st.sidebar.checkbox("Add Noise To Signal",False)
SNR = st.sidebar.slider('SNR', 1, 50, 1)

fs = st.sidebar.slider('fs ', 20, 300,100)

st.sidebar.markdown('''
---
Created with ❤️ by SBME Students.
''')

st.write("""### ECG Signal""")
if noise_flag:
    noisy_signal=functions.generateNoisySignal(SNR)
    st.line_chart(noisy_signal,x='Time',y='Amplitude')
else:
    signal=functions.generateClearSignal()
    st.line_chart(signal,x='Time',y='Amplitude')

st.write("""### Generated Sine Wave""")
generated_sine = functions.generateSineWave(sine_amplitude, sine_frequancy)
st.line_chart(generated_sine)

st.write("""### Resulted Signal""")
result_signal = functions.addSignals(sine_amplitude, sine_frequancy,noise_flag,SNR)
st.line_chart(result_signal,x='Time',y='Amplitude')

st.write("""### Reconstructed Signal""")
# print(functions.generateSampledSignal(fs))
st.line_chart(functions.generateSampledSignal(fs))