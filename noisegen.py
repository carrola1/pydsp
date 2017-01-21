import numpy as np

class AWGN():
    ''' 
    Designer:       Andrew Carroll

    Description:    Additive white gaussian noise generator
    
    Attributes:     rmsSig:     RMS of signal
                    snr:        Target SNR (dB)
                    
    Methods:        getSampPlusN(sampIn):   Add noise to input sample
                    getArrPlusN(arrIn):     Add noise to input array
    '''
    def __init__(self,rmsSig,snr):
        self.sigmaN = rmsSig/10**(snr/20)

    def addNoise(self,sampsIn):
        '''
        Description:    Add noise to input sample or array

        Params:         sampsIn:    Input sample (float)

        Returns:        sampsOut:   Output sample(s) with noise added (float)
        '''
        sampsOut = sampsIn + np.random.normal(0,self.sigmaN,sampsIn.size)
        return sampsOut

    def getNoise(self,numSamps):
        '''
        Description:    Get noise samples from gaussian distribution

        Params:         numSamps:   # of noise samples to return

        Returns:        sampsOut:   Output sample or array
        '''
        sampsOut = np.random.normal(0,self.sigmaN,numSamps)
        return sampsOut


# EXAMPLE:
import matplotlib.pyplot as plt
from fft import Fft
fs = 100
t = np.arange(0,1/fs*800,1/fs/100)
sig = np.sin(2*np.pi*fs*t)
test = AWGN(.70710678,10)
sigN = test.addNoise(sig)
plt.figure(1)
plt.plot(t[0:500],sig[0:500],'r',t[0:500],sigN[0:500],'b')
tFft = Fft(10000,'Hz',8,'none')
freq,amp = tFft.plot(sigN)
freqUnit = freq[1]-freq[0]
snr = np.max(amp) - np.mean(amp[int(freq.size/2):]) - 10*np.log10(5000/freqUnit)
print(snr)
plt.show()

