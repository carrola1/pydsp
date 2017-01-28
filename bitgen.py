import numpy as np

class __BitGen:
    ''' 
    Designer:       Andrew Carroll

    Description:    Generic pattern bit generation with upsampling option.
    
    Attributes:     pattern:    Array pattern to generate bits from
                    upSampRate: Upsampling rate
    
    Methods:        reset():            Reset pattern and upsampling
                    getSamp():          Get next sample in pattern
                    getArr(numBits):    Get next numBits in pattern
    '''
    def __init__(self,pattern,upSampRate):
        self.upSampRate = upSampRate
        self.pattern = pattern
        self.ind = 0
        self.__patLen = pattern.size
        self.upSampCnt = 0

    def reset(self):
        '''
        Description:    Resets pattern and upsample counter

        Params:         None

        Returns:        None
        '''
        self.ind = 0
        self.upSampCnt = 0
        return

    def getSamp(self):
        '''
        Description:    Gets new sample (new bit or hold previous value during
                            upsampling)

        Params:         None

        Returns:        newSamp:    Single bit value 
        '''
        newSamp = self.pattern[self.ind]
        if (self.upSampCnt == self.upSampRate-1):
            self.upSampCnt = 0 
            if (self.ind == self.__patLen-1):
                self.ind = 0
            else:
                self.ind += 1
        else:
            self.upSampCnt += 1
        return newSamp

    def getArr(self,numBits):
        '''
        Description:    Gets next specified # of bits in pattern

        Params:         numBits:    # of bits to return

        Returns:        dataOut:    Upsampled array of bits
        '''
        dataOut = np.array([])
        for ii in range(0,int(np.ceil(numBits/self.__patLen))):
            if (ii == int(np.ceil(numBits/self.__patLen))-1):
                dataOut = np.append(dataOut,self.pattern[
                            0:numBits-dataOut.size])
            else:
                dataOut = np.append(dataOut,self.pattern)
        return np.repeat(dataOut,self.upSampRate)

class GenSqWv(__BitGen):
    ''' 
    Designer:       Andrew Carroll

    Description:    Subclass of __BitGen, generates square wave pattern
    
    Attributes:     upSampRate: Integer upsampling rate (default = 1)
                    zerosOut:   Set to True to use 0 instead of -1 for low
                                    bit (default = False)
                    
    Methods:        See BitGen class
    '''
    def __init__(self,upSampRate=1,zerosOut=False):
        if (zerosOut == False):
            patterni = np.array([-1,1])
        else:
            patterni = np.array([0,1])
        super(GenSqWv, self).__init__(patterni,upSampRate)

class GenHexPat(__BitGen):
    ''' 
    Designer:       Andrew Carroll

    Description:    Subclass of __BitGen, generates 8-bit hex pattern
    
    Attributes:     hexPat:     8-bit hex input (Ex. 0x55)
                    upSampRate: Integer upsampling rate (default = 1)
                    zerosOut:   Set to True to use 0 instead of -1 for low
                                    bit (default = False)
                    
    Methods:        See BitGen class
    '''
    def __init__(self,hexPat,upSampRate=1,zerosOut=False):
        patterni  = "{0:08b}".format(int(hexPat))
        patterni = np.array(list(map(int,patterni)))

        if (zerosOut == False):
            patterni = patterni*2-1
        super(GenHexPat, self).__init__(patterni,upSampRate)

class GenArbArr(__BitGen):
    ''' 
    Designer:       Andrew Carroll

    Description:    Subclass of __BitGen, generates arbitrary pattern
    
    Attributes:     pattern:    Array of 0's and 1's to use as pattern
                    upSampRate: Integer upsampling rate (default = 1)
                    zerosOut:   Set to True to use 0 instead of -1 for low
                                    bit (default = False)
                    
    Methods:        See BitGen class
    '''
    def __init__(self,pattern,upSampRate=1,zerosOut=False):
        if (zerosOut == False):
            patterni = pattern*2-1
        else:
            patterni = pattern
        super(GenArbArr, self).__init__(patterni,upSampRate)

