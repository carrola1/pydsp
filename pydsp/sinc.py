import numpy as np
import matplotlib.pyplot as plt

class Sinc:
    """
    Designer:       Andrew Carroll

    Description:    Calculate and optionally plot sin(x)/x for given data rate

    Attributes:     dataRate: data rate (Hz)
                    units:    string input for desired freq units on plot
                              ('GHz','MHz','kHz','Hz')
    Methods:        plot():   Calculates sinc function and generates plot
                    calc():   Calculates sinc function  
    """
    __W = np.arange(np.pi/200,25*np.pi+np.pi/200,np.pi/200)
    __SIN_X = np.sin(__W) / __W

    def __init__(self, dataRate, units):
        self.dataRate = dataRate
        self.units = units
        if (units.lower() == 'GHz'.lower()):
          self.__range = 1e9
        elif (units.lower() == 'MHz'.lower()):
          self.__range = 1e6
        elif (units.lower() == 'kHz'.lower()):
          self.__range = 1e3
        elif (units.lower() == 'Hz'.lower()):
          self.__range = 1e0
        else:
          print('Error: Invalid units')

    def __crunch(self):
        freq    = self.__W*(self.dataRate/self.__range/np.pi)
        sinc = 10*np.log10(self.__SIN_X**2)

        # cap off at -70 dB
        sinc = np.clip(sinc,-70,None)
        return freq,sinc

    def plot(self):
        """
        Description:    Calculates and plots sinc function

        Params:         None

        Returns:        freq: frequency array in 'units'
                        sinc: sinc calculation (dB) 
        """
        freq,sinc = self.__crunch()
        plt.plot(freq,sinc)
        plt.xlabel(('Freq (' + self.units + ')'))
        plt.ylabel('dB')
        plt.title('Sinc Response')
        plt.show()
        return freq,sinc

    def calc(self):
        """
        Description:    Calculates sinc function

        Params:         None

        Returns:        freq: frequency array in 'units'
                        sinc: sinc calculation (dB) 
        """
        freq,sinc = self.__crunch()
        return freq,sinc

"""
# EXAMPLE:
test = Sinc(100,'kHz')
test.plot()
"""