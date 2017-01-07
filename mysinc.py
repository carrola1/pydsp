import numpy as np
import matplotlib.pyplot as plt

class mySinc:
  
  __w = np.arange(np.pi/200,25*np.pi+np.pi/200,np.pi/200)
  __sinx = np.sin(__w) / __w

  def __init__(self, dataRate, units):
    self.dataRate = dataRate
    self.units = units
    if (units.lower() == 'GHz'.lower()):
      self.range = 1e9
    elif (units.lower() == 'MHz'.lower()):
      self.range = 1e6
    elif (units.lower() == 'kHz'.lower()):
      self.range = 1e3
    elif (units.lower() == 'Hz'.lower()):
      self.range = 1e0
    else:
      print('Error: Invalid units')

  def __crunch(self):
    freq    = self.__w*(self.dataRate/self.range/np.pi)
    sinc = 10*np.log10(self.__sinx**2)
    # cap off at -70 dB
    sinc = np.clip(sinc,-70,None)
    return freq,sinc

  def plot(self):
    freq,sinc = self.__crunch()
    plt.plot(freq,sinc)
    plt.xlabel(('Freq (' + self.units + ')'))
    plt.ylabel('dB')
    plt.title('Sinc Response')
    plt.show()
    return freq,sinc

  def calc(self):
    freq,sinc = self.__crunch()
    return freq,sinc