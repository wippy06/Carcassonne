import numpy as np

class tileStack:
    def __init__(self, x):
        self.__stack = np.empty(shape=(x), dtype=object)
        self.__top_pointer = 0
        self.__space = x
    
    def stack_append(self, item):
        if self.__top_pointer != self.__space:
            self.__stack[self.__top_pointer] = item
            self.__top_pointer += 1

    def stack_pop(self):
        if self.__top_pointer != 0:
            self.__stack[self.__top_pointer-1] = None
            self.__top_pointer -= 1

    def get_item(self):
        return self.__stack[self.__top_pointer-1]
    
    def full_check(self):
        if self.__top_pointer == self.__space:
            return True
        return False
    
    def empty_check(self):
        if self.__top_pointer == 0:
            return True
        return False