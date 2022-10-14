import numpy as np
import matplotlib.pyplot as plt

signal_data = np.loadtxt("ECG.dat", unpack = True)
displaying_range = 1000


def createClearSignal():
    time = np.arange(0,10,1/100)
    plt.figure(1)
    plt.plot(time,signal_data[:displaying_range])
    plt.title("Clear Signal")
    plt.xlabel("Time")
    plt.ylabel("Amplitude")


def createNoisySignal(signalToNoiseRatio):
    time = np.arange(0,10,1/100)
    noise = np.random.normal(0,1/signalToNoiseRatio,len(signal_data))
    noisy_signal = signal_data + noise
    plt.figure(2)
    plt.plot(time,noisy_signal[:displaying_range])
    plt.title("Noisy Signal")
    plt.xlabel("Time")
    plt.ylabel("Amplitude")


def createSineWave(amplitude, frequency):
    time = np.arange(0,10,1/100)
    sineWave = amplitude * np.sin(2 * np.pi * frequency * time)
    plt.figure(3)
    plt.plot(time,sineWave)
    plt.title("Sine Wave")
    plt.xlabel("Time")
    plt.ylabel("Amplitude")


def createAddedSignals(amplitude, frequency):
    time = np.arange(0, 10, 1/100)
    sineWave = amplitude * np.sin(2 * np.pi * frequency * time)
    wavesSum = signal_data[:displaying_range] + sineWave
    plt.figure(4)
    plt.plot(time,wavesSum)



createClearSignal()
createNoisySignal(signalToNoiseRatio = 20)
createSineWave(amplitude = 1, frequency = 2)
createAddedSignals(amplitude=0.1, frequency=2)

plt.show()