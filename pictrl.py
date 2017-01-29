import numpy as np

class PICtrl():
    """
    Designer:       Andrew Carroll

    Description:    Implements Proportional Integral Controller.
    
    Attributes:     pCoeff:     Proportional coefficient
                    iCoeff:     Integral coefficient
                    maxVal:     Max output value (+/-)
                    
    Methods:        update(sampIn):     Update controller with new sample
                    clear():            Reset integral accumulator to 0
    """
    def __init__(self,pCoeff,iCoeff,maxVal):
        self.pCoefff = pCoeff
        self.iCoeff = iCoeff
        self.maxVal = maxVal
        self.__accum = 0

    def update(self,sampIn):
        """
        Description:    Update controller with new sample

        Params:         sampIn:     New input sample

        Returns:        sampOut:    Output sample
        """
        self.__accum += sampIn*self.iCoeff
        sampOut = sampIn*self.pCoeff + self.__accum
        sampOut = np.clip(sampOut,-self.maxVal,self.maxVal)
        return sampOut

    def clear(self):
        """
        Description:    Reset integral accumulator to 0

        Params:         None

        Returns:        None
        """
        self.__accum = 0
        