import streamlit as st
import pandas as pd
import sampling_studio_functions as func
import numpy as np


# ---------------------- Elements styling -------------------------------- #
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# ------------------------- variables ---------------------------------- #
file_as_array = None
uploaded_file = None
# ---------------------- Sidebar Elements -------------------------------- #

# ------------------------------------------------------------------------ #

# # Browsing a file
label_col, Button_col = st.sidebar.columns(2)
with label_col:
    st.markdown("## Upload Signal")
with Button_col:
    file = st.file_uploader(
        "", type="csv", accept_multiple_files=False)

uploaded_file = file
if file is not None:
    file_as_data_frame = pd.read_csv(file).values[:1000]
    file_as_flat_list = [
        item for sublist in file_as_data_frame for item in sublist]
    file_as_array = np.asarray(file_as_flat_list)


# # Add noise to signal
address_col, check_col = st.sidebar.columns(2)
with address_col:
    st.header('Noise')
with check_col:
    noise_flag = st.checkbox("", False)
if noise_flag:
    SNR_slider_value = st.sidebar.slider('SNR', 1, 100, 50)
else:
    SNR_slider_value = 1
# # Add signals to the original signal
st.sidebar.header('Add Signals')

adding_signal_slider_col1, adding_signal_slider_col2 = st.sidebar.columns(2)

with adding_signal_slider_col1:
    added_signal_amplitude = st.slider('Amplitude', 0.0, 1.0, 1.0, 0.01)

with adding_signal_slider_col2:
    added_signal_frequancy = st.slider('Frequency', 0.5, 20.0, 10.0, 0.1)


added_signal_phase = st.sidebar.slider('Phase', 0, 360, 0)


add_signal_button = st.sidebar.button("Add Signal...", key="add")
if add_signal_button:
    func.addSignalToList(added_signal_amplitude,
                         added_signal_frequancy, added_signal_phase)
# ------------------------------------------------------------------------ #

# # Show every signal amplitude and frequency in a select box
selectbox_signals_list = []
for signal in func.getAddedSignalsList():
    selectbox_signals_list.append(
        f"Amp: {signal.amplitude} / Freq: {signal.frequency} / Phase: {round(signal.phase * np.pi)}".format())
selected_signal = st.sidebar.selectbox("Signals", selectbox_signals_list)
selected_signal_split = str(selected_signal).split(" ")
if len(selected_signal_split) != 1:
    amplitude_sub = float(selected_signal_split[1])
    frequency_sub = float(selected_signal_split[4])
    phase_sub = float(selected_signal_split[7])

remove_button_col, clear_button_col = st.sidebar.columns(2)

with remove_button_col:
    remove_signal_button = st.button("Remove")
    if remove_signal_button and len(func.getAddedSignalsList()) > 0:
        func.removeSignalFromList(
            amplitude=amplitude_sub, frequency=frequency_sub, phase=phase_sub)
        st.experimental_rerun()


with clear_button_col:
    clear_signals_button = st.button("Clear")
    if clear_signals_button:
        func.clearAddedSignalsList()
        st.experimental_rerun()

# ------------------------------------------------------------------------ #


# # Sampling
st.sidebar.header('Sampling')
sampling_rate = st.sidebar.slider(
    'Factor Fs/Fmax', 0.5, 10.0, 2.0, 0.5, format="%f")

# ------------------------------------------------------------------------ #

# # Sidebar bottom
st.sidebar.markdown('''
©2022 SBME All rights reserved.
''')
# ----------------------- Main Window Elements --------------------------- #

website_title = '<p class="page_titel">Sampling Studio</p>'
st.markdown(website_title, unsafe_allow_html=True)
func.renderResultedSignal(noise_flag, file_as_array, SNR_slider_value)
# ------------------------------------------------------------------------ #

# st.write("""### Reconstructed Signal""")
fig, Reconstructed_signal = func.renderSampledSignal(sampling_rate)
fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
fig.update_traces(line_color='#EAE3FF')


st.plotly_chart(fig, use_container_width=True)
# ------------------------------------------------------------------------ #


@st.cache
def convert_df(downloaded_df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return downloaded_df.to_csv().encode('utf-8')


csv = convert_df(Reconstructed_signal)

st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='signal.csv',
    mime='text/csv',
)
