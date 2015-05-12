import numpy
import math


def RDE(x , y , hiddenBit):
    flag = 0
    if(x<y):
        flag = 1
        a =x
        x = y
        y =a
    m = math.floor((x+y)/2)
    mapFlag = 0
    d = x-y
    if(d>=2):
        rd = d - pow(2,((math.floor(math.log(d,2)))-1))
        if math.pow(2,(math.floor(math.log(d,2)))) == math.pow(2,(math.floor(math.log(rd,2)))):
            mapFlag=1
    else:
        rd = d
    _d = 2*rd+hiddenBit
    _x = m + math.floor((_d+1)/2)
    _y = m - math.floor(_d/2)


    if(_x <0 or _x >255) or( _y<0 or _y>255):
        return (-1,-1,-1)
    else:
        if (flag ==1 ):
            return (int(_y),int(_x),mapFlag)
        else:
            return (int(_x),int(_y),mapFlag)


def inv_RDE(_x,_y, mapFlag):
    flag = 0
    if(_x<_y):
        flag = 1
        a =_x
        _x = _y
        _y =a
    _d = _x -_y 
    _m = math.floor((_x+_y)/2)
    Bits = [int(x) for x in bin(int(_d))[2:]]
    lsb = Bits[len(Bits)-1]
    rd = (int(operation.binaryArraytoString(Bits),2))
    d  = math.floor(rd/2)
    if(mapFlag != 1):
        if(d>0):
            d = d + pow(2,((math.floor(math.log(d,2)))))
        else:
            d =0
    else:
        if(d>0):
            d = d + pow(2,((math.floor(math.log(d,2)))-1))
        else:
            d=0
    
    x = _m+math.floor((d+1)/2)
    y = _m-math.floor(d/2)

    if(flag == 1):
        return(y,x,lsb)
    else:
        return(x,y,lsb)

def RDE_Array(WaveArray,MessageArray,threshold):
    embedded = []
    reducedMap = []
    locMap1=[0 for i in range(len(WaveArray)/2)]
    locMap2=[0 for i in range(len(WaveArray)/2)]


    M1 = [sample[:8] for sample in WaveArray]
    M2 = [sample[8:] for sample in WaveArray]
    intM1 = [int(operation.binaryArraytoString(sample),2) for sample in M1]
    intM2 = [int(operation.binaryArraytoString(sample),2) for sample in M2]
    print(intM1)
    #print(intM2)
    check = operation.checkCapacity(WaveArray,MessageArray,threshold)
    if(check[2] == 1):
        S1 = MessageArray[:check[0]]
        S2 = MessageArray[check[0]:]
    else:
        print("kapasitas tidak cukup")
    print(S1)
    print(check)
    countM = 0
    for i in range(len(S1)):
        #print(countM)
        while(1):
            try:
                if(abs(intM1[countM]-intM1[countM+1]) <= threshold):
                    newbit = operation.RDE(intM1[countM],intM1[countM+1],S1[i])
                    if(newbit[0] != -1):
                        # print("embedding")
                        # print(newbit)
                        # print(intM1[countM],intM1[countM+1],S1[i])
                        intM1[countM] = newbit[0]
                        intM1[countM+1] = newbit[1]
                        reducedMap.append(newbit[2])
                        locMap1[(countM+1)/2] = 1
                        break
                countM+=2
            except:
                break
        countM+=2

          
    countM = 0
    for i in range(len(S2)):
        #print(countM)
        while(1):
            try:
                if(abs(intM2[countM]-intM2[countM+1]) <= threshold):
                    newbit = operation.RDE(intM2[countM],intM2[countM+1],S2[i])
                    if(newbit[0] != -1):
                        # print("embedding")
                        #print(newbit)
                        #print(intM2[countM],intM2[countM+1],S2[i])
                        intM2[countM] = newbit[0]
                        intM2[countM+1] = newbit[1]
                        reducedMap.append(newbit[2])
                        locMap2[(countM+1)/2] = 1
                        break
                countM+=2
            except:
                break
        countM+=2
    locMap = locMap1.append(locMap2)
    print(intM1)
    print(locMap1)
    return (intM1,intM2,reducedMap,locMap1,locMap2)

def inv_RDE_Array(WaveArray,locMap,reducedMap):
    countM = 0
    countR = 0
    countMap =0
    decoded_M = []
    decoded_S = []
    for i in range(len(WaveArray)):
        try:
            if(locMap[countMap] == 1):
                print("decoding :" + str(WaveArray[countM]) +","+ str(WaveArray[countM+1]))
                result = operation.inv_RDE(WaveArray[countM] , WaveArray[countM+1],reducedMap[countR])
                print(result)
                decoded_M.append(result[0])
                decoded_M.append(result[1])
                decoded_S.append(result[2])
                countR+=1
            else:
                decoded_M.append(WaveArray[countM])
                decoded_M.append(WaveArray[countM+1])
            countM+=2
            countMap+=1
        except:
            continue

    print (decoded_M)
    print (decoded_S)


        #@staticmethod
    #def checkCapacity(WaveArray,threshold):
    #    M1 = [sample[:8] for sample in WaveArray]
    #    M2 = [sample[8:] for sample in WaveArray]
    #    capacity1 =0
    #    capacity2 =0
    #    flag = 1
    #    intM1 = operation.binaryTonum(M1)
    #    intM2 = operation.binaryTonum(M2)
    #    count = 0
    #    for i in range(int(math.ceil(len(intM1)/2))):
    #            if(abs(intM1[count]-intM1[count+1]) <= threshold):
    #                capacity1+=1
    #                overflow_check = operation.RDE(intM1[count],intM1[count+1],1)
    #                if(overflow_check[0] == -1):
    #                    #print(overflow_check)
    #                    capacity1-=1
    #            count+=2

    #    count = 0
    #    for n in range(int(math.ceil(len(intM2)/2))):
    #        try:
    #            if(abs(intM2[count]-intM2[count+1]) <= threshold):
    #                capacity2+=1
    #                overflow_check = operation.RDE(intM2[count],intM2[count+1],1)
    #                if(overflow_check[0] == -1):
    #                    #print(overflow_check)
    #                    capacity2-=1
    #            count+=2
    #        except:
    #            continue
    #   #if(len(MessageArray) > (capacity1 + capacity2)):
    #    #    flag =0
    #    return (capacity1,capacity2,flag)

def checkCapacity(WaveArray,threshold):
    capacity =0
    flag = 1
    count = 0
    for i in range(int(math.ceil(len(WaveArray)/2))):
        try:
            if(abs(WaveArray[count]-WaveArray[count+1]) <= threshold):
                capacity+=1
                overflow_check = operation.RDE(WaveArray[count],WaveArray[count+1],1)
                if(overflow_check[0] == -1):
                    #print(overflow_check)
                    capacity-=1
            count+=2
        except:
            continue
    #if(len(MessageArray) > (capacity1 + capacity2)):
    #    flag =0
    return (capacity,flag)