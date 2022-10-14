import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd

signal_data = np.loadtxt("ECG.dat", unpack = True)
displaying_range = 1000


def createClearSignal():
    signaData=pd.DataFrame(signal_data)
    return signaData[:displaying_range]


def createNoisySignal(signalToNoiseRatio):
    noise = np.random.normal(0,signalToNoiseRatio,len(signal_data))
    noisy_signal = signal_data + noise
    noisy_data=pd.DataFrame(noisy_signal)
    return noisy_data[:displaying_range]


def createSineWave(amplitude, frequency):
    time = np.arange(0,10,1/100)
    sineWave = amplitude * np.sin(2 * np.pi * frequency * time)
    sineWave_data = pd.DataFrame(sineWave,time)
    return sineWave_data


def createAddedSignals(amplitude, frequency):
    time = np.arange(0, 10, 1/100)
    sineWave = amplitude * np.sin(2 * np.pi * frequency * time)
    wavesSum = signal_data[:displaying_range] + sineWave
    return pd.DataFrame(wavesSum,time)

