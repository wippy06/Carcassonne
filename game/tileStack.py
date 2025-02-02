import numpy as np

class tileStack:
    def __init__(self, x):
        #stack as a numpy array
        self.__stack = np.empty(shape=(x), dtype=object)
        #top pointer is array index with [0] being bottom of stack
        self.__topPointer = 0
        self.__space = x

    #Stack methods    
    def stackAppend(self, item):
        if self.__topPointer != self.__space:
            self.__stack[self.__topPointer] = item
            self.__topPointer += 1

    def stackPop(self):
        if self.__topPointer != 0:
            self.__stack[self.__topPointer-1] = None
            self.__topPointer -= 1

    def getItem(self):
        return self.__stack[self.__topPointer-1]
    
    def fullCheck(self):
        if self.__topPointer == self.__space:
            return True
        return False
    
    def emptyCheck(self):
        if self.__topPointer == 0:
            return True
        return False
    
    def getSize(self):
        return self.__topPointer
    
    def getMaxSize(self):
        return self.__space