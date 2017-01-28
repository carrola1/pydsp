import numpy as np

class MovAvg:
    ''' 
    Designer:       Andrew Carroll

    Description:    Implements moving average filter. Functions in sample or
                    array based modes.
    
    Attributes:     length: length of moving average filter
    
    Methods:        update(newVal): Update filter buf and return new output
                    clear():        Clear filter buffer
                    calc(data):     Return filtered data array
    '''
    def __init__(self, length):
        self.length = length
        self.__buf = np.zeros(length)

    def update(self,newVal):
        '''
        Description:    Update filter buffer and return new filter output.
    
        Params:         newVal:     New data sample
        
        Returns:        filtData:   Filter output sample
        '''
        self.__buf[1:] = self.buf__[0:-2]
        self.__buf[0] = newVal
        return sum(self.__buf)/self.length

    def clear(self):
        '''
        Description:    Clear filter buffer (zeros)
    
        Params:         None
        
        Returns:        None
        '''
        self.__buf = np.zeros(self.length)

    def calc(self,data):
        '''
        Description:    Implement moving average filter on input data array.
    
        Params:         data:       Input data array to be filtered
        
        Returns:        filtData:   Filter output array (same size as input)
        '''
        self.clear()
        filtData = np.zeros(data.size)
        for ii in range(0,data.size):
            self.__buf[1:] = self.__buf[0:-1]
            self.__buf[0] = data[ii]
            filtData[ii] = sum(self.__buf)/self.length
        return filtData

'''
# EXAMPLE:
import matplotlib.pyplot as plt
f = 1000
t = np.arange(0,1/f*10,1/f/100)
data = np.sin(2*np.pi*f*t)
filtObj1 = MovAvg(20)
filtData1 = filtObj1.calc(data)
filtObj2 = MovAvg(43)
filtData2 = filtObj2.calc(data)
plt.figure()
plt.plot(t,data,'r',t,filtData1,'b',t,filtData2,'c')
plt.show()
'''