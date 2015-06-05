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
import matplotlib.pyplot as plt
numpy.set_printoptions(threshold=numpy.nan)


#def encode(payload_path,cover_path,threshold,segment_size,partition_segment_size,method):
#    file_name = cover_path.split("\\")[len(cover_path.split("\\"))-1]
#    path = cover_path.replace(file_name,'')
#    print(" PROSES ENCODING ")
#    print(" METODE YANG DIGUNAKAN : " + method)
#    payload = Helper.payloadIO.open(payload_path)
#    bin_payload = op.operation.stringToBinary(payload)
#    print "besar payload : "
#    payload_size = len(bin_payload)
#    print(payload_size) 
#    medium = Helper.WavIO.open(cover_path)
#    print "bitrate: "
#    print(medium.bitrate)

#    samples = op.operation.numToBinary(medium.samples)
#    (M1,M2,Partisi) = op.operation.intel_partition(samples,partition_segment_size)
#    intM1 = op.operation.binaryTonum(M1)
#    intM2 = op.operation.binaryTonum(M2)
#    if method == "GDE" :
#        kapasitas_M1 = GDE.checkCapacity(intM1,segment_size,threshold)
#        kapasitas_M2 = GDE.checkCapacity(intM2,segment_size,threshold)
#    elif method == "GRDEI":
#        kapasitas_M1 = GRDEI.checkCapacity(intM1,segment_size,threshold)
#        kapasitas_M2 = GRDEI.checkCapacity(intM2,segment_size,threshold)
#    print(" kapasitas segmen 1 : " + str(kapasitas_M1))
#    print(" kapasitas segmen 2 : " + str(kapasitas_M2))
#    capacity = kapasitas_M1+kapasitas_M2
#    print "Kapasitas penyimpanan :"
#    print(capacity)
#    if capacity >= payload_size:
#        print "stegano dapat dilakukan"
#        payload_seg1 = bin_payload[:kapasitas_M1]
#        payload_seg2 = bin_payload[kapasitas_M1:len(bin_payload)]
#        if method == "GDE" :
#            (encoded_1,locMap_1) = GDE.encode(intM1,payload_seg1,segment_size,threshold)
#            (encoded_2,locMap_2) = GDE.encode(intM2,payload_seg2,segment_size,threshold)
#        elif method == "GRDEI":
#            (encoded_1,locMap_1,reduceMap_1) = GRDEI.encode(intM1,payload_seg1,segment_size,threshold)
#            (encoded_2,locMap_2,reduceMap_2) = GRDEI.encode(intM2,payload_seg2,segment_size,threshold)
#        encoded_1 = op.operation.numToBinary(encoded_1)
#        encoded_2 = op.operation.numToBinary(encoded_2)
#        for i in range(len(encoded_1)):
#            encoded_1[i]=encoded_1[i][8:16] 
#        for i in range(len(encoded_2)):
#            encoded_2[i]=encoded_2[i][8:16] 
#        encoded_1_bin = numpy.array(encoded_1,dtype=int)
#        encoded_2_bin = numpy.array(encoded_2,dtype=int)
#        _M = op.operation.reconstructPartition(encoded_1_bin,encoded_2_bin,Partisi)
#        _M_int2= numpy.asarray(op.operation.binaryTonum(_M),dtype=numpy.uint16)
#        _M_int = numpy.asarray(op.operation.binaryTonum(_M),dtype=numpy.int16)
#        new_wav = Wave.Wave(method+"_encoded_"+str(file_name))
#        new_wav.samples = _M_int
#        new_wav.bitrate = medium.bitrate

#        time_axis = numpy.linspace(0,len(medium.samples)/medium.bitrate,num=len(medium.samples))
#        plt.subplot(3,1,1)
#        plt.title("perbandingan wav asli dan hasil encode")
#        plt.plot(time_axis,numpy.array(medium.samples,dtype= "int16"))
#        plt.ylabel("WAV asli")
#        plt.subplot(3,1,2)
#        plt.plot(time_axis,numpy.array(_M_int,dtype= "int16"))
#        plt.ylabel("Hasil Encode")
#        plt.subplot(3,1,3)
#        plt.plot(time_axis,numpy.array(_M_int,dtype= "int16"))
#        plt.subplot(3,1,3)
#        plt.plot(time_axis,numpy.array(medium.samples,dtype= "int16"))

