import random
import numpy
import math
import operation
import Helper

def f(x):
    return math.ceil(float(x)/2)
def g(x):
   return  2*f(x)-x




def rdei(angka_input):
    angka = abs(angka_input)
    if angka>3:
        rd = angka - pow(2,((math.floor(math.log(angka,2)))-1))  - pow(2,(math.floor(math.log(angka,2))-2))
        flag =0
        if math.pow(2,(math.floor(math.log(angka,2)))) / math.pow(2,(math.floor(math.log(rd,2)))) == 4:
            flag = 1
        if math.pow(2,(math.floor(math.log(angka,2)))) / math.pow(2,(math.floor(math.log(rd,2)))) == 1:
            flag = 2
    else:
        rd = angka
        flag = 3
    if(angka_input<0):
        return (-rd,flag)
    else:
        return(rd,flag)


def inv_rdei(angka_input,flag):
    angka = abs(angka_input)
    if flag ==1:
        rd = angka + pow(2,(math.floor(math.log(angka,2))))  + pow(2,(math.floor(math.log(angka,2))+1))
    elif flag ==2:
        rd = angka + pow(2,(math.floor(math.log(angka,2))-1))  + pow(2,(math.floor(math.log(angka,2))-2))
    elif flag ==0:
        rd = angka + pow(2,(math.floor(math.log(angka,2))-1))  + pow(2,(math.floor(math.log(angka,2))))
    else:
        rd =angka
    if(angka_input<0):
        return -rd
    else:
        return rd

def checkThreshold(waveArray,threshold):
     flag=0
     n = len(waveArray)-1
     for i in range(n):
        diff = waveArray[i+1]-waveArray[0]
        (rdiff,rflag) = rdei(diff)
        if(abs(rdiff)>threshold):
            #print(rdiff)
            flag = 1
     return flag

def checkBlock(waveArray):
    flag=0
    n = len(waveArray)-1
    for i in range(n):
        diff = waveArray[i+1]-waveArray[0]
        (rdiff,rflag) = rdei(diff)
        if rdiff+waveArray[0] <255 or waveArray[0]+rdiff>0:
            ri =  (2*rdiff)+1
            #print(waveArray[0]+ ri)
            if waveArray[0]+ ri <=0 or waveArray[0]+ri >=255:
                flag = 2
        #        #print(str(waveArray[0]+ ri) + "kurang" )
        #        ri2 =  (2*math.floor((rdiff/2)))+1
        #        if waveArray[0]+ri2 <0 or waveArray[0]+ri2 >255:
        #            flag = 2
        #        else:
        #            flag = 1
        #else:
        #    flag = 2
            #print(rdiff+waveArray[0])

        #else:
        #    if waveArray[0]-rdiff >255 or waveArray[0]+rdiff<0:
        #        #print(rdiff+waveArray[0])
        #        flag = 1
    if(flag == 1):
        for i in range(n):
            diff = waveArray[i+1]-waveArray[0]
            (rdiff,rflag) = rdei(diff)
            if (2*math.floor((rdiff/2))) + 1 != rdiff - 1:
                flag ==2    
    #print("flag:" +str(flag))   
    return flag 
    

def encode_block(waveArray,message,validflag):
    flag = 0 
    n = len(waveArray)-1
    diffs = []
    encoded = []
    mapFlag=[]
    for i in range(n):
        diff = waveArray[i+1]-waveArray[0]
        (rdiff,flag) = rdei(diff)
        #if(rdiff == 0.25):
        #    print("found it master")
        #    print(diff)
        diffs.append(rdiff)
        mapFlag.append(flag)
    encoded.append(waveArray[0])
    for i in range(n):
        if(i<len(message)):
            if validflag == 0:
                #if diffs[i]<0:
                #    ri =  (2*diffs[i])- message[i]
                #else:
                ri =  (2*diffs[i])+ message[i]
                #print(2*diffs[i])
            elif validflag ==1: 
                #if diffs[i]<0:
                #    ri =  (2*math.floor((diffs[i]/2))) - message[i]
                #else:
                ri =  (2*math.floor((diffs[i]/2))) + message[i]
        else:
            if validflag == 0:
                #if diffs[i]<0:
                #    #print diffs[i]
                #    ri =  (2*diffs[i])

                #else:
                ri =  (2*diffs[i])

                #print(2*diffs[i])
            elif validflag ==1: 
                #if diffs[i]<0:
                #    ri =  (2*math.floor((diffs[i]/2))) 
                #else:
                ri =  (2*math.floor((diffs[i]/2)))   


               
        #print(ri)
        #if(ri < 0):
        #    ui =pwaveArray[0]-ri
        #else:
        ui = waveArray[0]+ri
        #if( (ui <0 or ui> 255)  ):
        #    print(waveArray)
        #    print(message)
        #    print validflag
        #    print(waveArray[0])
        #    print(ri)
        #    print("---------------")
        #    raw_input()
       
        encoded.append(ui)
    return (encoded,mapFlag)



