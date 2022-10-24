import numpy as np
import pandas as pd
from signal_class import Signal
import plotly_express as px


# ------------------------ Variables --------------------------- #
default_signal_time = np.arange(0,1,0.001)

default_signal = 1 * np.sin(2 * np.pi * 1 * default_signal_time) 
f_max = 1

resulted_signal = None

added_signals_list = []

uploaded_signals_list = []
# ------------------------ Modifying Functions --------------------------- #

def set_signal_time(Fs):
    global default_signal_time, f_max
    default_signal_time = np.arange(0,1000*1/Fs,1/Fs) 
    f_max = Fs/2 

def generateNoise(SNR):
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

    temp_signal = resulted_signal
    SNR_db = 10 * np.log10(SNR)
    power = temp_signal ** 2
    signal_average_power= np.mean(power)
    signal_average_power_db = 10 * np.log10(signal_average_power)
    noise_db = signal_average_power_db - SNR_db
    noise_watts = 10 ** (noise_db/10)

    noise = np.random.normal(0,np.sqrt(noise_watts), len(temp_signal))
    return noise

# ------------------------------------------------------------------------ #
def generateResultedSignal(is_noise_add, uploaded_signal, SNR = 1):
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
        temp_resulted_signal = uploaded_signal.copy()
    else:
        temp_resulted_signal = default_signal.copy()

    for signal in added_signals_list:
        temp_resulted_signal += signal.amplitude * np.sin(2 * np.pi * signal.frequency * default_signal_time + signal.phase * np.pi)

    global resulted_signal
    if is_noise_add:
        resulted_signal = temp_resulted_signal + generateNoise(SNR)
    else:
        resulted_signal = temp_resulted_signal
    return pd.DataFrame(resulted_signal, default_signal_time)


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
    return new_Amplitude
  
# ------------------------------------------------------------------------ #

def renderSampledSignal(nyquist_rate, normalized_sample_flag):
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
    global f_max
    if normalized_sample_flag:

        
        time = np.arange(0,default_signal_time[-1],1/(nyquist_rate*f_max))
    else:
        time = np.arange(0,default_signal_time[-1],1/(nyquist_rate))


    ynew = interpolate(time, default_signal_time, resulted_signal)

    y_inter = interpolate(default_signal_time, time, ynew)

    #Plot
    df = pd.DataFrame(default_signal_time, y_inter)
    fig = px.scatter(
                    x = time,
                    y = ynew,
                    labels={"x": "Time (s)","y": "Amplitude (mv)"},
                    title="Resulted Signal",
                    color_discrete_sequence=['#4558E8']
        )

    fig.add_scatter(x=default_signal_time, y=y_inter)

    fig.update_traces(marker = {'size': 6})
    fig.update_layout(showlegend=False,margin=dict(l=0, r=0, t=0, b=0),autosize = True)
    fig.update_xaxes(showline=True, linewidth=2, linecolor='black', gridcolor='#5E5E5E', title_font = dict(size=24, family='Arial'))
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black', gridcolor='#5E5E5E',title_font = dict(size=24, family='Arial'))
    
    return  fig, df.drop(df.columns[[0]],axis = 1)

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
    global f_max

    added_signals_list.append(Signal(amplitude = amplitude, frequency = frequency, phase = phase))
    f_max = max(f_max,frequency)

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

    for signal in added_signals_list:
        if signal.amplitude == amplitude and signal.frequency == frequency and signal.phase == phase:
            added_signals_list.remove(signal)
            return
# ------------------------------------------------------------------------ #

def clearAddedSignalsList():
    added_signals_list.clear()

# ---------------------------- Getter functions -------------------------- #

# def getSignalData(uploaded_signal):
#     """
#         get the main signal data

#         Parameters
#         ----------
#         uploaded_signal : array of float
#             the uploaded signal if exists

#         Return
#         ----------
#         df : dataframe
#             dataframe of the main signal
           
#     """
#     if uploaded_signal is not None:
#         return pd.DataFrame(uploaded_signal, default_signal_time)
#     else:
#         return pd.DataFrame(default_signal, default_signal_time)

# ------------------------------------------------------------------------ #

def getAddedSignalsList():
    return added_signals_list

# ------------------------------------------------------------------------ #

# def getTime():
#     return default_signal_time

# ------------------------------------------------------------------------ #

# def setGeneratedSignal(amplitude, frequency, phase):
#     """
#         set the generated signal

#         Parameters
#         ----------
#         amplitude : float
#             the amplitude of the signal
#         frequency : float
#             the frequancy of the signal
#         phase : float
#             the phase of the signal   
#     """
#     global default_signal
#     generated_signal = amplitude * np.sin(2 * np.pi * frequency * default_signal_time +  phase*np.pi/180 )

def getResultedSignal(signal):
    return signal