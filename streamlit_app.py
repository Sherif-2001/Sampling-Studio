import streamlit as st
import pandas as pd
import sampling_studio_functions as func
import numpy as np
import librosa, librosa.display

# ---------------------- Elements styling -------------------------------- #
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# ------------------------- variables ---------------------------------- #
file_as_array = None
# ---------------------- Sidebar Elements -------------------------------- #

# # Browsing a file
label_col, Button_col = st.sidebar.columns(2)
with label_col:
    st.markdown("## Upload Signal")
with Button_col:
    file = st.file_uploader(
        "", type="wav", accept_multiple_files=False)

if file is not None:
    file_wav = librosa.load(file)
    # print(file_wav)
    # file_as_data_frame = pd.read_csv(file).values[:1000]
    # file_as_flat_list = [
    #     item for sublist in file_wav for item in sublist]
    file_as_array = np.asarray(file_wav[0])[:1000]
    func.set_signal_time(file_wav[1])

# ------------------------------------------------------------------------ #
st.sidebar.markdown("***")
# ------------------------------------------------------------------------ #

# # Add noise to signal
noise_label_col, noise_checkbox_col = st.sidebar.columns(2)
with noise_label_col:
    st.header('Noise')
with noise_checkbox_col:
    noise_flag = st.checkbox("", False)
if noise_flag:
    SNR_slider_value = st.sidebar.slider('SNR', 1, 100, 50)
else:
    SNR_slider_value = 1

# ------------------------------------------------------------------------ #
st.sidebar.markdown("***")
# ------------------------------------------------------------------------ #

# # Add signals to the original signal
st.sidebar.header('Add Signals')

signal_amplitude_slider_col1, signal_frequency_slider_col2 = st.sidebar.columns(2)

with signal_amplitude_slider_col1:
    signal_amplitude_slider = st.slider(
        'Amplitude', 0.0, 1.0, 1.0, 0.01, format="%f")

with signal_frequency_slider_col2:
    signal_frequancy_slider = st.slider(
        'Frequency', 0.5, 20.0, 10.0, 0.1, format="%f")

signal_phase_slider = st.sidebar.slider(
    'Phase', 0.0, 2.0, 0.0, 0.1, format="%fπ")

add_signal_button = st.sidebar.button("Add Signal...", key="add_button")
if add_signal_button:
    func.addSignalToList(signal_amplitude_slider, signal_frequancy_slider, signal_phase_slider)
             
# ------------------------------------------------------------------------ #

# # add signals to the selectbox
selectbox_signals_list = []
for signal in func.getAddedSignalsList():
    selectbox_signals_list.append(
        f"Amp: {signal.amplitude} / Freq: {signal.frequency} / Phase: {signal.phase :.1f} π")
selected_signal = st.sidebar.selectbox("Signals", selectbox_signals_list)
selected_signal_split = str(selected_signal).split(" ")
if len(selected_signal_split) != 1:
    amplitude_slider = float(selected_signal_split[1])
    frequency_slider = float(selected_signal_split[4])
    phase_slider = float(selected_signal_split[7])

# # Remove and clear signals from selectbox
remove_button_col, clear_button_col = st.sidebar.columns(2)
with remove_button_col:
    remove_signal_button = st.button("Remove",key="remove_button",disabled=len(func.getAddedSignalsList()) <= 0)
    if remove_signal_button:
        func.removeSignalFromList(amplitude = amplitude_slider, frequency = frequency_slider, phase = phase_slider)
        st.experimental_rerun()

with clear_button_col:
    clear_signals_button = st.button("Clear",key="clear_button",disabled=len(func.getAddedSignalsList()) <= 0)
    if clear_signals_button:
        func.clearAddedSignalsList()
        st.experimental_rerun()

# ------------------------------------------------------------------------ #
st.sidebar.markdown("***")
# ------------------------------------------------------------------------ #

# # Sampling
st.sidebar.header('Sampling')
sampling_rate = st.sidebar.slider(
    'Factor Fs/Fmax', 0.5, 10.0, 2.0, 0.5, format="%f")

# ------------------------------------------------------------------------ #
st.sidebar.markdown("***")
# ------------------------------------------------------------------------ #

# # Sidebar bottom
st.sidebar.markdown('''© 2022 SBME All rights reserved.''')

# ----------------------- Main Window Elements --------------------------- #

website_title = '<p class="page_titel", style="font-family:Arial">Sampling Studio</p>'
st.markdown(website_title, unsafe_allow_html=True)
# ------------------------------------------------------------------------ #

# st.write("""### Reconstructed Signal""")
func.generateResultedSignal(noise_flag, file_as_array, SNR_slider_value)
fig, Reconstructed_signal = func.renderSampledSignal(sampling_rate)
# fig.update_traces(line_color='#EAE3FF')

st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------------------------------ #

@st.cache
def convert_df(downloaded_df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return downloaded_df.to_csv().encode('utf-8')

csv = convert_df(Reconstructed_signal)

st.download_button(
    label="Download data as CSV",
    data = csv,
    file_name = 'signal.csv',
    mime = 'text/csv',
)