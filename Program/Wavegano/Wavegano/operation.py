import numpy

class operation:
    @staticmethod 
    def ToBinary(numArr):
        binaries = []
        for sample in numArr:
            sample = [int(x) for x in bin(sample)[2:]]
            while len(sample) < 16:
                sample.insert(0,0)
            binaries.append(sample)
        return binaries

    @staticmethod
    def makeBigit(binaryArr):
        arr = numpy.array(binaryArr,dtype=int)
        bigits = arr.transpose()
        return bigits

