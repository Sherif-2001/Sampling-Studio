import streamlit as st
import pandas as pd
import sampling_studio_functions as func
import numpy as np

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# ---------------------- Sidebar Elements -------------------------------- #

# # Sidebar header
website_title = '<p class="page_titel">Sampling Studio</p>'
st.sidebar.markdown(website_title, unsafe_allow_html = True)
# st.sidebar.header('Sampling Studio')

# ------------------------------------------------------------------------ #

# # Browsing a file
uploaded_file = st.sidebar.file_uploader("", type="csv", accept_multiple_files = False)


# ------------------------------------------------------------------------ #

# # line break
st.sidebar.markdown("***")

# ------------------------------------------------------------------------ #

# # Add noise to signal
st.sidebar.header('Noise')
noise_flag = st.sidebar.checkbox("Add Noise", False)
if noise_flag:
    SNR_slider_value = st.sidebar.slider('SNR', 1, 100, 50)
else:
    SNR_slider_value = 1

# ------------------------------------------------------------------------ #

# # line break
st.sidebar.markdown("***")

# ------------------------------------------------------------------------ #

# # Add signals to the original signal
st.sidebar.header('Add Signals')

adding_col1, adding_col2 = st.sidebar.columns(2)

with adding_col1:
    signal_amplitude = st.slider('Amplitude', 0.0, 1.0, 1.0, 0.01)

with adding_col2:
    signal_frequancy = st.slider('Frequency', 0.5, 20.0, 10.0, 0.1)


signal_phase = st.sidebar.slider('Phase', 0, 360, 0)


add_signal_button = st.sidebar.button("Add Signal...", key="add")
if add_signal_button:
    func.addSignalToList(signal_amplitude, signal_frequancy, signal_phase)

# ------------------------------------------------------------------------ #

# # Show every signal amplitude and frequency in a select box
Options = []
for signal in func.getAddedSignalsList():
    Options.append(f"Amp: {signal.amplitude} / Freq: {signal.frequency} / Phase: {signal.phase*180/np.pi}")
selected_signal = st.sidebar.selectbox("Signals", Options)
selected_signal_arr = str(selected_signal).split(" ")
if len(selected_signal_arr) != 1:
    amplitude_sub = float(selected_signal_arr[1])
    frequency_sub = float(selected_signal_arr[4])
    phase_sub = float(selected_signal[7])

remove_signal_button = st.sidebar.button("Remove")
if remove_signal_button and len(func.getAddedSignalsList()) > 0:
    func.removeSignalFromList(amplitude=amplitude_sub, frequency=frequency_sub,phase=phase_sub)

# ------------------------------------------------------------------------ #

# # line break
st.sidebar.markdown("***")

# ------------------------------------------------------------------------ #

# # Sampling
st.sidebar.header('Sampling')
if uploaded_file is not None:
    max_freq = st.sidebar.number_input('Fmax',150)
else:
    max_freq = 1
sampling_rate = st.sidebar.slider('Factor Fs/Fmax', 0.5, 10.0,2.0,0.5)

# ------------------------------------------------------------------------ #

# # Sidebar bottom
st.sidebar.markdown('''
---
Created with ❤️ by SBME Students
''')

# ----------------------- Main Window Elements --------------------------- #

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.write("""### Uploaded Signal""")
    
    if uploaded_file is None:
        st.line_chart(func.getSignalData(uploaded_file))
    else:
        uploaded_signal = pd.read_csv(uploaded_file)["Amplitude"][:1000]
        st.line_chart(uploaded_signal)

with chart_col2:
    st.write("""### Generated Sine Wave""")
    generated_sine = func.renderGeneratedSignal(signal_amplitude, signal_frequancy, signal_phase)
    st.line_chart(generated_sine)

# ------------------------------------------------------------------------ #

st.write("""### Resulted Signal""")
st.line_chart(func.renderResultedSignal(noise_flag,uploaded_file, SNR_slider_value))

# ------------------------------------------------------------------------ #

st.write("""### Reconstructed Signal""")
fig,Reconstructed_signal = func.renderSampledSignal(sampling_rate, max_freq)
st.plotly_chart(fig,use_container_width=True)

# ------------------------------------------------------------------------ #

@st.cache
def convert_df(df): 
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

csv = convert_df(Reconstructed_signal)

st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='Reconstructed_signal.csv',
    mime='text/csv',
)

