import numpy as np

class IntDump:
    ''' 
    Designer:       Andrew Carroll

    Description:    Implements integrate and dump filter. Functions in samples 
                    or array based modes.
    
    Attributes:     length:         Length of moving average filter
                    dumpCnt:        Dump counter (counts samples)
    
    Methods:        update(newVal): Update filter buffer and return new output
                    clear():        Clear filter buffer
                    calc(data):     Return filtered data array
    '''
    def __init__(self, length):
        self.length = length
        self.__buf = np.zeros(length)
        self.dumpCnt = 0

    def update(self,newVal):
        '''
        Description:    Update filter buffer and return new filter output.
    
        Params:         newVal:         New data sample
        
        Returns:        filtOut:        Filter output sample
                        filtOutValid:   Valid output flag
        '''
        filtOut = sum(self.__buf)/self.length
        self.__buf[1:] = self.__buf[0:-1]
        self.__buf[0] = newVal
        self.dumpCnt += 1
        if (self.dumpCnt == self.length):
            filtOut = sum(self.__buf)/self.length
            self.dumpCnt = 0
            filtOutValid = 1
        else:
            filtOutValid = 0
        return (filtOut,filtOutValid)

    def clear(self):
        '''
        Description:    Clear filter buffer (zeros) and dump counter
    
        Params:         None
        
        Returns:        None
        '''
        self.__buf = np.zeros[self.length]
        self.dumpCnt = 0

    def calc(self,data):
        '''
        Description:    Implement integrate dump filter on input data array.
    
        Params:         data:       Input data array to be filtered
        
        Returns:        filtData:   Filt array of size floor(data.size/length) 
        '''
        filtData = np.zeros(int(np.floor(data.size/self.length)))
        for ii in range(0,filtData.size):
            filtData[ii] = sum(data[ii*self.length:ii*self.length+
                                self.length])/self.length
        return filtData

'''
# EXAMPLE:
import matplotlib.pyplot as plt
f = 1000
t = np.arange(0,1/f*10,1/f/100)
data = np.sin(2*np.pi*f*t)
print(data.size)
filtObj1 = IntDump(10)
filtData1 = filtObj1.calc(data)
filtObj2 = IntDump(23)
filtData2 = filtObj2.calc(data)
tFilt1 = np.arange(1/f/100*10,1/f*10+1/f/100*10,1/f/100*10)
tFilt2 = np.arange(1/f/100*23,1/f*10,1/f/100*23)
plt.figure()
plt.plot(t,data,'r',tFilt1,filtData1,'b',tFilt2,filtData2,'c')
plt.show()
'''