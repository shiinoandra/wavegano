import operation as op
import random
import math
import Helper
import GRDEI
import RDE
import GDE
import Wave
import os
import numpy

numpy.set_printoptions(threshold=numpy.nan)

##def logger(angka):
##    rd = angka - pow(2,((math.floor(math.log(angka,2)))-1))  - pow(2,(math.floor(math.log(angka,2))-2))
##    flag =0
##    if math.pow(2,(math.floor(math.log(angka,2)))) / math.pow(2,(math.floor(math.log(rd,2)))) == 4:
##        flag = 1
##    if math.pow(2,(math.floor(math.log(angka,2)))) / math.pow(2,(math.floor(math.log(rd,2)))) == 1:
##        flag = 2
##    return (rd,flag)


##def inv_logger(angka,flag):
##    if flag ==1:
##        rd = angka + pow(2,(math.floor(math.log(angka,2))))  + pow(2,(math.floor(math.log(angka,2))+1))
##    elif flag ==2:
##        rd = angka + pow(2,(math.floor(math.log(angka,2))-1))  + pow(2,(math.floor(math.log(angka,2))-2))
##    else:
##        rd = angka + pow(2,(math.floor(math.log(angka,2))-1))  + pow(2,(math.floor(math.log(angka,2))))
##    return rd

#def logger_rde(angka):
#    flag =0
#    rd = angka - pow(2,((math.floor(math.log(angka,2)))-1))
#    if math.pow(2,(math.floor(math.log(angka,2)))) == math.pow(2,(math.floor(math.log(rd,2)))):
#        flag=1
#    return (rd,flag)

#def inv_logger_rde(angka,flag):
#    if(flag != 1):
#        rd = angka + pow(2,((math.floor(math.log(angka,2)))))
#    else:
#       rd = angka + pow(2,((math.floor(math.log(angka,2)))-1))

#    return rd




##f= open("hasil.txt",mode='w')
##for i in range(4,255):
    
##    a = logger(i)
##    b = (inv_logger(a[0],a[1]))
##    #if( int(i) != b):
##    f.write(str(i))
##    f.write("\n")
##    f.write(str(a[0]))
##    f.write("\n")
##    f.write(str(b))
##    f.write("\n")
##    f.write("------------------------------------")
##    f.write("\n")
##f.close()


#f= open("hasil_rde.txt",mode='w')
#for i in range(4,255):
#    a = logger_rde(i)
#    b = (inv_logger_rde(a[0],a[1]))
#    f.write(str(i))
#    f.write("\n")
#    f.write(str(a[0]))
#    f.write("\n")
#    f.write(str(b))
#    f.write("\n")
#    f.write("------------------------------------")
#    f.write("\n")
#f.close()






if __name__ == "__main__":
    payload = Helper.payloadIO.open("D:\\payload.txt")
   # print "data payload : "
    #print(payload)
  
    bin_payload = op.operation.stringToBinary(payload)

    print "besar payload : "
    payload_size = len(bin_payload)
    print(payload_size) 


    besar_segmen_partisi = 10
    medium = Helper.WavIO.open("D:\\coba16.wav")
    print "bitrate: "
    print(medium.bitrate)
    samples = op.operation.numToBinary(medium.samples)

    besar_segmen = 2
    threshold = 5
    (M1,M2,Partisi) = op.operation.intel_partition(samples,besar_segmen_partisi)

    intM1 = op.operation.binaryTonum(M1)
    intM2 = op.operation.binaryTonum(M2)
    kapasitas_M1 = GRDEI.checkCapacity(intM1,besar_segmen,threshold)
    kapasitas_M2 = GRDEI.checkCapacity(intM2,besar_segmen,threshold)
    print(" kapasitas segmen 1 : " + str(kapasitas_M1))
    print(" kapasitas segmen 2 : " + str(kapasitas_M2))
    capacity = kapasitas_M1+kapasitas_M2
    print "Kapasitas penyimpanan :"
    print(capacity)

    if capacity >= payload_size:
        print "stegano dapat dilakukan"
        payload_seg1 = bin_payload[:kapasitas_M1]
        print(len(payload_seg1))
        payload_seg2 = bin_payload[kapasitas_M1:len(bin_payload)]
        print(len(payload_seg2))
        (encoded_1,locMap_1,reducedMap_1) = GRDEI.encode(intM1,payload_seg1,besar_segmen,threshold)
        (encoded_2,locMap_2,reducedMap_2) = GRDEI.encode(intM2,payload_seg2,besar_segmen,threshold)
        encoded_1 = op.operation.numToBinary(encoded_1)
        encoded_2 = op.operation.numToBinary(encoded_2)
        for i in range(len(encoded_1)):
            encoded_1[i]=encoded_1[i][8:16] 
        for i in range(len(encoded_2)):
            encoded_2[i]=encoded_2[i][8:16] 
        encoded_1_bin = numpy.array(encoded_1,dtype=int)
        encoded_2_bin = numpy.array(encoded_2,dtype=int)
        _M = op.operation.reconstructPartition(encoded_1_bin,encoded_2_bin,Partisi)
        _M_int = numpy.asarray(op.operation.binaryTonum(_M),dtype=numpy.int16)
        new_wav = Wave.Wave("encoded16.wav")
        new_wav.samples = _M_int
        new_wav.bitrate = 22050
        #print(medium.samples)
        #raw_input()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
        #print(new_wav.samples)
        new_wav.print_info()
        medium.print_info()
        Helper.WavIO.write("D:\\",new_wav)

        ########### DECODING ###############

        medium_encoded = Helper.WavIO.open("D:\\coba16.wav")
        print "bitrate: "
        print(medium_encoded.bitrate)
        samples_decode = op.operation.numToBinary(medium_encoded.samples)

        (_M1,_M2,P) = op.operation.intel_partition(samples_decode,besar_segmen_partisi,Partisi)
        _intM1 = op.operation.binaryTonum(_M1)
        _intM2 = op.operation.binaryTonum(_M2)
        (decoded_M1,message1) = GRDEI.decode(_intM1,besar_segmen,locMap_1,reducedMap_1)
        (decoded_M2,message2) = GRDEI.decode(_intM2,besar_segmen,locMap_2,reducedMap_2)
        counter =0
        for i in range(len(decoded_M1)):
            if(decoded_M1[i] != intM1[i]):
                print(str(decoded_M1[i])+ " --- " + str(intM1[i]))
        for i in locMap_1:
            if i == 0:
                counter+=1
        print(counter)


        message_decoded = []
        message_decoded.extend(message1)
        message_decoded.extend(message2)
        message_decoded = message_decoded[:payload_size]
        message_write = op.operation.revStringToBinary(message_decoded)
        Helper.payloadIO.write("D:\\payload_decoded.txt",message_write)


    else:
        print "kapasitas tidak mencukupi" 


