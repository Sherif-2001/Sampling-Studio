import streamlit as st
from sampling_studio_functions import createClearSignal, createNoisySignal, createSineWave, createAddedSignals

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
st.sidebar.header('Sampling Studio')

st.sidebar.subheader('Opened Chart')
# time_hist_color = st.sidebar.selectbox('Color by') 

st.sidebar.subheader('Created Sine Wave')
sine_amplitude = st.sidebar.slider('Amplitude', 0.0,1.0,1.0,0.01)
sine_frequancy = st.sidebar.slider('Frequancy',0.5,100.0,10.0,0.1 )




st.sidebar.subheader('SignaltoNoiseRatio')
noise_flag = st.sidebar.checkbox("Add Noise",False)
SNR = st.sidebar.slider('SNR% ', 1, 100, 1)

st.sidebar.markdown('''
---
Created with ❤️ by SBME Students.
''')


st.write("""### Opened ECG Signal""")
if noise_flag:
    noisy_signal=createNoisySignal(SNR/100)
    st.line_chart(noisy_signal)
else:
    signal=createClearSignal()
    st.line_chart(signal)

st.write("""### Generated Sine Wave""")
generated_sine = createSineWave(sine_amplitude, sine_frequancy)
st.line_chart(generated_sine)

st.write("""### Resulted Signal""")
result_signal = createAddedSignals(sine_amplitude, sine_frequancy)
st.line_chart(result_signal)
