import numpy as np
import pandas as pd
from signal_class import Signal
import plotly_express as px
from scipy import signal


# ------------------------ Variables --------------------------- #
default_signal_time = np.arange(0,0.5,0.0005)

generated_signal = 1 * np.sin(2 * np.pi * 1 * default_signal_time)
resulted_signal = None

added_signals_list = []

# signal_time = uploaded_signal_data["Time"]
# signal_amplitude = signal_data["Amplitude"]

# maximum_frequency = np.fft.fft(signal_data).max()
# sampling_frequency = 2 * maximum_frequency


# ------------------------ Modifying Functions --------------------------- #

def generateNoise(SNR, uploaded_signal):
    if uploaded_signal is not None:
        temp_data = uploaded_signal
    else:
        temp_data = generated_signal.copy()
    SNR_db = 10 * np.log10(SNR)
    power = temp_data ** 2
    signal_average_power= np.mean(power)
    signal_average_power_db = 10 * np.log10(signal_average_power)
    noise_db = signal_average_power_db - SNR_db
    noise_watts = 10 ** (noise_db/10)

    noise = np.random.normal(0,np.sqrt(noise_watts), len(temp_data))
    return noise

# ------------------------------------------------------------------------ #

def renderGeneratedSignal(amplitude, frequency, phase):
    sineWave = amplitude * np.sin(2 * np.pi * frequency * default_signal_time + phase*np.pi/180)
    sine_signal = pd.DataFrame(sineWave, default_signal_time)
    return sine_signal

# ------------------------------------------------------------------------ #

def renderResultedSignal(is_noise_add, uploaded_signal, SNR = 100):
    if uploaded_signal is not None:
        temp_clear_resulted_signal = uploaded_signal
        temp_noisy_resulted_signal = uploaded_signal + generateNoise(SNR, uploaded_signal)
    else:
        temp_clear_resulted_signal = generated_signal.copy()
        temp_noisy_resulted_signal = generated_signal.copy() + generateNoise(SNR, uploaded_signal)

    for signal in added_signals_list:
        temp_clear_resulted_signal += signal.amplitude * np.sin(2 * np.pi * signal.frequency * default_signal_time + signal.phase * np.pi/180)
        temp_noisy_resulted_signal += signal.amplitude * np.sin(2 * np.pi * signal.frequency * default_signal_time + signal.phase * np.pi/180)       

    global resulted_signal
    if is_noise_add:
        resulted_signal = temp_noisy_resulted_signal
        return pd.DataFrame(temp_noisy_resulted_signal, default_signal_time)
    else:
        resulted_signal = temp_clear_resulted_signal
        return pd.DataFrame(temp_clear_resulted_signal, default_signal_time)

# ------------------------------------------------------------------------ #

def Interpolate(time_new, signal_time, signal_amplitude):

    # Find the period
    T = signal_time[1] - signal_time[0]

    # sinc interpolation
    sincM = np.tile(time_new, (len(signal_time), 1)) - np.tile(signal_time[:,np.newaxis], (1, len(time_new)))
    ynew = np.dot(signal_amplitude, np.sinc(sincM/T))
    

    return  ynew

  
# ------------------------------------------------------------------------ #
def renderSampledSignal(factor):
    n_sample = len(default_signal_time)
    
    f, t, Sxx = signal.spectrogram(resulted_signal, 1/0.0005, return_onesided=False)

    f_max = np.argmax(f)
    print(f_max)

    time = np.arange(0,0.5,1/(factor*f_max))

    ynew = Interpolate(time, default_signal_time, resulted_signal)

    y_inter = Interpolate(default_signal_time, time, ynew)

    #Plot
    df=pd.DataFrame(default_signal_time, y_inter)
    fig = px.scatter(x=time,y=ynew,  labels={
                     "index": "Time (s)",
                     "value": "Amplitude (mv)"
                 },
                title="Resulted Signal")
    fig.add_scatter(x=default_signal_time, y=y_inter)
    
    # fig.update_traces(marker=dict(color="crimson"))  
    
    return  fig,df.drop(df.columns[[0]],axis = 1)

# ------------------------------------------------------------------------ #

def addSignalToList(amplitude, frequency, phase):
    added_signals_list.append(Signal(amplitude = amplitude, frequency = frequency, phase =  phase*np.pi/180))

# ------------------------------------------------------------------------ #

def removeSignalFromList(amplitude, frequency, phase):
    for added_signal in added_signals_list:
        if added_signal.amplitude == amplitude and added_signal.frequency == frequency and round(added_signal.phase / np.pi*180)  ==  phase :
            added_signals_list.remove(added_signal)
            return

# ---------------------------- Getter functions -------------------------- #

def getSignalData(uploaded_signal):
    if uploaded_signal is not None:
        return pd.DataFrame(uploaded_signal, default_signal_time)
    else:
        return pd.DataFrame(generated_signal, default_signal_time)

# ------------------------------------------------------------------------ #

def getAddedSignalsList():
    return added_signals_list


# ------------------------------------------------------------------------ #

def clearAddedSignalsList():
    added_signals_list.clear()

# ------------------------------------------------------------------------ #

def setGeneratedSignal(amplitude, frequency, phase):
    global generated_signal
    generated_signal = amplitude * np.sin(2 * np.pi * frequency * default_signal_time +  phase*np.pi/180 )

