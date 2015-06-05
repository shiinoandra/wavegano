import operation  as o
import numpy
import Helper
import GDE
import GRDEI
import RDE
import binascii
import operation as op

numpy.set_printoptions(threshold=numpy.nan)

## tes kapasitas ##


#for i in range(1000):
#    #arr = [random.randint(0,255) for i in range(3)]
#    arr = [192,192,190]
#    check = checkBlock(arr,25)
#    print(check)

#arr  =[19, 90, 198, 106, 84, 188, 129, 70, 70, 23, 11, 65, 18, 218, 53, 30, 199, 147, 204,205,121,242]
#arr_bin = operation.operation.numToBinary(arr)
#(M1,M2,P) = operation.operation.intel_partition(arr_bin,3)
#intM1 = operation.operation.binaryTonum(M1)
#intM2 = operation.operation.binaryTonum(M2)
#print(checkCapacity(intM1,3,30))
#print(checkCapacity(intM2,3,30))
#message ="0001"
#print(intM1)
#(encoded,locmap)= encode(intM1,message,3,30)
#print(encoded)
#print(locmap)
#(decoded,messages)= decode(encoded,3,locmap)
#print(decoded)
#print(messages)


#wa = encode(arr,'111000')
#print(wa)
#decode(wa)

#ax = [15, 7, 16, 17, 4, 14, 15, 5, 7, 20]
#bx = operation.operation.numToBinary(ax)

#wave = Helper.WavIO.open("D:\coba16.wav")
#samples = o.operation.numToBinary(wave.samples)
#(M1,M2,P) = o.operation.intel_partition(samples,2)
#intM1 = o.operation.binaryTonum(M1)
#intM2 = o.operation.binaryTonum(M2)
#check1=checkCapacity(intM1,4,200)
#check2=checkCapacity(intM2,4,200)
#print(check1)
#print(check2)

#check3 = operation.operation.checkCapacity(intM1,200)
#check4 = operation.operation.checkCapacity(intM2,200)
#print(check3)
#print(check4)





## tes partisi dan konstruksi ulang partisi##

