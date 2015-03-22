import numpy
import Wave
from scipy.io.wavfile import read
from scipy.io.wavfile import write
import  matplotlib.pyplot as pl
import operation as op

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
              

w = WavIO.open("D:\coba.wav")
w.print_info()

bin = op.operation.ToBinary(w.samples)
bigits = op.operation.makeBigit(bin)
print(bigits[10])
print(bigits.shape)
pl.figure(1)
pl.plot(w.samples)
pl.ylabel = "Amplitudo"
pl.xlabel = "Waktu"
pl.title = "coba.wav"







