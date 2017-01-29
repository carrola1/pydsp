import numpy as np

class QtrRateDwnCvt():
    """
    Designer:       Andrew Carroll

    Description:    Implements Quarter Rate Down Converter. Multiplies input 
                        by sin/cos waveforms of frequency = 1/4*fSamp.
    
    Attributes:     None
                    
    Methods:        update(sampIn):     Apply Qtr Rate function to input
                    clear():            Reset sin/cos phases
    """
    def __init__(self):
        self.cosPhase = np.array([1,0,-1,0])
        self.sinPhase = np.array([0,1,0,-1])

    def update(self,sampIn):
        """
        Description:    Apply Qtr Rate function to input

        Params:         sampIn:     New input sample

        Returns:        iOut:       Input*cos(phase)
                        qOut:       Input*sin(phase)
        """
        iOut = sampIn*self.cosPhase[0]
        qOut = sampIn*self.sinPhase[0]
        self.cosPhase = np.roll(self.cosPhase,-1)
        self.sinPhase = np.roll(self.sinPhase,-1)
        return iOut,qOut

    def clear(self):
        """
        Description:    Reset sin/cos phases

        Params:         None

        Returns:        None
        """
        self.cosPhase = np.array([1,0,-1,0])
        self.sinPhase = np.array([0,1,0,-1])

"""
# EXAMPLE:
from fft import Fft
fSamp = 1000
fSig = 100
t = np.arange(0,1/fSig*10,1/fSamp)
sig = np.sin(2*np.pi*fSig*t)
test = QtrRateDwnCvt()
newSigI = np.zeros(sig.size)
newSigQ = np.zeros(sig.size)
for ii in range(0,sig.size):
    newSigI[ii],newSigQ[ii] = test.update(sig[ii])
fftObj = Fft(1000,'Hz')
fftObj.plot(newSigI)
"""