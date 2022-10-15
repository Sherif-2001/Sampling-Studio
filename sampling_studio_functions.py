import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd

signal_data = pd.read_csv("ecg_data.csv")
signal_time = signal_data["Time"]
signal_amplitude = signal_data["Amplitude"]
maximum_frequency = np.fft.fft(signal_data).max()
sampling_frequency = 2 * maximum_frequency

noisy_data = pd.read_csv("ecg_data.csv")


def generateClearSignal():
    return signal_data


def generateNoisySignal(noise_ratio):
    noise = np.random.normal(0,noise_ratio,len(noisy_data))
    noisy_data["Amplitude"] += noise
    return noisy_data

def generateSineWave(amplitude, frequency):
    time = np.arange(0,10,1/100)
    sineWave = amplitude * np.sin(2 * np.pi * frequency * time)
    sineWave_data = pd.DataFrame(sineWave,time)
    return sineWave_data


def addSignals(amplitude, frequency,noise_flag,noise_ratio = 0.0001):
    sineWave = amplitude * np.sin(2 * np.pi * frequency * signal_time)
    signal_copy = signal_data.copy()
    if noise_flag:
        signal_copy["Amplitude"] = generateNoisySignal(noise_ratio=noise_ratio)["Amplitude"] + sineWave
    else:
        signal_copy["Amplitude"] += sineWave
    return signal_copy

def generateSampledSignal():
    fs = 35
    Ts = 1/fs
    # sig = signal_data.loc[signal_data['Time'][i] % Ts == 0 for i in range(len(signal_data))]
    # plt.plot(sig)
