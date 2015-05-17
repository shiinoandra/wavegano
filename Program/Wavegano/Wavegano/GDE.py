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
    decoded = [int(i) for i in decoded]
    messages = [int(i) for i in messages]
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
       


