import numpy
import Wave
from scipy.io.wavfile import read
from scipy.io.wavfile import write
import  matplotlib.pyplot as pl
import operation as op
import binascii
import math

class WavIO:
    @staticmethod
    def open(path):
        wav = read(path)
        waveObj = Wave.Wave("sample")
        waveObj.bitrate = wav[0]
        samples = wav[1]
        samples = numpy.array(samples,dtype =numpy.uint16)
        #for i in range(len(samples)):
        #    samples[i] = samples[i] + 32767
        waveObj.samples = samples
        waveObj.max = samples.max
        waveObj.min = samples.min
        waveObj.shape = samples.shape
        waveObj.type = samples.dtype
        return waveObj

    @staticmethod
    def write(path,wavObj):
        rate = wavObj.bitrate
        write(path+wavObj.name ,rate,wavObj.samples)

class payloadIO:
    @staticmethod
    def open(path):
        message = open(path).read()
        return message

    @staticmethod
    def write(path,message):
        f = open(path,mode='w')
        f.write(message)
        f.close()

class analytics:
    @staticmethod
    def calculatePSNR(original_wave,corrupted_wave):
        samplelen = len(original_wave)
        sum = 0
        for i in range(samplelen):
            sum+=(math.pow((original_wave[i] - corrupted_wave[i]),2))
        MSE = float(sum)/float(samplelen)
        if(MSE == 0):
            return -1
        else:
            max =65535 #16bit
            PSNR = 10*(math.log10((math.pow(max,2)/MSE)))
            return PSNR


        



          
#w = WavIO.open("D:\coba.wav")
#w.print_info()
#tes = [3732,1664,12523,4482,121,17543,2243,6742,9,10,11,12,13,14,15,16,20,11,33,14,12,10,10,1004,1012,1001,1000,1000,1000,1000,1013,999,998,990,992,991]
#bin = op.operation.numToBinary(tes)
#secret  = payloadIO.open("D:\secret.txt")
#secret = op.operation.stringToBinary(secret)
#result = op.operation.RDE_Array(bin,secret,20)
#intM1 = result[0]
#reducedMap = result[2]
#locMap1 = result[3]
#op.operation.inv_RDE_Array(intM1,locMap1,reducedMap)


#print(result[0])
#print(result[1])
#print(result[2])




#bigits = op.operation.makeBigit(bin)
#print(bigits[10])
#print(bigits.shape)
#pl.figure(1)
#pl.plot(w.samples)
#pl.ylabel = "Amplitudo"
#pl.xlabel = "Waktu"
#pl.title = "coba.wav"
#pl.show()






