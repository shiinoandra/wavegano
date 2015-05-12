import random
import numpy
import math
import Helper
import operation

def f(x):
    return math.ceil(float(x)/2)
def h(x):
    return math.floor(float(x)/2)
def harr(arrX):
    return [h(x) for x in arrX]
def g(x):
   return  2*f(x)-x

def a(arrX):
    avg = float(sum(arrX))/len(arrX)
    if(avg - math.floor(avg) < 0.5):
        return math.floor(avg)
    else:
        return math.ceil(avg)
#def v(arrX):
#    return numpy.var(arrX)

def v(arrX):
    sum  = 0
    for x in arrX:
        mean = a(arrX)
        val = pow((x -mean),2)
        sum+=val
    retval = math.sqrt(sum)
    return retval

#def vh(arrX):
#    hx = [h(x) for x in arrX]
#    return numpy.var(hx)

def vh(arrX):
    sum  = 0
    for x in arrX:
        val = pow((h(x) - a(harr(arrX))),2)
        sum+=val
    retval = math.sqrt(sum)
    return retval

def ha(arrX):
    return [h(x) for x in arrX]



def checkA(waveArray):
    flag = True
    for wave in waveArray:
        if wave > 255 or wave <0:
            flag = False
    return flag

def checkD(WaveArray):
    flag = True
    n = len(WaveArray)-1
    if(checkA(WaveArray) == False):
        flag = False
        return flag
    else:
        for i in range(n+1):
            c = WaveArray[i] - f(a(WaveArray))
            if (  c<0 or c > 127):
                flag = False
        d = 2*WaveArray[n] - a(WaveArray)
        if(d <0 and d >255):
            flag = False
        return flag

        

def checkBlock(waveArray,threshold):
    # 0 = Ot (unchanged)
    # 1 = Et (embeddable)
    # 2 = Ct (changeable)
    flag =0
   # print("v array : "+ str(v(waveArray)))
   # print("vh array : "+ str(vh(waveArray)))

    if( checkD(waveArray) == True and v(waveArray) < threshold):
        flag = 1
    elif(checkA(waveArray) == True and vh(waveArray) < threshold):
        flag = 2
    else:
        flag = 0
    return flag

def encode_block(waveArray,message):
    flag = 0 
    n = len(waveArray)-1
    encoded = []
    for i in range(len(waveArray)-1):
        if(i<len(message)):
            w = 2*waveArray[i] - 2*f(a(waveArray))+ int(message[i])
            encoded.append(w)
        else:
            w = 2*waveArray[i] - 2*f(a(waveArray)) 
            encoded.append(w)
    wn = 2* waveArray[n] -  a(waveArray)
    encoded.append(wn)
    encoded = [int(e) for e in encoded]
    return encoded

def decode_block(waveArray):
    wave = []
    message =[]
    n = len(waveArray)-1
    for i in range(n):
            w = g(waveArray[i])
            message.append(w)
            x = h(waveArray[i]) + a(ha(waveArray)) + g(waveArray[n]) 
            wave.append(x)
    xn = h(waveArray[n]) + a(ha(waveArray)) + g(waveArray[n])
    wave.append(xn)
    return (wave,message)

def encode(waveArray,message,segLength,threshold):
    counter_seg =0
    counter_msg = 0
    encoded =[]
    n = len(waveArray)
    locMap=[]
    for x in range (len(waveArray)/segLength):
        seg = waveArray[counter_seg:counter_seg+segLength]
        counter_seg += segLength
        flag = checkBlock(seg,threshold)
        locMap.append(flag)
        if flag ==1:
            msg_block = message[counter_msg:counter_msg+(segLength-1)]
            #print(msg_block)
            #print(seg)
            counter_msg +=(segLength-1)
            seg_encoded =encode_block(seg,msg_block)
            #print(seg_encoded)
            encoded.extend(seg_encoded)
        elif flag ==2:
            encoded.extend(seg)
        else:
            encoded.extend(seg)
    if(n%segLength != 0):
        encoded.extend(waveArray[-(n%segLength):])
    return(encoded,locMap)


def decode(waveArray,segLength,locMap):
    decoded =[]
    messages=[]
    n = len(waveArray)
    seg_counter =0
    flag_counter =0
    for x in range(n/segLength):
        seg = waveArray[seg_counter:seg_counter+segLength]
        if locMap[flag_counter] == 1:
            (w,m) = decode_block(seg)
            #print(seg)
            #print w
            #print m
            decoded.extend(w)
            messages.extend(m)
        else :
            decoded.extend(seg)
        flag_counter+=1
        seg_counter+=segLength

    if(n%segLength != 0):
        decoded.extend(waveArray[-(n%segLength):])
    return(decoded,messages)
       

