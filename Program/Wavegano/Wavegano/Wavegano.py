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


def encode(payload_path,cover_path,threshold,segment_size,partition_segment_size,method):
    file_name = cover_path.split("\\")[len(cover_path.split("\\"))-1]
    path = cover_path.replace(file_name,'')
    print(" PROSES ENCODING ")
    print(" METODE YANG DIGUNAKAN : " + method)
    payload = Helper.payloadIO.open(payload_path)
    bin_payload = op.operation.stringToBinary(payload)
    print "besar payload : "
    payload_size = len(bin_payload)
    print(payload_size) 
    medium = Helper.WavIO.open(cover_path)
    print "bitrate: "
    print(medium.bitrate)
    samples = op.operation.numToBinary(medium.samples)
    (M1,M2,Partisi) = op.operation.intel_partition(samples,partition_segment_size)
    intM1 = op.operation.binaryTonum(M1)
    intM2 = op.operation.binaryTonum(M2)
    if method == "GDE" :
        kapasitas_M1 = GDE.checkCapacity(intM1,segment_size,threshold)
        kapasitas_M2 = GDE.checkCapacity(intM2,segment_size,threshold)
    elif method == "GRDEI":
        kapasitas_M1 = GRDEI.checkCapacity(intM1,segment_size,threshold)
        kapasitas_M2 = GRDEI.checkCapacity(intM2,segment_size,threshold)
    print(" kapasitas segmen 1 : " + str(kapasitas_M1))
    print(" kapasitas segmen 2 : " + str(kapasitas_M2))
    capacity = kapasitas_M1+kapasitas_M2
    print "Kapasitas penyimpanan :"
    print(capacity)
    if capacity >= payload_size:
        print "stegano dapat dilakukan"
        payload_seg1 = bin_payload[:kapasitas_M1]
        payload_seg2 = bin_payload[kapasitas_M1:len(bin_payload)]
        if method == "GDE" :
            (encoded_1,locMap_1) = GDE.encode(intM1,payload_seg1,segment_size,threshold)
            (encoded_2,locMap_2) = GDE.encode(intM2,payload_seg2,segment_size,threshold)
        elif method == "GRDEI":
            (encoded_1,locMap_1,reduceMap_1) = GRDEI.encode(intM1,payload_seg1,segment_size,threshold)
            (encoded_2,locMap_2,reduceMap_2) = GRDEI.encode(intM2,payload_seg2,segment_size,threshold)
        encoded_1 = op.operation.numToBinary(encoded_1)
        encoded_2 = op.operation.numToBinary(encoded_2)
        for i in range(len(encoded_1)):
            encoded_1[i]=encoded_1[i][8:16] 
        for i in range(len(encoded_2)):
            encoded_2[i]=encoded_2[i][8:16] 
        encoded_1_bin = numpy.array(encoded_1,dtype=int)
        encoded_2_bin = numpy.array(encoded_2,dtype=int)
        _M = op.operation.reconstructPartition(encoded_1_bin,encoded_2_bin,Partisi)
        _M_int2= numpy.asarray(op.operation.binaryTonum(_M),dtype=numpy.uint16)
        _M_int = numpy.asarray(op.operation.binaryTonum(_M),dtype=numpy.int16)
        new_wav = Wave.Wave(method+"_encoded_"+str(file_name))
        new_wav.samples = _M_int
        new_wav.bitrate = medium.bitrate
        #print(medium.samples)
        #raw_input()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
        #print(new_wav.samples)
        #new_wav.print_info()
        #medium.print_info()
        Helper.WavIO.write(path,new_wav)
        if method == "GDE" :
            return(locMap_1,locMap_2,Partisi)
        elif method == "GRDEI":
            return(locMap_1,locMap_2,reduceMap_1,reduceMap_2,Partisi)

    else:
        print "kapasitas tidak mencukupi"
        return -1 

def decode(file_path,segment_size,payload_size,method,Partition,locMap_1,locMap_2,reduceMap_1 = None , reduceMap_2 = None):
        file_name = file_path.split("\\")[len(file_path.split("\\"))-1]
        path = file_path.replace(file_name,'')
        print(" PROSES DECODING ")
        print(" METODE YANG DIGUNAKAN : " + method)
        medium_encoded = Helper.WavIO.open(file_path)
        print "bitrate: "
        print(medium_encoded.bitrate)
        samples_decode = op.operation.numToBinary(medium_encoded.samples)
        (_M1,_M2,P) = op.operation.intel_partition(samples_decode,0,Partition)
        _intM1 = op.operation.binaryTonum(_M1)
        _intM2 = op.operation.binaryTonum(_M2)
        if method == "GDE" :
            (decoded_M1,message1) = GDE.decode(_intM1,segment_size,locMap_1)
            (decoded_M2,message2) = GDE.decode(_intM2,segment_size,locMap_2)
        elif method == "GRDEI":
            (decoded_M1,message1) = GRDEI.decode(_intM1,segment_size,locMap_1,reduceMap_1)
            (decoded_M2,message2) = GRDEI.decode(_intM2,segment_size,locMap_2,reduceMap_2)

        message_decoded = []
        message_decoded.extend(message1)
        message_decoded.extend(message2)
        message_decoded = message_decoded[:payload_size]
        message_write = op.operation.revStringToBinary(message_decoded)
        Helper.payloadIO.write(path+"payload_decoded.txt",message_write)
        decoded_1 = op.operation.numToBinary(decoded_M1)
        decoded_2 = op.operation.numToBinary(decoded_M2)
        for i in range(len(decoded_1)):
            decoded_1[i]=decoded_1[i][8:16] 
        for i in range(len(decoded_2)):
            decoded_2[i]=decoded_2[i][8:16] 
        decoded_1_bin = numpy.array(decoded_1,dtype=int)
        decoded_2_bin = numpy.array(decoded_2,dtype=int)
        M_awal = op.operation.reconstructPartition(decoded_1_bin,decoded_2_bin,Partition)
        M__awal = numpy.asarray(op.operation.binaryTonum(M_awal),dtype=numpy.int16)


        new_wav2 = Wave.Wave(file_name.replace("encoded","decoded"))
        new_wav2.samples = M__awal
        new_wav2.bitrate = medium_encoded.bitrate
        Helper.WavIO.write(path,new_wav2)



if __name__ == "__main__":
    (map1,map2,rmap1,rmap2,p) = encode("D:\\payload.txt","D:\\coba16.wav",100,20,10,"GRDEI")
    decode("D:\\GRDEI_encoded_coba16.wav",20,1831,"GRDEI",p,map1,map2,rmap1,rmap2)
#   # print "data payload : "
#    #print(payload)
  






#    #arr = [13954, 4369, 37385, 3995, 2556, 46896, 13816, 17865, 40433, 42503, 27740, 14980, 22323, 27920, 48381, 40456, 58866, 60412, 36991, 30730, 14601, 31475, 50583, 57144, 18332, 46140, 47181, 62996, 19071, 30753, 55953, 62831, 8814, 44566, 2191, 16703, 36414, 55831, 28696, 43850]
#    #samples = op.operation.numToBinary(arr)

#    besar_segmen = 2
#    threshold = 200




   

#        ########### DECODING ###############