#arr = [240, 246, 70, 1, 138, 66, 235, 203, 162, 78, 5, 194, 185, 245, 195, 57, 237, 167, 215, 244, 44, 26, 116, 214, 127, 109, 8, 71, 21, 102, 123, 148, 147, 236, 211, 118, 99, 187, 107, 87, 77, 150, 128, 158, 181, 12, 254, 145, 54, 8, 191, 255, 249, 97, 70, 12, 186, 72, 189, 130, 107, 41, 242, 203, 73, 36, 53, 224, 25, 231, 227, 209, 77, 214, 23, 153, 44, 173, 47, 203, 90, 195, 121, 244, 22, 177, 160, 2, 51, 10, 179, 220, 53, 139, 21, 145, 202, 217, 137, 175, 192, 126, 17, 161, 180, 118, 176, 253, 149, 130, 59, 202, 234, 147, 167, 7, 169, 250, 118, 64, 56, 212, 22, 239, 50, 13, 60, 21, 251, 28, 190, 241, 176, 174, 154, 85, 18, 134, 132, 170, 187, 72, 98, 195, 124, 138, 243, 169, 50, 255, 16, 125, 74, 74, 213, 40, 61, 63, 240, 86, 49, 185, 11, 121, 60, 5, 111, 151, 206, 90, 84, 122, 33, 125, 93, 78, 29, 110, 57, 72, 247, 174, 5, 173, 141, 4, 207, 212, 108, 9, 42, 53, 237, 10, 199, 150, 175, 58, 28, 15, 50, 36, 2, 22, 222, 128, 88, 204, 221, 103, 72, 34, 66, 148, 202, 129, 70, 252, 121, 85, 17, 81, 10, 81, 196, 248, 100, 12, 194, 37, 94, 108, 146, 196, 161, 99, 168, 231, 68, 84, 171, 243, 113, 15, 69, 45, 132, 201, 12, 24, 185, 171, 247, 93, 189, 167, 21, 243, 62, 199, 174, 190, 249, 160, 86, 100, 162, 217, 152, 4, 109, 178, 43, 118, 146, 32, 112, 190, 229, 180, 215, 6, 100, 189, 235, 23, 151, 47, 137, 101, 159, 150, 126, 248, 106, 41, 244, 165, 202, 97, 208, 203, 244, 1, 74, 122, 220, 146, 152, 159, 4, 130, 134, 142, 233, 206, 169, 149, 98, 68, 167, 21, 62, 172, 163, 96, 198, 205, 226, 101, 57, 169, 203, 243, 164, 236, 194, 209, 44, 70, 8, 103, 113, 145, 155, 215, 235, 9, 192, 190, 207, 51, 87, 28, 187, 69, 117, 82, 82, 112, 243, 34, 254, 160, 186, 30, 215, 113, 180, 185, 233, 52, 179, 54, 17, 67, 150, 141, 37, 236, 188, 252, 57, 3, 205, 59, 17, 141, 171, 93, 68, 162, 19, 53, 28, 45, 123, 140, 202, 98, 50, 25, 122, 112, 167, 35, 72, 171, 52, 18, 92, 43, 248, 49, 236, 216, 159, 200, 197, 243, 180, 226, 64, 185, 106, 177, 193, 182, 115, 12, 168, 82, 54, 65, 143, 195, 199, 205, 53, 48, 174, 46, 5, 227, 10, 36, 114, 9, 105, 111, 221, 238, 112, 49, 124, 53, 112, 144, 2, 17, 14, 79, 171, 214, 129, 50, 238, 221, 194, 142, 152, 103, 50, 195, 197, 173, 172, 165, 205, 153, 67, 83, 105, 108, 176, 69, 242, 186, 114, 72, 72, 74, 88, 180, 143, 179, 107, 49, 152, 215, 46, 116, 46, 155, 124, 32, 117, 152, 216, 113, 165, 175, 189, 214, 21, 91, 223, 236, 35, 166, 140, 13, 31, 182, 23, 77, 249, 1, 222, 125, 10, 227, 247, 219, 31, 222, 127, 177, 224, 67, 168, 175, 147, 144, 173, 160, 65, 33, 253, 2, 220, 109, 179, 106, 223, 69, 73, 70, 63, 26, 109, 196, 208, 249, 54, 68, 10, 37, 157, 217, 41, 254, 237, 65, 227, 121, 99, 183, 61, 211, 169, 246, 28, 211, 64, 214, 223, 246, 69, 188, 50, 173, 146, 185, 203, 13, 236, 119, 14, 184, 80, 110, 40, 56, 100, 206, 131, 248, 206, 176, 164, 190, 239, 137, 156, 11, 191, 210, 39, 13, 166, 217, 50, 106, 79, 173, 4, 56, 93, 26, 30, 140, 113, 67, 141, 161, 246, 142, 170, 111, 105, 5, 235, 60, 177, 77, 73, 116, 103, 47, 45, 118, 238, 198, 146, 69, 99, 11, 92, 119, 90, 176, 228, 230, 120, 70, 84, 236, 32, 229, 12, 12, 101, 38, 95, 79, 215, 116, 187, 65, 126, 136, 198, 50, 47, 184, 60, 63, 136, 26, 146, 211, 93, 217, 63, 164, 108, 32, 80, 205, 152, 123, 128, 33, 112, 0, 1, 24, 217, 29, 15, 69, 227, 218, 45, 229, 190, 34, 119, 90, 195, 60, 10, 32, 164, 167, 50, 29, 247, 162, 39, 244, 121, 7, 101, 147, 90, 46, 249, 28, 36, 194, 29, 58, 241, 219, 172, 37, 121, 100, 30, 214, 125, 182, 34, 60, 250, 43, 83, 31, 32, 72, 102, 70, 98, 96, 92, 10, 241, 145, 10, 49, 68, 182, 34, 33, 18, 197, 153, 22, 45, 175, 22, 148, 12, 83, 255, 233, 99, 78, 30, 240, 106, 130, 147, 170, 122, 36, 102, 233, 239, 231, 31, 228, 218, 195, 102, 99, 251, 65, 157, 93, 61, 30, 91, 138, 207, 130, 21, 205, 110, 41, 68, 10, 5, 217, 152, 68, 39, 204, 132, 213, 230, 183, 79, 38, 156, 3, 23, 86, 195, 177, 90, 93, 26, 24, 111, 163, 17, 191, 69, 27, 57, 28, 2, 6, 164, 143, 254, 194, 181, 185, 118, 3, 184, 187, 195, 5, 164, 104, 157, 147, 89, 177, 37, 224, 246, 112, 157, 0, 51, 40, 126, 8, 60, 215, 247, 20, 127, 43, 157, 192, 155, 224, 225, 32, 92, 102, 62, 85, 6, 233, 252, 212, 151, 61, 170, 222, 14, 52, 207, 218, 182, 224, 217, 2, 7, 24, 91, 145, 120, 163, 109, 84, 215, 120, 240, 183, 72, 186, 44, 217, 58, 184, 159, 191, 82, 31, 21, 215, 135, 87, 174, 162, 252, 86, 73, 249, 49, 238, 142, 26, 33, 80, 223, 118, 34, 196, 42, 9, 244, 229, 156, 58, 253, 193, 109, 43, 207, 162, 236, 154, 217, 153, 213, 40, 60, 137, 91, 36, 82, 108, 159, 28, 99, 164, 191, 98, 45, 17, 54, 246, 215, 243, 176, 198, 82, 102, 83, 197];



