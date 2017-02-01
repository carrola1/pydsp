import numpy as np

class AGC:
    """
    Designer:       Andrew Carroll

    Description:    Implements Automatic Gain Control algorithm. Calculates
                    standard deviation of input and sets gain to target
                    probability of numSigma samples lie within +/- fullScale.
                    Clamps output at +/- fullScale. 
    
    Attributes:     bufLength:  # of samples used to calc new gain value
                    fullScale:  Output full scale (assumes +/-)
                    numSigma:   (*optional) # of std dev to fall within +/- 
                                    fullScale. Default = 2 (95%).
    
    Methods:        update(samp):   Update AGC object with new sample
                    clear():        Clear buffer and gain
                    calc(data):     Apply AGC to data array
    """

    def __init__(self,bufLength,fullScale,numSigma=2):
        self.numSigma = numSigma
        self.fullScale = fullScale
        self.buf = np.zeros(bufLength)
        self.bufCnt = 0
        self.gain = 1

    def update(self,samp):
        """
        Description:    Update AGC object with new sample
    
        Params:         samp:       New data sample
        
        Returns:        sampOut:    Output sample with gain applied
        """
        self.buf = np.roll(self.buf,1)
        self.buf[0] = samp
        if (self.bufCnt == self.buf.size-1):
            self.gain = self.fullScale/(np.std(self.buf)*self.numSigma)
            self.bufCnt = 0
        else:
            self.bufCnt += 1
        sampOut = np.clip(samp*self.gain,-self.fullScale,self.fullScale)
        return sampOut

    def clear(self):
        """
        Description:    Clear AGC buffer and gain
    
        Params:         None
        
        Returns:        None
        """
        self.bufCnt = 0
        self.buf = np.zeros(self.buf.size)
        self.gain = 1

    def calc(self,data):
        """
        Description:    Apply AGC to data array
    
        Params:         data:       Input data array
        
        Returns:        dataOut:    Output data with gain applied
        """
        dataOut = np.zeros(data.size)
        self.clear()
        for ii in range(0,data.size):
            self.buf = np.roll(self.buf,1)
            self.buf[0] = data[ii]
            if (self.bufCnt == self.buf.size-1):
                self.gain = self.fullScale/(np.std(self.buf)*self.numSigma)
                self.bufCnt = 0
            else:
                self.bufCnt += 1
            dataOut[ii] = np.clip(data[ii]*self.gain,-self.fullScale,
                            self.fullScale)
        return dataOut

"""
# EXAMPLE:
import matplotlib.pyplot as plt
from noisegen import AWGN
f = 1000
t = np.arange(0,1/f*100,1/f/100)
data = np.sin(2*np.pi*f*t)
nGen = AWGN(.7071,-5)
dataN = nGen.addNoise(data)
z = AGC(200,4)
dataZ = z.calc(dataN)
# Calc % of clipped samples (will come out as 5% if SNR is low (mostly noise))
cnt = 0
for ii in range(0,dataZ.size):
    if ((dataZ[ii] == 4) | (dataZ[ii] == -4)):
        cnt += 1
print(cnt/dataZ.size*100)
plt.figure()
plt.plot(t[0:500],dataN[0:500],'r',t[0:500],dataZ[0:500],'b')
plt.show()
"""
