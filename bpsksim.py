import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import bitgen
import noisegen
import agc
import qtrratedwncvt
import fir
import intdump

# Parameters
F_SAMP = 10e6
F_BIT = 100e3
F_CAR = 2.5e6
NUM_BITS = 5000
NUM_SAMPS = int(F_SAMP/F_BIT*NUM_BITS)
EB_NO = 4
BIT_W = 10
FULL_SCALE = 2**(BIT_W-1)-1
BIT_GAIN = 4
PH_OFFSET = np.pi/2
SAMP_DLY = 50

# FIR Design
taps = signal.firwin(100, cutoff = 0.03, window = "hamming")

# Create DSP objects
bitGen = bitgen.GenPn(9,int(F_SAMP/F_BIT))
noiseGen = noisegen.EbNo(F_BIT,F_SAMP,EB_NO)
agc = agc.AGC(100,FULL_SCALE,3)
qtrRate = qtrratedwncvt.QtrRateDwnCvt()
firFiltI = fir.FIR(taps)
firFiltQ = fir.FIR(taps)
intDumpI = intdump.IntDump(100)
intDumpQ = intdump.IntDump(100)

# Test Sigs
tArr = np.zeros(NUM_SAMPS)
tSigI = np.zeros(NUM_SAMPS)
tSigQ = np.zeros(NUM_SAMPS)

bitRec = np.array([])
tp = np.array([])
sampDly = 0
for ii in range(0,NUM_SAMPS):
    t = ii*1/F_SAMP
    tArr[ii] = t

    # Create input signal
    sigIn = np.sin(2*np.pi*F_CAR*t+PH_OFFSET)
    sigIn = sigIn*bitGen.getSamp() + noiseGen.getNoise(1)
    sigIn = agc.update(sigIn)
    sigIn = int(np.clip(sigIn,-FULL_SCALE,FULL_SCALE))

    # Receiver
    iSig,qSig = qtrRate.update(sigIn)
    iSig = firFiltI.update(iSig)
    qSig = firFiltQ.update(qSig)
    iSig = int(np.clip(iSig*BIT_GAIN,-FULL_SCALE,FULL_SCALE))
    qSig = int(np.clip(qSig*BIT_GAIN,-FULL_SCALE,FULL_SCALE))
    tSigI[ii] = iSig
    tSigQ[ii] = qSig
    if (sampDly == SAMP_DLY):
        iSig, iSigVal = intDumpI.update(iSig)
        qSig, qSigVal = intDumpQ.update(qSig)
        if (iSigVal == 1):
            bitRec = np.append(bitRec, np.sign(iSig))
    else:
        sampDly += 1


"""
plt.figure()
plt.plot(tArr[0:int(F_SAMP/F_BIT*20)],tSigI[0:int(F_SAMP/F_BIT*20)],'b',
            tArr[0:int(F_SAMP/F_BIT*20)],tSigQ[0:int(F_SAMP/F_BIT*20)],'r')
plt.show()
"""
theoCurveEbNo = np.array([-2,-1,0,1,2,3,4,5,6])
theoCurveBER = np.array([.13,.1,.08,.06,.04,.022,.012,.006,.0025])
bitGen.upSampRate = 1
bitGen.reset()
bitSent = bitGen.getArr(NUM_BITS)
numErr = np.sum(np.abs((bitSent[0:-1]*bitRec - 1)/2))
ber = numErr/NUM_BITS
print(numErr)
print(ber)
plt.figure()
plt.plot(theoCurveEbNo,theoCurveBER,'b',EB_NO,ber,'ro')
plt.show()