def decode_block(waveArray,mapFlag,validFlag):
    wave = []
    message =[]
    wave.append(waveArray[0])
    n = len(waveArray)-1
    for i in range(n):
        diff = waveArray[i+1] -  waveArray[0] 
        w = g(diff)
        #if(w == 1.5):
            #print(diff)
            #print(waveArray[i+1])
            #print(waveArray[0])
        message.append(w)
        if validFlag  == 0:
                rdiff = (diff-w)/2
        elif validFlag==1:
                rdiff = (diff-w)
        #print(rdiff)
        realdiff=inv_rdei(rdiff,mapFlag[i]) 
        #print(realdiff)
        x = waveArray[0] + realdiff
        wave.append(x)
    return (wave,message)
           

def encode(waveArray,message,segLength,threshold):
    counter_seg =0
    counter_msg = 0
    encoded =[]
    n = len(waveArray)
    locMap=[]
    reducedMap = []
    for x in range (n/segLength):
        seg = waveArray[counter_seg:counter_seg+segLength]
        counter_seg += segLength
        thres = checkThreshold(seg,threshold)
        if thres==0 :
            flag = checkBlock(seg)
            #print(flag)
            if flag!=2 :
                locMap.append(flag)
                msg_block = message[counter_msg:counter_msg+(segLength-1)]
                #print(msg_block)
                counter_msg +=(segLength-1)

                (seg_encoded,r)=encode_block(seg,msg_block,flag)
                #print(seg_encoded)
                encoded.extend(seg_encoded)
                reducedMap.extend(r)
            else:
                encoded.extend(seg)
                locMap.append(2);
        else:
            encoded.extend(seg)
            locMap.append(2);
       
       
    if(n%segLength != 0):
        encoded.extend(waveArray[-(n%segLength):])

    encoded = [int(i) for i in encoded]
    return(encoded,locMap,reducedMap)


def decode(waveArray,segLength,locMap,reducedMap):
    #print(len(locMap))
    #print(len(reducedMap))
    decoded =[]
    messages=[]
    n = len(waveArray)
    seg_counter =0
    flag_counter =0
    reduce_counter =0
    for x in range(n/segLength):
        seg = waveArray[seg_counter:seg_counter+segLength]
       # print(seg)
        if locMap[flag_counter] == 0:
            rmap = reducedMap[reduce_counter:reduce_counter+(segLength-1)]
            (w,m) = decode_block(seg,rmap,locMap[flag_counter])
           # print(seg)
           # print w
           # print m
            decoded.extend(w)
            messages.extend(m)
            reduce_counter+=(segLength-1)
        else :
            decoded.extend(seg)
        flag_counter+=1
        seg_counter+=segLength
    if(n%segLength != 0):
        decoded.extend(waveArray[-(n%segLength):])

    decoded = [int(i) for i in decoded]
    messages = [int(i) for i in messages]
    return(decoded,messages)
       

def checkCapacity(waveArray,segLength,threshold):
    capacity = 0
    counter = 0
    for x in range (len(waveArray)/segLength):
        seg = waveArray[counter:counter+segLength]
        counter += segLength
        flag = checkBlock(seg)
        flag2 = checkThreshold(seg,threshold)
        if (flag == 1 or flag == 0) and flag2!=1:
            capacity+=(segLength-1)

    if(capacity <0):capacity =0
    return capacity



