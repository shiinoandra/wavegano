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

