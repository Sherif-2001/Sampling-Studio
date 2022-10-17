import streamlit as st
import sampling_studio_functions as functions




with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


# Sidebar header
st.sidebar.header('Sampling Studio')
st.sidebar.file_uploader('')
# Browsing a file

# time_hist_color = st.sidebar.selectbox('Color by') 

st.sidebar.subheader('Generate Sine Wave')
sine_amplitude = st.sidebar.slider('Amplitude', 0.0,1.0,1.0,0.01)
sine_frequancy = st.sidebar.slider('Frequancy',0.5,20.0,10.0,0.1)

st.sidebar.subheader('Generate Noise')
noise_flag = st.sidebar.checkbox("Add Noise To Signal",False)
SNR = st.sidebar.slider('SNR', 1, 50, 1)

fs = st.sidebar.slider('fs ', 10, 500,100)

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