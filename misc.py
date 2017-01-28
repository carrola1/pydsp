#import numpy as np

class Accum():
    ''' 
    Designer:       Andrew Carroll

    Description:    Accumulator with optional rollover/clamp.
    
    Attributes:     maxVal:     Maximum value of accumulator
                    rollOver:   (*optional) Set to True for automatic rollover
                                    at maxVal. Otherwise clamp at maxVal.
                                    Default = True
                    
    Methods:        update(incrVal):        Add incrVal to accumulator
                    clear():                Clear accumulator (set to 0)
    '''
    def __init__(self,maxVal,rollOver=True):
        self.maxVal = maxVal
        self.accum = 0
        self.rollOver = rollOver

    def update(self,incrVal):
        '''
        Description:    Add incrVal to accumulator

        Params:         incrVal:    Value to add to accumulator

        Returns:        accum:      New accumulator value
        '''
        self.accum = self.accum + incrVal
        if (self.accum > self.maxVal):
            if (self.rollOver == True):
                self.accum = self.accum - self.maxVal - 1
            else: 
                self.accum = self.maxVal
        elif (self.accum < 0):
            if (self.rollOver == True):
                self.accum = self.accum + self.maxVal + 1
            else: 
                self.accum = 0
        return self.accum

    def clear(self):
        '''
        Description:    Clear accumulator

        Params:         None

        Returns:        None
        '''
        self.accum = 0
        return

class NCO(Accum):
    ''' 
    Designer:       Andrew Carroll

    Description:    Implements Numerically Controlled Oscillator. Special
                    Accum subclass with rollOver always set to True. 
    
    Attributes:     maxVal:     Maximum value of accumulator
                    
    Methods:        update(incrVal):        Add incrVal to accumulator
                    clear():                Clear accumulator (set to 0)
    '''
    def __init__(self,maxVal):
        super(NCO, self).__init__(maxVal)
