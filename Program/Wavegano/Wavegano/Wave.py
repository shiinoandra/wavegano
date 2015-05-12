import numpy

class Wave:

    def __init__(self,name):
        self.name = name
        self.bitrate = 0
        self.samples=[]
        self.shape = ""
        self.type = ""
        self.min = 0
        self.max =0


    def print_info(self):
        print("Name : " + self.name + "\n" + 
               "Bitrate :"  + str(self.bitrate) + "\n" +
               "Shape : " + str(self.shape) + "\n" +
               "Type:" + str(self.type) + "\n" +
               "MIN : " + str(self.samples.min()) + "\n" +
               "MAX : " + str(self.samples.max()) + "\n")
    