if __name__ == "__main__":
    wave = Helper.WavIO.open("D:\coba16.wav")
    samples = operation.operation.numToBinary(wave.samples)
    (M1,M2,P) = operation.operation.intel_partition(samples,2)
    intM1 = operation.operation.binaryTonum(M1)
    intM2 = operation.operation.binaryTonum(M2)
    print(len(intM1))
    print(len(intM2))
    check1=checkCapacity(intM1,20,5)
    check2=checkCapacity(intM2,20,5)
    print(check1)
    print(check2)

    #a = [200,32,112,221,187]



    #arr = [86, 202, 252, 156, 132, 66, 28, 117, 124, 43, 55, 105, 240, 142, 116, 103, 13, 219, 19, 38, 147, 179, 91, 146, 214, 234, 10, 152, 12, 42, 24, 14, 138, 181, 111, 14, 39, 141, 6, 4, 28, 25, 219, 102, 34, 217, 219, 10, 249, 129, 230, 228, 20, 25, 4, 171, 30, 123, 155, 120, 67, 93, 92, 50, 97, 56, 2, 115, 29, 208, 207, 35, 42, 112, 168, 185, 53, 64, 228, 46, 22, 29, 162, 60, 124, 109, 165, 239, 95, 187, 192, 43, 31, 156, 34, 147, 179, 190, 0, 119, 163, 194, 121, 43, 205, 148, 248, 115, 32, 144, 52, 194, 186, 201, 19, 82, 105, 77, 3, 113, 233, 177, 43, 52, 139, 182, 80, 172, 52, 69, 64, 86, 192, 222, 199, 110, 208, 130, 24, 155, 243, 144, 24, 133, 58, 52, 1, 243, 46, 81, 247, 204, 237, 89, 29, 20, 31, 145, 101, 122, 191, 100, 192, 240, 198, 187, 8, 144, 156, 137, 243, 26, 239, 192, 24, 37, 117, 40, 8, 174, 185, 55, 160, 115, 56, 230, 242, 243, 21, 84, 158, 251, 116, 196, 247, 225, 124, 15, 184, 171, 72, 254, 36, 74, 23, 30, 128, 202, 99, 248, 36, 63, 182, 138, 152, 135, 176, 253, 149, 186, 194, 214, 219, 183, 59, 112, 37, 118, 197, 183, 68, 181, 97, 31, 36, 188, 181, 179, 93, 5, 232, 67, 245, 244, 227, 252, 8, 250, 188, 129, 155, 151, 84, 11, 95, 105, 147, 42, 173, 80, 24, 39, 70, 162, 158, 162, 135, 236, 22, 207, 172, 219, 2, 92, 187, 63, 20, 213, 13, 157, 198, 188, 223, 71, 70, 203, 231, 235, 150, 214, 117, 66, 235, 5, 26, 118, 124, 234, 194, 15, 130, 212, 251, 48, 25, 142, 51, 84, 166, 29, 127, 205, 38, 57, 6, 4, 51, 74, 17, 15, 176, 144, 76, 231, 178, 239, 181, 123, 202, 145, 223, 220, 245, 148, 0, 10, 241, 197, 208, 160, 178, 169, 107, 212, 59, 1, 68, 107, 107, 46, 206, 32, 6, 251, 226, 191, 146, 165, 225, 10, 170, 19, 27, 81, 98, 205, 67, 54, 117, 202, 172, 157, 239, 227, 133, 82, 117, 153, 1, 90, 86, 23, 166, 76, 108, 231, 227, 183, 145, 137, 73, 80, 95, 243, 8, 252, 139, 62, 11, 16, 108, 43, 102, 147, 52, 107, 70, 251, 95, 81, 133, 10, 176, 71, 4, 31, 165, 37, 164, 92, 186, 35, 175, 126, 234, 3, 127, 74, 205, 171, 187, 216, 203, 158, 134, 197, 79, 169, 103, 118, 130, 67, 72, 230, 194, 211, 103, 126, 87, 120, 11, 241, 144, 255, 188, 98, 3, 110, 208, 222, 231, 60, 126, 200, 165, 251, 27, 124, 136, 219, 198, 21, 79, 78, 157, 166, 246, 6, 1, 50, 222, 12, 9, 236, 44, 106, 90, 85, 232, 227, 184, 93, 35, 83, 77, 200, 142, 104, 177, 165, 88, 207, 236, 125, 148, 179, 137, 94, 140, 24, 240, 85, 163, 120, 78, 113, 232, 25, 95, 246, 123, 179, 79, 94, 148, 118, 66, 98, 0, 244, 226, 124, 49, 215, 121, 2, 172, 17, 244, 5, 126, 163, 89, 12, 52, 51, 123, 70, 98, 178, 206, 205, 23, 159, 182, 159, 13, 9, 4, 165, 95, 246, 234, 184, 113, 169, 124, 166, 218, 92, 140, 220, 13, 2, 121, 3, 41, 29, 132, 248, 212, 103, 127, 197, 236, 217, 140, 99, 97, 138, 228, 127, 148, 202, 172, 64, 233, 251, 119, 33, 152, 176, 15, 232, 114, 65, 211, 130, 195, 125, 155, 48, 235, 131, 126, 34, 61, 99, 37, 2, 103, 154, 219, 191, 177, 249, 92, 251, 200, 1, 13, 211, 237, 86, 143, 113, 65, 236, 123, 65, 10, 119, 206, 25, 0, 98, 93, 83, 30, 214, 41, 63, 114, 218, 114, 194, 228, 213, 156, 180, 135, 81, 142, 245, 166, 154, 194, 1, 219, 4, 233, 180, 26, 172, 60, 69, 96, 154, 202, 231, 165, 226, 251, 158, 117, 145, 73, 129, 91, 213, 42, 186, 254, 241, 143, 128, 23, 228, 14, 13, 7, 111, 197, 249, 244, 99, 5, 175, 136, 150, 201, 27, 114, 222, 76, 208, 30, 136, 4, 80, 147, 211, 255, 19, 249, 78, 149, 80, 232, 176, 254, 147, 139, 147, 36, 210, 223, 136, 24, 21, 67, 14, 203, 5, 117, 223, 165, 124, 158, 254, 203, 153, 19, 75, 140, 27, 241, 104, 249, 173, 250, 191, 252, 106, 29, 206, 196, 223, 66, 184, 36, 255, 2, 243, 2, 181, 125, 115, 114, 56, 35, 126, 228, 145, 216, 154, 157, 145, 209, 110, 78, 63, 58, 67, 72, 58, 58, 140, 52, 53, 190, 147, 38, 225, 254, 174, 11, 216, 134, 118, 77, 1, 181, 139, 162, 83, 22, 150, 169, 237, 180, 52, 238, 89, 26, 196, 240, 8, 12, 238, 224, 1, 204, 241, 141, 190, 69, 85, 121, 206, 9, 74, 118, 0, 139, 170, 252, 224, 150, 138, 99, 53, 95, 58, 219, 18, 70, 145, 137, 72, 96, 45, 38, 55, 74, 26, 92, 8, 74, 146, 105, 88, 217, 255, 244, 51, 78, 52, 243, 33, 89, 129, 124, 247, 35, 102, 49, 137, 104, 172, 117, 70, 104, 166, 50, 113, 208, 225, 149, 243, 49, 181, 244, 210, 88, 23, 123, 100, 60, 251, 85, 71, 162, 194, 230, 204, 84, 121, 124, 3, 169, 206, 35, 137, 29, 192, 186, 94, 0, 197, 163, 189, 108, 69, 233, 63, 222, 250, 198, 223, 217, 177, 8, 104, 63, 188, 105, 42, 249, 75, 241, 41, 60, 1, 150, 240, 153, 120, 61, 175, 85, 139, 201, 185, 47, 191, 119, 78, 212, 167, 172, 195, 11, 136, 135, 33, 39, 32, 43, 46, 4, 188, 42, 209, 188, 89, 15, 116, 30, 131, 220, 161, 26, 69, 8, 14, 37, 74, 186,186];
    #arr =[2, 0, 1, 1, 0, 0, 0, 0, 0, 0]
    #arr= [0,1]
    #caps = checkCapacity(arr,10,200)
    #print(caps)
    message = [1,0,1,0,1,1,1,1,1]
    (encoded,locmap,reducemap)= encode(intM1,message,20,5)
    #(encoded,reducemap) = encode_block(arr,message,cap)
    #print(encoded)
    #print(reducemap)
    ##print(locmap)
    ##print(reducemap)

    #(wave,message2) = decode_block(encoded,reducemap,cap)
    (wave2,message2) = decode(encoded,20,locmap,reducemap)
    #print(len(wave))
    #print(len(intM1))
    print(message2[:9])
    #print(wave)
    if wave2 == intM1:
        print("aman")
    else:
        print("ga aman")

    #print(wave)

    #wave = [int(i) for i in wave]


    #errors_number = [0 for i in range(100)]
    #for i in range(len(wave)):
    #    if(wave[i] != intM1[i]):
    #        errors_number[int(wave[i])]+=1
    #        errors_number[intM1[i]]+=1


    #for idx,i in enumerate(errors_number):
    #    if(i!=0):
    #        print(idx)
    #        print(i)
    #        print("=========")