#print(M1)
#print(M2)
#_M = o.operation.reconstructPartition(M1,M2,P)
#int_M = o.operation.binaryTonum(_M)
#int_numpy_M = numpy.array(_M,dtype=int)

#if(int_numpy_M.all() == wave.samples.all()):
#    print("sama")

#(M3,M4,P2) = o.operation.intel_partition(_M,2,P)
#intM3 = o.operation.binaryTonum(M3)
#intM4 = o.operation.binaryTonum(M4)

#if(intM3 == intM1):
#    print("seg1 aman")
#if(intM4 == intM2):
#    print("Seg2 aman")

#_M2 = o.operation.reconstructPartition(M3,M4,P2)
#int_M2 = o.operation.binaryTonum(_M2)
#int_numpy_M2 = numpy.array(_M2,dtype=int)

#if(int_numpy_M.all() == int_numpy_M2.all() == wave.samples.all()):
#    print("SEMUA AMAN PAK")


#f = open("GDE_seg.txt",mode="w")

#segment = 10
#thres = 120
#wave = Helper.WavIO.open("D:\coba.wav")
#samples = operation.operation.numToBinary(wave.samples)
#(M1,M2,P) = operation.operation.intel_partition(samples,2)
#intM1 = operation.operation.binaryTonum(M1)
#intM2 = operation.operation.binaryTonum(M2)
#print(len(intM1))
#print(len(intM2))

#while segment<3000 :
#    segment*=2
#    check1=GDE.checkCapacity(intM1,segment,thres)
#    check2=GDE.checkCapacity(intM2,segment,thres)
#    print(check1)
#    print(check2)
#    f.writelines("segment : " + str(segment) + "\n")
#    f.writelines(str(check1+check2)+ "\n")
#    f.writelines("---------------\n")

#f.close()



##tes hex ascii encoding##

#mess = [1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1]
#string_mes= o.operation.binaryArraytoString(mess)
#print(string_mes)
#_hex = hex(int(string_mes,2))[2:-1]
#print(_hex)
#message = binascii.unhexlify(_hex)
#print(message)


## tes improved RDE##

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

#angka1 = 100
#angka2 = 101
#file = open("hasil_RDE.txt",mode = 'w')

#for i in range(150):
#    (hasil1,hasil2,flag) = RDE.RDE(angka1,angka2,1)
#    angka2+=1
#    write_String = str(angka1)+","+str(angka2)+","+str(hasil1)+","+str(hasil2)+"\n"
#    file.write(write_String)
#file.close()


segment_size =2
threshold = 10

medium = Helper.WavIO.open("D:\\coba16.wav")

samples = op.operation.numToBinary(medium.samples)
(M1,M2,Partisi) = op.operation.intel_partition(samples,10)
intM1 = op.operation.binaryTonum(M1)
intM2 = op.operation.binaryTonum(M2)

for i in range(5):
    file = open("perbandingan_kapasitas_segmen_thres"+str(threshold)+".csv",mode='w')
    for i in range(20):
        kapasitas_M1 = GDE.checkCapacity(intM1,segment_size,threshold)
        kapasitas_M2 = GDE.checkCapacity(intM2,segment_size,threshold)
        capacity = kapasitas_M1+kapasitas_M2
        string_write = str(segment_size)+","+str(threshold) +","+str(capacity)+"\n"
        file.write(string_write)
        segment_size+=2
    file.close()
    segment_size=2
    threshold+=10