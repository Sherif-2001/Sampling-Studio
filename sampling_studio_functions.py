import numpy as np
import pandas as pd
from scipy import interpolate
from signal_class import Signal
# import plotly_express as px

display_range=1000
signal_data = pd.read_csv("ecg_data.csv")[:display_range]
signal_time = signal_data["Time"]
signal_amplitude = signal_data["Amplitude"]
maximum_frequency = np.fft.fft(signal_data).max()
sampling_frequency = 2 * maximum_frequency

added_signals = signal_data.copy()
added_signals_list = []

def generateClearSignal():
    return signal_data


def generateNoisySignal(SNR):
    noisy_data = signal_data.copy()
    power= noisy_data["Amplitude"] ** 2
    signal_average_power= np.mean(power)
    signal_average_power_db = 10 * np.log10(signal_average_power)
    noise_db = signal_average_power_db - SNR
    noise_watts = 10 ** (noise_db/10)

    noise = np.random.normal(0,np.sqrt(noise_watts),len(noisy_data))
    
    noisy_data["Amplitude"] += noise
    return noisy_data


def generateSineWave(amplitude, frequency):
    time = np.arange(0,10,1/100)
    sineWave = amplitude * np.sin(2 * np.pi * frequency * time)
    sineWave_data = pd.DataFrame(sineWave,time)
    return sineWave_data


def addSignals(amplitude, frequency):
    sineWave = amplitude * np.sin(2 * np.pi * frequency * signal_time)
    added_signals_list.append(Signal(amplitude=amplitude,frequency=frequency))
    # if noise_flag:
    #     added_signals["Amplitude"] += (generateNoisySignal(SNR=SNR)["Amplitude"] + sineWave)
    # else:
    added_signals["Amplitude"] += sineWave
    print(len(added_signals_list))
    return added_signals

def generateSampledSignal(sampling_frequency):

    func = interpolate.interp1d(signal_data["Time"], signal_data["Amplitude"],kind='quadratic')
    time = np.arange(0,0.5,1/sampling_frequency)
    ynew = func(time)
   
    # Ts = 1/sampling_frequency
    # sampled_signal = signal_data[:-1:round(Ts*1000)]
    return pd.DataFrame(ynew,time)


def removeSignals(signal):
    removed_signal = signal.amplitude * np.sin(2 * np.pi * signal.frequency * signal_time)
    added_signals_list.remove(signal)
    added_signals["Amplitude"] -= removed_signal