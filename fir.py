import numpy as np

class FIR:
    ''' 
    Designer:       Andrew Carroll

    Description:    Implements FIR filter.
    
    Attributes:     taps:       Filter taps
                    length:     Length of filter
                    shiftReg:   Filter shift register
    
    Methods:        update(newVal): Update filter buffer and return new output
                    clear():        Clear filter shift register
                    calc(data):     Return filtered data array
    '''

    def __init__(self, taps):
        self.taps = taps
        self.length = taps.size
        self.shiftReg = np.zeros(self.length)

    def update(self,samp):
        '''
        Description:    Update filter buffer and return new filter output.
    
        Params:         samp:           New data sample
        
        Returns:        filtSamp:       Filter output sample
        '''
        self.shiftReg = np.roll(self.shiftReg,1)
        self.shiftReg[0] = samp
        filtSamp = sum(self.shiftReg*self.taps)
        return filtSamp

    def clear(self):
        '''
        Description:    Clear filter shift register (zeros)
    
        Params:         None
        
        Returns:        None
        '''
        self.shiftReg = np.zeros(self.length)

    def calc(self,data):
        '''
        Description:    Applies FIR filter to input data array.
    
        Params:         data:       Input data array to be filtered
        
        Returns:        filtData:   Filtered data of same size as input 
        '''
        filtData = np.zeros(data.size)
        self.clear()
        for ii in range(0,data.size):
            self.shiftReg = np.roll(self.shiftReg,1)
            self.shiftReg[0] = data[ii]
            filtData[ii] = sum(self.shiftReg*self.taps)
        return filtData

'''
# EXAMPLE:
import matplotlib.pyplot as plt
f = 1000
t = np.arange(0,1/f*10,1/f/100)
data = np.sin(2*np.pi*f*t)
filt = FIR(np.ones(50)*(1/50))
dataFilt = filt.calc(data)
plt.figure()
plt.plot(t,data,'r',t,dataFilt)
plt.show()
'''