#        plt.ylabel("perbandingan")
#        plt.xlabel("Waktu (s)")
#        plt.savefig("original-encoded.png")
#        #print(medium.samples)
#        #raw_input()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
#        #print(new_wav.samples)
#        #new_wav.print_info()
#        #medium.print_info()
#        Helper.WavIO.write(path,new_wav)
#        if method == "GDE" :
#            return(locMap_1,locMap_2,Partisi)
#        elif method == "GRDEI":
#            return(locMap_1,locMap_2,reduceMap_1,reduceMap_2,Partisi)

#    else:
#        print "kapasitas tidak mencukupi"
#        return -1 


def encode(intM1,intM2,payload_seg1,payload_seg2,threshold,segment_size,partition_segment_size,Partisi,method):

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

    if method == "GDE" :
        return(_M_int2,locMap_1,locMap_2,Partisi)
    elif method == "GRDEI":
        return(_M_int2,locMap_1,locMap_2,reduceMap_1,reduceMap_2,Partisi)





def decode(file_path,segment_size,payload_size,method,Partition,locMap_1,locMap_2,reduceMap_1 = None , reduceMap_2 = None):
        file_name = file_path.split("\\")[len(file_path.split("\\"))-1]
        path = file_path.replace(file_name,'')
        print(" PROSES DECODING ")
        print(" METODE YANG DIGUNAKAN : " )
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
        print(len(message_decoded))
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
        plt.clf()
        time_axis = numpy.linspace(0,len(medium_encoded.samples)/medium_encoded.bitrate,num=len(medium_encoded.samples))
        plt.subplot(2,1,1)
        plt.title("perbandingan hasil encode  dan hasil decode")
        plt.plot(time_axis,numpy.array(medium_encoded.samples,dtype= "int16"))
        plt.ylabel("WAV encoded")
        plt.subplot(2,1,2)
        plt.plot(time_axis,numpy.array(M__awal,dtype= "int16"))
        plt.ylabel("WAV Hasil Dencode")
        plt.xlabel("Waktu (s)")
        plt.savefig("encoded-decoded.png")
        Helper.WavIO.write(path,new_wav2)

