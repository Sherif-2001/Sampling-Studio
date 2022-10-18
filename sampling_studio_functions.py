import numpy as np
import pandas as pd
from scipy import interpolate
from signal_class import Signal
# import plotly_express as px

# ------------------------ Variables --------------------------- #

display_range=1000
signal_data = pd.read_csv("ecg_data.csv")[:display_range]
signal_time = signal_data["Time"]
signal_amplitude = signal_data["Amplitude"]

# maximum_frequency = np.fft.fft(signal_data).max()
# sampling_frequency = 2 * maximum_frequency

added_signals_list = []


# ------------------------ Modifying Functions --------------------------- #

def generateNoisySignal(SNR):
    SNR_db = 10*np.log10(SNR)
    power = signal_data["Amplitude"] ** 2
    signal_average_power= np.mean(power)
    signal_average_power_db = 10 * np.log10(signal_average_power)
    noise_db = signal_average_power_db - SNR_db
    noise_watts = 10 ** (noise_db/10)

    noise = np.random.normal(0,np.sqrt(noise_watts),len(signal_data))
    noisy_data = signal_data["Amplitude"] + noise
    return pd.DataFrame(noisy_data)

# ------------------------------------------------------------------------ #

# def generateSineWave(amplitude, frequency):
#     time = np.arange(0, 10, 1/100)
#     sineWave = amplitude * np.sin(2 * np.pi * frequency * time)
#     sine_wave_data = pd.DataFrame(sineWave, time)
#     return sine_wave_data

# ------------------------------------------------------------------------ #

def drawAddedSignals(noise_flag, SNR = 100):
    clear_added_signal = signal_data.copy()
    noisy_added_signal = generateNoisySignal(SNR = SNR)
    for signal in added_signals_list:
        clear_added_signal["Amplitude"] += (signal.amplitude * np.sin(2 * np.pi * signal.frequency * signal_time))
        noisy_added_signal["Amplitude"] += (signal.amplitude * np.sin(2 * np.pi * signal.frequency * signal_time))
    if noise_flag:
        return noisy_added_signal
    else:
        return clear_added_signal

# ------------------------------------------------------------------------ #

def generateSampledSignal(sampling_frequency):
    func = interpolate.interp1d(signal_data["Time"], signal_data["Amplitude"],kind='quadratic')
    time = np.arange(0,0.5,1/sampling_frequency)
    ynew = func(time)
   
    # Ts = 1/sampling_frequency
    # sampled_signal = signal_data[:-1:round(Ts*1000)]
    return pd.DataFrame(ynew,time)

# ------------------------------------------------------------------------ #

def addSignal(amplitude, frequency):
    added_signals_list.append(Signal(amplitude = amplitude, frequency = frequency))

# ------------------------------------------------------------------------ #

def removeSignal(amplitude,frequency):
    for added_signal in added_signals_list:
        if added_signal.amplitude == amplitude and added_signal.frequency == frequency:
            added_signals_list.remove(added_signal)
            return

# ---------------------------- Getter functions -------------------------- #

def getClearSignal():
    return signal_data

# ------------------------------------------------------------------------ #

def getAddedSignalsList():
    return added_signals_list