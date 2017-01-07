
import numpy as np
import matplotlib.pyplot as plt

class myFft:

    def __init__(self,fsHz,plotUnits,numAvg=1):
        self.fs = fsHz
        self.units = plotUnits
        self.numAvg = numAvg
        if (self.units.lower() == 'GHz'.lower()):
          self.range = 1e9
        elif (self.units.lower() == 'MHz'.lower()):
          self.range = 1e6
        elif (self.units.lower() == 'kHz'.lower()):
          self.range = 1e3
        elif (self.units.lower() == 'Hz'.lower()):
          self.range = 1e0
        else:
          print('Error: Invalid units')

    def __crunch(self,data):
        pow2   = int(np.floor(np.log2(data.size)) - np.floor(np.log2(self.numAvg)))
        if pow2 < 1:
            print('Error :Too many averages!')
            return

        NFFT   = 2**pow2
        YSum   = np.zeros(NFFT)
        window = np.hanning(NFFT)

        for ii in range(0,int(2**np.floor(np.log2(self.numAvg)))):
            dataWin = data[ii*NFFT:(ii+1)*NFFT]*window
            Y       = np.abs(np.fft.fft(dataWin,NFFT))/NFFT
            YSum    = YSum + Y**2;
        YAvg = YSum/2**np.floor(np.log2(self.numAvg));

        freq = self.fs/2*np.linspace(0,1,NFFT/2+1)/self.range
        resp = 10*np.log10(YAvg[0:NFFT//2+1])
        return freq,resp

    def plot(self,data):
        """This is a docstring"""
        freq,resp = self.__crunch(data)
        plt.figure()
        plt.plot(freq,resp)
        plt.xlabel(('Freq (' + self.units + ')'))
        plt.ylabel('Amplitude (dB)')
        plt.title('FFT')
        plt.show()
        return freq,resp

# EXAMPLE:
#f = 1000
#t = np.arange(0,1/f*10,1/f/100)
#data = np.sin(2*np.pi*f*t)
#plt.figure()
#plt.plot(t,data)
#plt.draw()
#test = myFft(100e3,'kHz',2)
#freq,dataOut = test.plot(data)
#test2 = myFft(100)
test = myFft(1000,'kHz')