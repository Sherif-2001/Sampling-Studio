import streamlit as st
import sampling_studio_functions as func

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# # # Sidebar Elements

# # Sidebar header
website_title = '<p class="page_titel">Sampling Studio</p>'
st.sidebar.markdown(website_title, unsafe_allow_html=True)
# st.sidebar.header('Sampling Studio')

# # Browsing a file
st.sidebar.file_uploader('')

# # line break 
st.sidebar.markdown("***")

# time_hist_color = st.sidebar.selectbox('Color by') 

# # Add signals to the origin signal
st.sidebar.header('Add Signals')

adding_col1, adding_col2= st.sidebar.columns(2)

with adding_col1:
    sine_amplitude = st.slider('Amplitude', 0.0,1.0,1.0,0.01)

with adding_col2:
    sine_frequancy = st.slider('Frequency',0.5,20.0,10.0,0.1)

add_signal_button = st.sidebar.button("Add Signal...",key="add")

if add_signal_button:
    func.addSignals(sine_amplitude, sine_frequancy)

# # Show every signal amplitude and frequency (last signal will be deleted if you click the button twice)
for signal in func.added_signals_list:
    st.sidebar.text(f"Amplitude: {signal.amplitude}, Frequency: {signal.frequency}")
    remove_button = st.sidebar.button("Remove",key=f"{func.added_signals_list.index(signal)}")
    if remove_button:
        func.removeSignals(signal)

# # line break 
st.sidebar.markdown("***")

# # Add noise to signal
st.sidebar.header('Noise')
noise_flag = st.sidebar.checkbox("Add Noise", False)
if noise_flag:
    SNR = st.sidebar.slider('SNR', 1, 50, 25)
else:
    SNR = 0

# # line break 
st.sidebar.markdown("***")

# # Sampling
st.sidebar.header('Sampling')
sampling_rate = st.sidebar.slider('Sampling Frequency (Fs)', 10, 500,100)

# # Sidebar bottom
st.sidebar.markdown('''
---
Created with ❤️ by SBME Students
''')

# # # Main Window Elements

st.write("""### Signal""")
if noise_flag:
    noisy_signal=func.generateNoisySignal(SNR)
    st.line_chart(noisy_signal, x='Time', y='Amplitude')
else:
    signal=func.generateClearSignal()
    st.line_chart(signal, x='Time', y='Amplitude')

# # line break
st.markdown("***")

# st.write("""### Generated Sine Wave""")
# generated_sine = functions.generateSineWave(sine_amplitude, sine_frequancy)
# st.line_chart(generated_sine)

st.write("""### Resulted Signal""")
st.line_chart(func.added_signals, x='Time', y='Amplitude')

# # line break
st.markdown("***")

st.write("""### Reconstructed Signal""")
# print(functions.generateSampledSignal(fs))
st.line_chart(func.generateSampledSignal(sampling_rate))