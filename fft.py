
import numpy as np
import matplotlib.pyplot as plt

class Fft:
    """
    Designer:       Andrew Carroll

    Description:    Calculates and optionally plots fft of input data set in dB.  
                    Does not zero pad. Divides input array up into numAvg  
                    sections, calcs fft of each and averages. Uses hann window.
    
    Attributes:     data:   Input data array
                    fs:     Sampling rate (Hz)
                    units:  String input for desired freq units on plot
                                ('GHz','MHz','kHz','Hz')
                    numAvg: (*Optional) # of spectrums to average 
                                Must be power of 2. Default = 1.
                    window: (*Optional) Windowing function. Supports 'hanning'
                                or 'none'. Default = 'hanning' 
    
    Methods:        plot(data): Calculates FFT and generates plot
                    calc(data): Calculates FFT  
    """
    def __init__(self,fsHz,plotUnits,numAvg=1,window='hanning'):
        self.fs = fsHz
        self.units = plotUnits
        self.numAvg = numAvg
        if (self.units.lower() == 'GHz'.lower()):
          self.__range = 1e9
        elif (self.units.lower() == 'MHz'.lower()):
          self.__range = 1e6
        elif (self.units.lower() == 'kHz'.lower()):
          self.__range = 1e3
        elif (self.units.lower() == 'Hz'.lower()):
          self.__range = 1e0
        else:
          print('Error: Invalid units')

        if ((window.lower() == 'hanning'.lower()) |
                (window.lower() == 'hann'.lower())):
            self.__window = 'hann'
        else:
            self.__window = 'none'
        

    def setWindow(self,window):
        """
        Description:    Set window function.
    
        Params:         window: Windowing function. Supports 'hanning or 'none'
        
        Returns:        None 
        """
        if ((window.units.lower() == 'hanning') |
                (window.units.lower() == 'hann')):
            self.__window = 'hann'
        else:
            self.__window = 'none'
        return

    def __crunch(self,data):
        pow2 = int(np.floor(np.log2(data.size)) - 
                    np.floor(np.log2(self.numAvg)))
        if pow2 < 1:
            print('Error: Too many averages!')
            return

        nfft   = 2**pow2
        ySum   = np.zeros(nfft)
        if (self.__window == 'hann'):
            window = np.hanning(nfft)
        else:
            window = np.ones(nfft)

        for ii in range(0,int(2**np.floor(np.log2(self.numAvg)))):
            dataWin = data[ii*nfft:(ii+1)*nfft]*window
            Y = np.abs(np.fft.fft(dataWin,nfft))/nfft
            ySum += Y**2;
        yAvg = ySum/2**np.floor(np.log2(self.numAvg));

        freq = self.fs/2*np.linspace(0,1,nfft/2)/self.__range
        resp = 10*np.log10(yAvg[0:nfft//2])
        return freq,resp

    def plot(self,data):
        """
        Description:    Calculates and plots fft of input data set in dB.
    
        Params:         data: input data array
        
        Returns:        freq: frequency array in 'units'
                        resp: FFT calculation (dB) 
        """
        freq,resp = self.__crunch(data)
        plt.figure()
        plt.plot(freq,resp)
        plt.xlabel(('Freq (' + self.units + ')'))
        plt.ylabel('Amplitude (dB)')
        plt.title('FFT')
        plt.show()
        return freq,resp

    def calc(self,data):
        """
        Description:    Calculates and returns fft of input data set in dB.
    
        Params:         data: input data array
        
        Returns:        freq: frequency array in 'units'
                        resp: FFT calculation (dB) 
        """
        freq,resp = self.__crunch(data)
        return freq,resp    

"""
# EXAMPLE:
f = 1000
t = np.arange(0,1/f*10,1/f/100)
data = np.sin(2*np.pi*f*t)
plt.figure()
plt.plot(t,data)
plt.draw()
test = Fft(100e3,'kHz',2)
freq,dataOut = test.plot(data)
"""