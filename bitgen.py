import numpy as np

class BitGen:
    ''' 
    Designer:       Andrew Carroll

    Description:    Implements moving average filter. Functions in sample or
                    array based modes.
    
    Attributes:     length: length of moving average filter
    
    Methods:        update(newVal): Update filter buf and return new output.
                    clear():        Clear filter buffer
                    calc():         Return filtered data array
    '''
    def __init__(self,pattern,upSampRate):
        self.upSampRate = upSampRate
        self.pattern = pattern
        self.ind = 0
        self.patLen = pattern.size
        self.upSampCnt = 0

    def reset(self):
        self.ind = 0
        self.upSampCnt = 0
        return

    def getSamp(self):
        newSamp = self.pattern[self.ind]
        if (self.upSampCnt == self.upSampRate-1):
            self.upSampCnt = 0 
            if (self.ind == self.patLen-1):
                self.ind = 0
            else:
                self.ind += 1
        else:
            self.upSampCnt += 1
        return newSamp

    def getArr(self,numBits):
        dataOut = np.array([])
        for ii in range(0,int(np.ceil(numBits/self.patLen))):
            if (ii == int(np.ceil(numBits/self.patLen))-1):
                dataOut = np.append(dataOut,self.pattern[
                            0:numBits-dataOut.size])
            else:
                dataOut = np.append(dataOut,self.pattern)
        return np.repeat(dataOut,self.upSampRate)

class GenSqWv(BitGen):
    def __init__(self,upSampRate=1,zerosOut=False):
        if (zerosOut == False):
            patterni = np.array([-1,1])
        else:
            patterni = np.array([0,1])
        super(GenSqWv, self).__init__(patterni,upSampRate)

class GenHexPat(BitGen):
    def __init__(self,hexPat,upSampRate=1,zerosOut=False):
        patterni  = "{0:04b}".format(int(hexPat))
        patterni = np.array(list(map(int,patterni)))

        if (zerosOut == False):
            patterni = patterni*2-1
        super(GenHexPat, self).__init__(patterni,upSampRate)

class GenArbArr(BitGen):
    def __init__(self,pattern,upSampRate=1,zerosOut=False):
        if (zerosOut == False):
            patterni = pattern*2-1
        else:
            patterni = pattern
        super(GenArbArr, self).__init__(patterni,upSampRate)

#class GenRndBits:

class GenPn(BitGen):
    TAPS = {23:np.array([23,18,1]),
            15:np.array([15,14,1]),
             9:np.array([9,5,1])}

    def __init__(self,pow2,upSampRate=1,zerosOut=False):
        patterni = self.__calcPn(pow2)
        if (zerosOut == False):
            patterni = (patterni - 1)*2 + 1
        super(GenPn, self).__init__(patterni,upSampRate)
    
    def __calcPn(self,pow2):
        fBTaps = self.TAPS[pow2]
        shiftReg = np.ones(pow2)
        pnOut = np.zeros(2**pow2-1)
        fBSel = np.zeros(pow2)

        for tap in fBTaps:
            if (tap != 1):
                fBSel[tap-1] = 1

        for ii, elem in enumerate(pnOut):
            pnOut[ii] = shiftReg[pow2-1]
            fB = shiftReg*fBSel
            fBXOR = sum(fB) % 2
            shiftReg = np.append(fBXOR,shiftReg[0:-1])            
        return pnOut

test = GenPn(15,1,False)
x = test.getArr(20)
print(x)


    


