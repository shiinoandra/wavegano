import numpy
import Wave
from scipy.io.wavfile import read
from scipy.io.wavfile import write
import  matplotlib.pyplot as pl
import operation as op
import binascii

class WavIO:
    @staticmethod
    def open(path):
        wav = read(path)
        waveObj = Wave.Wave("sample.wav")
        waveObj.bitrate = wav[0]
        samples = wav[1]
        waveObj.samples = samples
        waveObj.max = samples.max
        waveObj.min = samples.min
        waveObj.shape = samples.shape
        waveObj.type = samples.dtype
        return waveObj

    @staticmethod
    def write(path,wavObj):
        rate = wavObj.bitrate
        write(path,rate,wavObj.samples  )

class payloadIO:
    @staticmethod
    def open(path):
        message = open(path).read()
        return message


          
w = WavIO.open("D:\coba.wav")
w.print_info()
tes = [3732,1664,12523,4482,121,17543,2243,6742,9,10,11,12,13,14,15,16,20,11,33,14,12,10,10,1004,1012,1001,1000,1000,1000,1000,1013,999,998,990,992,991]
bin = op.operation.numToBinary(tes)
secret  = payloadIO.open("D:\secret.txt")
secret = op.operation.stringToBinary(secret)
result = op.operation.RDE_Array(bin,secret,20)
intM1 = result[0]
reducedMap = result[2]
locMap1 = result[3]
op.operation.inv_RDE_Array(intM1,locMap1,reducedMap)


#print(result[0])
#print(result[1])
#print(result[2])




#bigits = op.operation.makeBigit(bin)
#print(bigits[10])
#print(bigits.shape)







