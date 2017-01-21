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

    def getSampPlusN(self,sampIn):
        '''
        Description:    Add noise to input sample

        Params:         sampIn: Input sample (float)

        Returns:        sampOut: Output sample with noise added (float)
        '''
        sampOut = sampIn + np.random.normal(0,self.sigmaN)
        return sampOut

    def getArrPlusN(self,arrIn):
        '''
        Description:    Add noise to input array

        Params:         sampIn: Input array (float)

        Returns:        sampOut: Output array with noise added (float)
        '''
        arrOut = arrIn + np.random.normal(0,self.sigmaN,arrIn.size)
        return arrOut

'''
# EXAMPLE:
import matplotlib.pyplot as plt
from fft import Fft
fs = 100
t = np.arange(0,1/fs*800,1/fs/100)
sig = np.sin(2*np.pi*fs*t)
test = AWGN(.70710678,10)
sigN = test.getArrPlusN(sig)
plt.figure(1)
plt.plot(t,sig,'r',t,sigN,'b')
tFft = Fft(10000,'Hz',8,'none')
freq,amp = tFft.plot(sigN)
freqUnit = freq[1]-freq[0]
snr = np.max(amp) - np.mean(amp[int(freq.size/2):]) - 10*np.log10(5000/freqUnit)
print(snr)
plt.draw()
'''
