from matplotlib.pyplot import grid
import numpy as np
import pandas as pd
from signal_class import Signal
import plotly_express as px
from scipy import signal


# ------------------------ Variables --------------------------- #
default_signal_time = np.arange(0,0.5,0.0005)

generated_signal = 1 * np.sin(2 * np.pi * 2 * default_signal_time)

resulted_signal = None

added_signals_list = []
# ------------------------ Modifying Functions --------------------------- #

def generateNoise(SNR, uploaded_signal):
    """
        Generate noise according to the SNR

        Parameters
        ----------
        SNR : float
            Signal to Noise Ratio
        uploaded_signal : array of float
            the uploaded signal if exists

        Return
        ----------
        noise : array of float
            Generated noise
    """

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
    """
        Generate sinusoidal wave

        Parameters
        ----------
        amplitude : float
            the amplitude of the signal
        frequency : float
            the frequancy of the signal
        phase : float
            the phase of the signal

        Return
        ----------
        sine_signal : dataframe of generated signal
            dataframe of generated signal
    """

    sineWave = amplitude * np.sin(2 * np.pi * frequency * default_signal_time + phase*np.pi/180)
    sine_signal = pd.DataFrame(sineWave, default_signal_time)
    return sine_signal

# ------------------------------------------------------------------------ #

def renderResultedSignal(is_noise_add, uploaded_signal, SNR = 100):
    """
        Render the resulted signal

        Parameters
        ----------
        is_noise_add : boolean
            add noise or not
        uploaded_signal : array of float
            the uploaded signal if exists
        SNR : int
            signal to noise ratio

        Return
        ----------
        result_signal df : dataframe
            dataframe of resulted signal
    """

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

def interpolate(time_new, signal_time, signal_amplitude):
    """
        Sinc Interpolation

        Parameters
        ----------
        time_new : array of float
            new time to smple at
        signal_time : array of float
            samples of time
        signal_amplitude : array of float
            amplitudes at signal_time 

        Return
        ----------
        new_Amplitude : array of float
            new amplitudes at time_new
    """

    # Find the period
    T = signal_time[1] - signal_time[0]

    # sinc interpolation
    sincM = np.tile(time_new, (len(signal_time), 1)) - np.tile(signal_time[:,np.newaxis], (1, len(time_new)))
    new_Amplitude = np.dot(signal_amplitude, np.sinc(sincM/T))
    

    return  new_Amplitude

  
# ------------------------------------------------------------------------ #
def renderSampledSignal(nyquist_rate):
    """
        render sampled and interpolated signal

        Parameters
        ----------
        nyquist_rate : float
            F_sample/F_max
        

        Return
        ----------
        fig : Figure
            plot of the interpolated sampled signal
        downloaded_df : Dataframe
            the resulted signal to be downloaded
    """

    step_size = default_signal_time[1] - default_signal_time[0]
    
    f, t, Sxx = signal.spectrogram(resulted_signal, 1/step_size, return_onesided=False)

    f_max = np.argmax(f)

    time = np.arange(0,0.5,1/(nyquist_rate*f_max))

    ynew = interpolate(time, default_signal_time, resulted_signal)

    y_inter = interpolate(default_signal_time, time, ynew)

    #Plot
    df=pd.DataFrame(default_signal_time, y_inter)
    fig = px.scatter(x=time,y=ynew,  labels={
                     "x": "Time (s)",
                     "y": "Amplitude (mv)"
                 },
                title="Resulted Signal"
                  ,color_discrete_sequence=['#4558E8']
                )
    fig.update_traces(marker={'size': 6})

    fig.add_scatter(x=default_signal_time, y=y_inter)
    
    fig.update_layout(showlegend=False)
    fig.update_xaxes(showline=True, linewidth=2, linecolor='black', gridcolor='#5E5E5E')
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black', gridcolor='#5E5E5E')
    
  
    
    return  fig,df.drop(df.columns[[0]],axis = 1)

# ------------------------------------------------------------------------ #

def addSignalToList(amplitude, frequency, phase):
    """
        Add signals to added_list

        Parameters
        ----------
        amplitude : float
            the amplitude of the signal
        frequency : float
            the frequancy of the signal
        phase : float
            the phase of the signal        
    """

    added_signals_list.append(Signal(amplitude = amplitude, frequency = frequency, phase =  phase*np.pi/180))

# ------------------------------------------------------------------------ #

def removeSignalFromList(amplitude, frequency, phase):
    """
        remove signals from added_list

        Parameters
        ----------
        amplitude : float
            the amplitude of the signal
        frequency : float
            the frequancy of the signal
        phase : float
            the phase of the signal        
    """

    for added_signal in added_signals_list:
        if added_signal.amplitude == amplitude and added_signal.frequency == frequency and round(added_signal.phase / np.pi*180)  ==  phase :
            added_signals_list.remove(added_signal)
            return

# ---------------------------- Getter functions -------------------------- #

def getSignalData(uploaded_signal):
    """
        get the main signal data

        Parameters
        ----------
        uploaded_signal : array of float
            the uploaded signal if exists

        Return
        ----------
        df : dataframe
            dataframe of the main signal
           
    """
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

def getTime():
    return default_signal_time

# ------------------------------------------------------------------------ #

def setGeneratedSignal(amplitude, frequency, phase):
    """
        set the generated signal

        Parameters
        ----------
        amplitude : float
            the amplitude of the signal
        frequency : float
            the frequancy of the signal
        phase : float
            the phase of the signal   
    """
    global generated_signal
    generated_signal = amplitude * np.sin(2 * np.pi * frequency * default_signal_time +  phase*np.pi/180 )