def checkCapacity(waveArray,segLength,threshold):
    counter = 0
    flags=[0 for i in range(3)]
    for x in range (len(waveArray)/segLength):
        seg = waveArray[counter:counter+segLength]
        counter += segLength
        flag = checkBlock(seg,threshold)
        flags[flag]+=1
    return(flags[1]*(segLength-1))
       


#wave = Helper.WavIO.open("D:\coba.wav")
#samples = operation.operation.numToBinary(wave.samples)
#(M1,M2,P) = operation.operation.intel_partition(samples,2)
#intM1 = operation.operation.binaryTonum(M1)
#intM2 = operation.operation.binaryTonum(M2)
#check1=checkCapacity(intM1,20,3)
#check2=checkCapacity(intM2,20,3)
#print(check1)
#print(check2)

#print(len(intM1))


##arr = [86, 202, 252, 156, 132, 66, 28, 117, 124, 43, 55, 105, 240, 142, 116, 103, 13, 219, 19, 38, 147, 179, 91, 146, 214, 234, 10, 152, 12, 42, 24, 14, 138, 181, 111, 14, 39, 141, 6, 4, 28, 25, 219, 102, 34, 217, 219, 10, 249, 129, 230, 228, 20, 25, 4, 171, 30, 123, 155, 120, 67, 93, 92, 50, 97, 56, 2, 115, 29, 208, 207, 35, 42, 112, 168, 185, 53, 64, 228, 46, 22, 29, 162, 60, 124, 109, 165, 239, 95, 187, 192, 43, 31, 156, 34, 147, 179, 190, 0, 119, 163, 194, 121, 43, 205, 148, 248, 115, 32, 144, 52, 194, 186, 201, 19, 82, 105, 77, 3, 113, 233, 177, 43, 52, 139, 182, 80, 172, 52, 69, 64, 86, 192, 222, 199, 110, 208, 130, 24, 155, 243, 144, 24, 133, 58, 52, 1, 243, 46, 81, 247, 204, 237, 89, 29, 20, 31, 145, 101, 122, 191, 100, 192, 240, 198, 187, 8, 144, 156, 137, 243, 26, 239, 192, 24, 37, 117, 40, 8, 174, 185, 55, 160, 115, 56, 230, 242, 243, 21, 84, 158, 251, 116, 196, 247, 225, 124, 15, 184, 171, 72, 254, 36, 74, 23, 30, 128, 202, 99, 248, 36, 63, 182, 138, 152, 135, 176, 253, 149, 186, 194, 214, 219, 183, 59, 112, 37, 118, 197, 183, 68, 181, 97, 31, 36, 188, 181, 179, 93, 5, 232, 67, 245, 244, 227, 252, 8, 250, 188, 129, 155, 151, 84, 11, 95, 105, 147, 42, 173, 80, 24, 39, 70, 162, 158, 162, 135, 236, 22, 207, 172, 219, 2, 92, 187, 63, 20, 213, 13, 157, 198, 188, 223, 71, 70, 203, 231, 235, 150, 214, 117, 66, 235, 5, 26, 118, 124, 234, 194, 15, 130, 212, 251, 48, 25, 142, 51, 84, 166, 29, 127, 205, 38, 57, 6, 4, 51, 74, 17, 15, 176, 144, 76, 231, 178, 239, 181, 123, 202, 145, 223, 220, 245, 148, 0, 10, 241, 197, 208, 160, 178, 169, 107, 212, 59, 1, 68, 107, 107, 46, 206, 32, 6, 251, 226, 191, 146, 165, 225, 10, 170, 19, 27, 81, 98, 205, 67, 54, 117, 202, 172, 157, 239, 227, 133, 82, 117, 153, 1, 90, 86, 23, 166, 76, 108, 231, 227, 183, 145, 137, 73, 80, 95, 243, 8, 252, 139, 62, 11, 16, 108, 43, 102, 147, 52, 107, 70, 251, 95, 81, 133, 10, 176, 71, 4, 31, 165, 37, 164, 92, 186, 35, 175, 126, 234, 3, 127, 74, 205, 171, 187, 216, 203, 158, 134, 197, 79, 169, 103, 118, 130, 67, 72, 230, 194, 211, 103, 126, 87, 120, 11, 241, 144, 255, 188, 98, 3, 110, 208, 222, 231, 60, 126, 200, 165, 251, 27, 124, 136, 219, 198, 21, 79, 78, 157, 166, 246, 6, 1, 50, 222, 12, 9, 236, 44, 106, 90, 85, 232, 227, 184, 93, 35, 83, 77, 200, 142, 104, 177, 165, 88, 207, 236, 125, 148, 179, 137, 94, 140, 24, 240, 85, 163, 120, 78, 113, 232, 25, 95, 246, 123, 179, 79, 94, 148, 118, 66, 98, 0, 244, 226, 124, 49, 215, 121, 2, 172, 17, 244, 5, 126, 163, 89, 12, 52, 51, 123, 70, 98, 178, 206, 205, 23, 159, 182, 159, 13, 9, 4, 165, 95, 246, 234, 184, 113, 169, 124, 166, 218, 92, 140, 220, 13, 2, 121, 3, 41, 29, 132, 248, 212, 103, 127, 197, 236, 217, 140, 99, 97, 138, 228, 127, 148, 202, 172, 64, 233, 251, 119, 33, 152, 176, 15, 232, 114, 65, 211, 130, 195, 125, 155, 48, 235, 131, 126, 34, 61, 99, 37, 2, 103, 154, 219, 191, 177, 249, 92, 251, 200, 1, 13, 211, 237, 86, 143, 113, 65, 236, 123, 65, 10, 119, 206, 25, 0, 98, 93, 83, 30, 214, 41, 63, 114, 218, 114, 194, 228, 213, 156, 180, 135, 81, 142, 245, 166, 154, 194, 1, 219, 4, 233, 180, 26, 172, 60, 69, 96, 154, 202, 231, 165, 226, 251, 158, 117, 145, 73, 129, 91, 213, 42, 186, 254, 241, 143, 128, 23, 228, 14, 13, 7, 111, 197, 249, 244, 99, 5, 175, 136, 150, 201, 27, 114, 222, 76, 208, 30, 136, 4, 80, 147, 211, 255, 19, 249, 78, 149, 80, 232, 176, 254, 147, 139, 147, 36, 210, 223, 136, 24, 21, 67, 14, 203, 5, 117, 223, 165, 124, 158, 254, 203, 153, 19, 75, 140, 27, 241, 104, 249, 173, 250, 191, 252, 106, 29, 206, 196, 223, 66, 184, 36, 255, 2, 243, 2, 181, 125, 115, 114, 56, 35, 126, 228, 145, 216, 154, 157, 145, 209, 110, 78, 63, 58, 67, 72, 58, 58, 140, 52, 53, 190, 147, 38, 225, 254, 174, 11, 216, 134, 118, 77, 1, 181, 139, 162, 83, 22, 150, 169, 237, 180, 52, 238, 89, 26, 196, 240, 8, 12, 238, 224, 1, 204, 241, 141, 190, 69, 85, 121, 206, 9, 74, 118, 0, 139, 170, 252, 224, 150, 138, 99, 53, 95, 58, 219, 18, 70, 145, 137, 72, 96, 45, 38, 55, 74, 26, 92, 8, 74, 146, 105, 88, 217, 255, 244, 51, 78, 52, 243, 33, 89, 129, 124, 247, 35, 102, 49, 137, 104, 172, 117, 70, 104, 166, 50, 113, 208, 225, 149, 243, 49, 181, 244, 210, 88, 23, 123, 100, 60, 251, 85, 71, 162, 194, 230, 204, 84, 121, 124, 3, 169, 206, 35, 137, 29, 192, 186, 94, 0, 197, 163, 189, 108, 69, 233, 63, 222, 250, 198, 223, 217, 177, 8, 104, 63, 188, 105, 42, 249, 75, 241, 41, 60, 1, 150, 240, 153, 120, 61, 175, 85, 139, 201, 185, 47, 191, 119, 78, 212, 167, 172, 195, 11, 136, 135, 33, 39, 32, 43, 46, 4, 188, 42, 209, 188, 89, 15, 116, 30, 131, 220, 161, 26, 69, 8, 14, 37, 74, 186, 54];
##arr = [99, 231, 66, 61, 212, 24, 167, 177, 128, 233]
##print(checkCapacity(arr,3,255))
#message = [1]
#(encoded,locmap)= encode(intM1,message,3,255)
##print(len(encoded))
##print(locmap)

#(wave,message) = decode(encoded,3,locmap)
#wave =[int(i) for i in wave] 
#count =0