def multilayer_encode(payload_path,cover_path,threshold,segment_size,partition_segment_size,method,n_layer):
    locmap_list = []
    reducemap_list = []
    capacities = []
    payload_sizes = []
    total_capacity = 0
    file_name = cover_path.split("\\")[len(cover_path.split("\\"))-1]
    path = cover_path.replace(file_name,'')
    print(" PROSES ENCODING ")
    print(" METODE YANG DIGUNAKAN : " + str(method))
    payload = Helper.payloadIO.open(payload_path)
    bin_payload = op.operation.stringToBinary(payload)
    print "besar payload : "
    payload_size = len(bin_payload)
    print(payload_size) 
    medium = Helper.WavIO.open(cover_path)
    print "bitrate: "
    print(medium.bitrate)
    audio_sample = medium.samples
    #for i in range(n_layer):
    #    samples = op.operation.numToBinary(audio_sample)
    #    (M1,M2,Partisi) = op.operation.intel_partition(samples,partition_segment_size)
    #    intM1 = op.operation.binaryTonum(M1)
    #    intM2 = op.operation.binaryTonum(M2)
    #    if method == "GDE" :
    #        kapasitas_M1 = GDE.checkCapacity(intM1,segment_size,threshold)
    #        kapasitas_M2 = GDE.checkCapacity(intM2,segment_size,threshold)
    #    elif method == "GRDEI":
    #        kapasitas_M1 = GRDEI.checkCapacity(intM1,segment_size,threshold)
    #        kapasitas_M2 = GRDEI.checkCapacity(intM2,segment_size,threshold)
    #    print(" kapasitas segmen 1 : " + str(kapasitas_M1))
    #    print(" kapasitas segmen 2 : " + str(kapasitas_M2))
    #    capacity = kapasitas_M1+kapasitas_M2
    #    capacities.append((kapasitas_M1,kapasitas_M2))
    #    print "Kapasitas penyimpanan layer ke "+str(i)+":"+str(capacity)
    #    payload_seg1 = [1 for i in range(kapasitas_M1)]
    #    payload_seg2 = [1 for i in range(kapasitas_M2)]
    #    total_capacity+=capacity
    #    audio_sample = encode(intM1,intM2,payload_seg1,payload_seg2,threshold,segment_size,partition_segment_size,Partisi,method)[0]
    #print("total kapasitas "+str(total_capacity))
    #if(total_capacity > payload_size):
    #    print("stegano dapat dilakukan")
    

    #time_axis = numpy.linspace(0,len(medium.samples)/medium.bitrate,num=len(medium.samples))
    #plt.subplot(n_layer+1,1,1)
    #plt.title("perbandingan wav asli dan hasil encode multi-layer")
    #plt.plot(time_axis,numpy.array(medium.samples,dtype= "int16"))
    #plt.ylabel("WAV asli")

    P = op.operation.intel_partition(op.operation.numToBinary(audio_sample),partition_segment_size)[2]
    payload_counter = 0
    for i in range(n_layer):
        print("layer ke " + str(i))
        samples = op.operation.numToBinary(audio_sample)
        (M1,M2,Partisi) = op.operation.intel_partition(samples,partition_segment_size,P)
        intM1 = op.operation.binaryTonum(M1)
        intM2 = op.operation.binaryTonum(M2)
        if method == "GDE" :
            kapasitas_M1 = GDE.checkCapacity(intM1,segment_size,threshold)
            kapasitas_M2 = GDE.checkCapacity(intM2,segment_size,threshold)
        elif method == "GRDEI":
            kapasitas_M1 = GRDEI.checkCapacity(intM1,segment_size,threshold)
            kapasitas_M2 = GRDEI.checkCapacity(intM2,segment_size,threshold)
        capacities.append((kapasitas_M1,kapasitas_M2))
        kapasitas_total_layer = kapasitas_M1+kapasitas_M2
        total_capacity += kapasitas_total_layer
        if((payload_size - payload_counter) > kapasitas_total_layer):
            payload_i = bin_payload[payload_counter:kapasitas_total_layer]
            payload_sizes.append(kapasitas_total_layer)
            payload_counter+=kapasitas_total_layer
            print(len(payload_i))
        else:
            payload_i = bin_payload[payload_counter:payload_size]
            payload_sizes.append((payload_size-payload_counter))
            payload_counter+=(payload_size-payload_counter)
            print(len(payload_i))

        payload_seg1 = payload_i[:kapasitas_M1]
        print(len(payload_seg1))
        payload_seg2 = payload_i[kapasitas_M1:len(payload_i)]
        print(len(payload_seg2))
        if method == "GDE" :
            (audio_sample,locMap_1,locMap_2,Partisi)= encode(intM1,intM2,payload_seg1,payload_seg2,threshold,segment_size,partition_segment_size,P,method)
            locmap_list.append((locMap_1,locMap_2))
        elif method == "GRDEI":
            (audio_sample,locMap_1,locMap_2,reduceMap_1,reduceMap_2,Partisi) =  encode(intM1,intM2,payload_seg1,payload_seg2,threshold,segment_size,partition_segment_size,P,method)
            locmap_list.append((locMap_1,locMap_2))
            reducemap_list.append((reduceMap_1,reduceMap_2))
            #audio_sample =  numpy.asarray(audio_sample2,dtype="uint16")
        #plt.subplot(n_layer+1,1,i+2)
        #plt.plot(time_axis,numpy.array(audio_sample,dtype= "int16"))
        #plt.ylabel("Hasil Encode layer ke "+str(i+1))
        #plt.xlabel("Waktu (s)")
        #plt.savefig("original-multiencode-"+str(n_layer)+".png")
    if(payload_counter>=payload_size):
        print("stegano berhasil dilakukan")
        print(total_capacity)
        _M_int = numpy.asarray(audio_sample,dtype=numpy.int16)
        new_wav = Wave.Wave(method+"_encoded_"+str(file_name))
        new_wav.samples = _M_int
        new_wav.bitrate = medium.bitrate
        Helper.WavIO.write(path,new_wav)
        if method == "GDE" :
            return(locmap_list,payload_sizes,P)
        elif method == "GRDEI":
            return(locmap_list,reducemap_list,payload_sizes,P)
    else:
        print("kapasitas tidak mencukupi")

#else:
#    print "kapasitas tidak mencukupi"
#    return -1 
             

