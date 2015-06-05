import operation as op
import kromosom as kromosom


class genetic:
    def __init__(self,jumlahpop=100,thresbitlength=8,layerbitlength=4,segbitlength=10):
        self.populasi = []
        self.jumlahPopulasi = jumlahpop
        self.bestSolution = kromosom.kromosom
        self.optimalCapacity=0
        self.optimalQuality=0
        self.segBitLength=segbitlength
        self.thresBitLength=thresbitlength
        self.layerBitLength=layerbitlength

    def getFitness(self):

        for k in self.populasi:
            segment_length = int(op.operation.binaryArraytoString(k.data[0:self.segBitLength]),2)
            threshold = int(op.operation.binaryArraytoString(k.data[segBitLength:self.segBitLength+self.thresBitLength]),2)
            jml_layer = int(op.operation.binaryArraytoString(k.data[self.segBitLength+self.thresBitLength:]),2)
            print(segment_length)
            print(threshold)
            print(jml_layer)

g = genetic(10,3,4,3)
k = kromosom.kromosom("1100100011")
g.populasi.append(k)
g.getFitness()




