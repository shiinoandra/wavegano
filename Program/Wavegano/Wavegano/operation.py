import numpy
import math
import binascii

class operation:
    @staticmethod 
    def numToBinary(numArr):
        binaries = []
        for sample in numArr:
            try:
                str = bin(sample)
                sample = operation.binaryStringtoArray(str[2:])
                while len(sample) < 16:
                    sample.insert(0,0)
                binaries.append(sample)
            except:
                continue
                #print(" ini nih biangnya")
               #print(sample)
        return binaries

    @staticmethod
    def binaryTonum(binaryArr):
        return [int(operation.binaryArraytoString(sample),2) for sample in binaryArr]

    @staticmethod
    def stringToBinary(msg):
        message = bin(int(binascii.hexlify(msg),16))
        binaries = operation.binaryStringtoArray(message[2:])
        return binaries

    @staticmethod
    def revStringToBinary(binaries):
        binstr = operation.binaryArraytoString(binaries)
        _hex = hex(int(binstr,2))[2:-1]
        message = binascii.unhexlify(_hex)
        return message

    @staticmethod
    def binaryStringtoArray(binaryString):
       binaries =[int(x) for x in binaryString]
       return binaries

    @staticmethod
    def binaryArraytoString(binaryArray):
        s= ''.join([str(x) for x in binaryArray])
        return s  


    @staticmethod
    def makeBigit(binaryArr):
        arr = numpy.array(binaryArr,dtype=int)
        bigits = arr.transpose()
        return bigits

    
    @staticmethod
    def intel_partition(WaveArray,segLength,P=None):
        groupA=[]
        groupB=[]
        if  P == None :
            bigits = operation.makeBigit(WaveArray)
            variances=[]
            for idx,bigit in enumerate(bigits):
                counter=0
                total_var=0
                while counter < numpy.alen(bigit):
                    seg= bigit[counter:counter+segLength]
                    var_seg = numpy.var(seg)
                    total_var += var_seg
                    counter += segLength
                variances.append((idx,total_var))
            #print(variances)
            sorted_variances = sorted(variances,key= lambda tup:tup[1])
            #print(sorted_variances)
            #print(sorted_variances)

            partition= [0 for i in range(16)]
            #append bit ke 9 , 11 , 13 , 15 ke grup A
            #DONOT FORGET index = bit-1
            groupA.append(sorted_variances[8][0])
            groupA.append(sorted_variances[10][0])
            groupA.append(sorted_variances[12][0])
            groupA.append(sorted_variances[14][0])
            #tandai pada partition
            partition[sorted_variances[8][0]] =1
            partition[sorted_variances[10][0]] =1
            partition[sorted_variances[12][0]] =1
            partition[sorted_variances[14][0]] =1

            #append bit ke 10 , 12 , 14 , 16 ke grup B
            #DONOT FORGET index = bit-1
            groupB.append(sorted_variances[9][0])
            groupB.append(sorted_variances[11][0])
            groupB.append(sorted_variances[13][0])
            groupB.append(sorted_variances[15][0])
            #tandai pada partition
            partition[sorted_variances[9][0]] =0
            partition[sorted_variances[11][0]] =0
            partition[sorted_variances[13][0]] =0
            partition[sorted_variances[15][0]] =0

            #bit ke 1 dan ke 3 ke grup A
            groupA.append(sorted_variances[0][0])
            groupA.append(sorted_variances[2][0])
            #bit ke 2 dan ke 4 ke grup B
            groupB.append(sorted_variances[1][0])
            groupB.append(sorted_variances[3][0])
            #tandai pada partition
            partition[sorted_variances[0][0]] =1
            partition[sorted_variances[1][0]] =0
            partition[sorted_variances[2][0]] =1
            partition[sorted_variances[3][0]] =0

            #sisanya
            groupA.append(sorted_variances[4][0])
            groupA.append(sorted_variances[5][0])
            groupB.append(sorted_variances[6][0])
            groupB.append(sorted_variances[7][0])

            #tandai pada partition
            partition[sorted_variances[4][0]] =1
            partition[sorted_variances[5][0]] =1
            partition[sorted_variances[6][0]] =0
            partition[sorted_variances[7][0]] =0

            #sort indeks yang disimpan pada kedua grup
            groupA = sorted(groupA)
            #print(groupA)
            groupB = sorted(groupB)
            #print(groupB)
            #print(partition)

            #susun kembali bigit berdasarkan index
            M1 = [bigits[i] for i in groupA]
            M1 = numpy.transpose(M1)
           # print(operation.binaryTonum(M1))
            M2 = [bigits[i] for i in groupB]
            M2 = numpy.transpose(M2)
           # print(operation.binaryTonum(M2))
            return (M1,M2,partition)
        else:
            bigits = operation.makeBigit(WaveArray)
            for idx,i in enumerate(P):
                if i == 1:
                    groupA.append(idx)
                else:
                    groupB.append(idx)
            M1 = [bigits[i] for i in groupA]
            M1 = numpy.transpose(M1)
            M2 = [bigits[i] for i in groupB]
            M2 = numpy.transpose(M2)

            return (M1,M2,P)

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
    @staticmethod
    def reconstructPartition(M1,M2,P):
        _M = []


        M1 = numpy.ndarray.transpose(M1)
        M2 = numpy.ndarray.transpose(M2)

        for i in range(len(P)):
            if P[i] == 1:
                _M.append(M1[0])
                M1 = numpy.delete(M1,0,0)
            else:
                _M.append(M2[0])
                M2 = numpy.delete(M2,0,0)
        _M2 = numpy.array(_M,dtype = int)
        _M2 = numpy.ndarray.transpose(_M2)
        return _M2


 

#a = [15, 7, 16, 17, 4, 14, 15, 5, 7, 20]
#b = operation.numToBinary(a)
#operation.intel_partition(b,3)



                