class GenRndBits:
    ''' 
    Designer:       Andrew Carroll

    Description:    Generates random bit pattern
    
    Attributes:     upSampRate: Integer upsampling rate (default = 1)
                    zerosOut:   Set to True to use 0 instead of -1 for low
                                    bit (default = False)
                    
    Methods:        reset():            Reset upsampling
                    getSamp():          Get next sample
                    getArr(numBits):    Get array of upsampled random bits
    '''
    def __init__(self,upSampRate=1,zerosOut=False):
        self.upSampRate = upSampRate
        self.zerosOut = zerosOut
        self.upSampCnt = self.upSampRate-1
        self.sampOut = 0

    def reset(self):
        '''
        Description:    Resets upsample counter

        Params:         None

        Returns:        None
        '''
        self.upSampCnt = self.upSampRate-1
        return

    def getSamp(self):
        '''
        Description:    Gets next sample (new bit or hold previous value during
                            upsampling)

        Params:         None

        Returns:        newSamp:    Single bit value 
        '''
        if (self.upSampCnt == self.upSampRate-1):
            self.upSampCnt = 0
            self.sampOut = np.random.randint(0,2)
        else:
            self.upSampCnt += 1      
        if (self.zerosOut == False):
            self.sampOut = self.sampOut*2-1
        return self.sampOut

    def getArr(self,numBits):
        '''
        Description:    Gets array of upsampled random bits

        Params:         numBits:    # of bits to return

        Returns:        dataOut:    Upsampled array of bits
        '''
        dataOut = np.random.randint(0,2,numBits)
        if (self.zerosOut == False):
            dataOut = dataOut*2-1
        return np.repeat(dataOut,self.upSampRate)


class GenPn():
    ''' 
    Designer:       Andrew Carroll

    Description:    Generates maximal length PN pattern
    
    Attributes:     pow2:       Specifies power of PN pattern to generate 
                                    (currently supports 9, 15, and 23) 

                    upSampRate: Integer upsampling rate (default = 1)
                    zerosOut:   Set to True to use 0 instead of -1 for low
                                    bit (default = False)
                    
    Methods:        reset():            Reset pattern and upsampling
                    getSamp():          Get next sample
                    getArr(numPn):      Get array of upsampled bits
    '''
    # Dictionary of feedback taps for specific PN patterns
    __TAPS = {23:np.array([23,18,1]),
              15:np.array([15,14,1]),
               9:np.array([9,5,1])}

    def __init__(self,pow2,upSampRate=1,zerosOut=False):
        self.pow2 = pow2
        self.upSampRate = upSampRate
        self.upSampCnt = 0
        self.zerosOut = zerosOut
        self.__shiftReg = np.ones(pow2)
        self.__fBSel = np.zeros(pow2)
        fBTaps = self.__TAPS[pow2]
        for tap in fBTaps:
            if (tap != 1):
                self.__fBSel[tap-1] = 1
        self.pnOut = self.__shiftReg[pow2-1]

    def reset(self):
        '''
        Description:    Resets pattern and upsample counter

        Params:         None

        Returns:        None
        '''
        self.upSampCnt = 0
        self.__shiftReg = np.ones(self.pow2)
        self.pnOut = self.__shiftReg[self.pow2-1]

    def __getSeq(self):
        pnSeq = np.zeros(2**self.pow2-1)
        for ii, elem in enumerate(pnSeq):
            pnSeq[ii] = self.__shiftReg[self.pow2-1]
            fB = self.__shiftReg*self.__fBSel
            fBXOR = sum(fB) % 2
            self.__shiftReg = np.append(fBXOR,self.__shiftReg[0:-1])            
        return pnSeq

    def getSamp(self):
        '''
        Description:    Gets next sample (new bit or hold previous value during
                            upsampling)

        Params:         None

        Returns:        newSamp:    Single bit value 
        '''
        if (self.upSampCnt == self.upSampRate-1):
            self.upSampCnt = 0
            fB = self.__shiftReg*self.__fBSel
            fBXOR = sum(fB) % 2
            self.__shiftReg = np.append(fBXOR,self.__shiftReg[0:-1])
            self.pnOut = self.__shiftReg[self.pow2-1]
            if (self.zerosOut == False):
                self.pnOut = self.pnOut*2-1
        else:
            self.upSampCnt += 1    
        return self.pnOut

    def getArr(self,numPn):
        '''
        Description:    Gets array of upsampled bits

        Params:         numBits:    # of bits to return

        Returns:        dataOut:    Upsampled array of bits
        '''
        pnArr = np.zeros(numPn)
        if (numPn > 2**self.pow2-1):
            pnSeq = self.__getSeq()
            for ii in range(0,int(np.floor(numPn/pnSeq.size))):
                pnArr[ii*pnSeq.size:ii*pnSeq.size+pnSeq.size] = pnSeq
            for jj in range(numPn-int(np.floor(numPn/pnSeq.size))*pnSeq.size):
                self.upSampCnt = self.upSampRate-1
                pnArr[jj] = self.getSamp()
        else:
            for ii, elem in enumerate(pnArr):
                self.upSampCnt = self.upSampRate-1
                pnArr[ii] = self.getSamp()
        self.upSampCnt = 0
        return np.repeat(pnArr,self.upSampRate)

'''
# EXAMPLE:
test = GenPn(9,3)
x = np.zeros(200)
for ii in range(0,x.size):
    x[ii] = test.getSamp()
print(x)
'''
    