def multilayer_decode(file_path,segment_size,payload_sizes,Partition,method,n_layer,locmap_list,reducemap_list = None,):
        full_messages=[]
        file_name = file_path.split("\\")[len(file_path.split("\\"))-1]
        path = file_path.replace(file_name,'')
        print(" PROSES DECODING ")
        print(" METODE YANG DIGUNAKAN : " )
        print(method)
        medium_encoded = Helper.WavIO.open(file_path)
        print "bitrate: "
        print(medium_encoded.bitrate)
        audio_samples = medium_encoded.samples
        for i in range (n_layer):
            print("layer ke " + str(i))
            (locmap_i_1,locmap_i_2) = locmap_list.pop()
            if(method == "GRDEI"):
                (reducemap_i_1,reducemap_i_2) = reducemap_list.pop()
            samples = op.operation.numToBinary(audio_samples)
            (_M1,_M2,P) = op.operation.intel_partition(samples,0,Partition)
            _intM1 = op.operation.binaryTonum(_M1)
            _intM2 = op.operation.binaryTonum(_M2)
            if method == "GDE" :
                (decoded_M1,message1) = GDE.decode(_intM1,segment_size,locmap_i_1)
                (decoded_M2,message2) = GDE.decode(_intM2,segment_size,locmap_i_2)        
            elif method == "GRDEI":
                (decoded_M1,message1) = GRDEI.decode(_intM1,segment_size,locmap_i_1,reducemap_i_1)
                (decoded_M2,message2) = GRDEI.decode(_intM2,segment_size,locmap_i_2,reducemap_i_2)
            message_decoded = []
            message_decoded.extend(message1)
            message_decoded.extend(message2)
            payload_i_size = payload_sizes.pop()
            full_messages.insert(0,message_decoded[0:payload_i_size])
            decoded_1 = op.operation.numToBinary(decoded_M1)
            decoded_2 = op.operation.numToBinary(decoded_M2)
            for i in range(len(decoded_1)):
                decoded_1[i]=decoded_1[i][8:16] 
            for i in range(len(decoded_2)):
                decoded_2[i]=decoded_2[i][8:16] 
            decoded_1_bin = numpy.array(decoded_1,dtype=int)
            decoded_2_bin = numpy.array(decoded_2,dtype=int)
            M_awal = op.operation.reconstructPartition(decoded_1_bin,decoded_2_bin,Partition)
            audio_samples = numpy.asarray(op.operation.binaryTonum(M_awal),dtype=numpy.uint16)
            for i in audio_samples:
                if(i<0):
                    print(i)
        message_write = []
        for i in range(len(full_messages)):
            message_write.extend(full_messages[i])
        message_write = op.operation.revStringToBinary(message_write)
        Helper.payloadIO.write(path+"payload_decoded.txt",message_write)
        new_wav = Wave.Wave(file_name.replace("encoded","decoded"))
        M__awal = numpy.asarray(audio_samples,dtype=numpy.int16)
        new_wav.samples = M__awal
        new_wav.bitrate = medium_encoded.bitrate
        Helper.WavIO.write(path,new_wav)







if __name__ == "__main__":
    #(map1,map2,rmap1,rmap2,p) = encode("D:\\payload.txt","D:\\coba16.wav",100,20,10,"GRDEI")
    (locmap_list,reducemap_list,payload_sizes,partisi) = multilayer_encode("D:\\payload.txt","D:\\coba16.wav",50,20,10,"GRDEI",20)
    #print(len(locmap_list))
   # print(len(reducemap_list))
    multilayer_decode("D:\\GRDEI_encoded_coba16.wav",20,payload_sizes,partisi,"GRDEI",20,locmap_list,reducemap_list)
    #locmap_list.pop()
    #(map1_1,map1_2) = locmap_list.pop()
    #reducemap_list.pop()
    #(rmap1_1,rmap1_2) = reducemap_list.pop()

    #decode("D:\\GRDEI_encoded2_coba16.wav",20,1187,"GRDEI",partisi,map1_1,map1_2,rmap1_1,rmap1_2)
     #print(len(locmap_list),len(reducemap_list))
#   # print "data payload : "
#    #print(payload)
  






#    #arr = [13954, 4369, 37385, 3995, 2556, 46896, 13816, 17865, 40433, 42503, 27740, 14980, 22323, 27920, 48381, 40456, 58866, 60412, 36991, 30730, 14601, 31475, 50583, 57144, 18332, 46140, 47181, 62996, 19071, 30753, 55953, 62831, 8814, 44566, 2191, 16703, 36414, 55831, 28696, 43850]
#    #samples = op.operation.numToBinary(arr)

#    besar_segmen = 2
#    threshold = 200




   

#        ########### DECODING ###############







