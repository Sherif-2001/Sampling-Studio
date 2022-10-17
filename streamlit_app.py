import streamlit as st
import sampling_studio_functions as functions

import streamlit.components.v1 as components


result=(components.html("""
<style>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css"/>

::selection{
  color: #fff;
  background: #6990F2;
}
.wrapper{
  width: 550px;

  border-radius: 5px;
  padding: 30px;
  box-shadow: 7px 7px 12px rgba(0,0,0,0.05);
}
.wrapper header{
  color: #6990F2;
  font-size: 27px;
  font-weight: 600;
  text-align: center;
}
.wrapper form{
  height: 167px;
  display: flex;
  cursor: pointer;
  margin: 30px 0;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  border-radius: 5px;
  border: 2px dashed #6990F2;
}
form :where(i, p){
  color: #6990F2;
}
form i{
  font-size: 50px;
}
form p{
  margin-top: 15px;
  font-size: 16px;
}

.custom-file-input::-webkit-file-upload-button {
  visibility: hidden;
}
.custom-file-input::before {
  content: 'Upload your signal';
  display: inline-block;
 background-color: #6990F2;
  border: 1px solid #999;
  border-radius: 3px;
  padding: 12px 30px;
  outline: none;
  white-space: nowrap;
  cursor: pointer;
  font-weight: 700;
  font-size: 10pt;
  margin-top: 13px;
  margin-left: 40px;
}

    </style>
    <div class="wrapper">
        <form action="#">
        
           <i class="fas fa-cloud-upload-alt"></i>
           <input type="file" class="custom-file-input" name="filename">
          </form>
          
        </form> 
    </div>
  """))

print(result)
st.write(" ##   ")

# # horizontal Menu
# selected = option_menu(None, ["Home", "Upload"], 
#     icons=['house', 'cloud-upload'], 
#     menu_icon="cast", default_index=0, orientation="horizontal")
    
# if selected == 'Upload':
#     uploaded_file = st.file_uploader("Choose a file")
# st.set_page_config(layout='wide', initial_sidebar_state='expanded')

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