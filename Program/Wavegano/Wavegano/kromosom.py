import operation as op
import random
class kromosom:
  def __init__(self,data=""):
      self.data=""
      self.fitnessVal=0

  def mutate(self):
      i = random.randint(0,len(self.data))
      mutated = op.operation.binaryStringtoArray(self.data)
      if tobe_mutated[i] == 0:
          mutated[i] =1;
      else:
          mutated[i] = 0
      self.data  = op.operation.binaryArraytoString(tobe_mutated)
   
  def isEqual(self,_kromosom):
      if self.data == _kromosom.data:
          return true
      else:
          return false




