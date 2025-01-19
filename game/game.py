from constants import STARTING_TILE
import random
import json
from tile import tile
from tileStack import tileStack

class game:
    def __init__(self, gameFile):
        
        fileObj = open(gameFile, "r")
        self.__gameFile = json.loads(fileObj.read())
        fileObj.close()

        random.seed(self.__gameFile["Seed"])

        self.__tileList = []
        self.__tileDataDict = {}

        randomList = self.__generateList()
        self.__generateTiles(randomList)
        randomTileList = self.__mergeSort(self.__tileList)

        self.__tileStack = tileStack(len(randomTileList)+1)
        self.__generateTileStack(randomTileList)

    def __generateList(self):
        generatedList = []
        for i in range(83):
            generatedList.append(i)

        generatedList = self.__fisherYates(generatedList)

        return generatedList

    def __fisherYates(self, No_list):
        for i in range(len(No_list) - 1,0,-1):
            j = random.randint(0, i)
            No_list[i], No_list[j] = No_list[j], No_list[i]

        return No_list
    
    def __generateTiles(self, randomList):
        tileData = open("tiles/tileData.json", "r")
        self.__tileDataDict = json.loads(tileData.read())
        tileData.close()

        tileTypeCount = open("tiles/tileCount.json", "r")
        tileTypeCountDict = json.loads(tileTypeCount.read())
        tileTypeCount.close()

        tileKeys = tileTypeCountDict.keys()

        tileCount = 0
        for key in tileKeys:
            for i in range(tileTypeCountDict[key]):
                self.__tileList.append(tile(self.__tileDataDict[key], randomList[tileCount]+1))
                tileCount += 1

    def __mergeSort(self, arr):
        if len(arr) == 1:
            return arr
        
        mid = len(arr) // 2
        left_half = []
        right_half = []

        for i in range(mid):
            left_half.append(arr[i])
        print(left_half)

        for i in range(len(arr)-mid):
            right_half.append(arr[i + mid])
        print(right_half)

        left_half = self.__mergeSort(left_half)
        right_half = self.__mergeSort(right_half)
        
        sorted_list = []
        i = 0
        j=0
        
        while i < len(left_half) and j < len(right_half):
            if left_half[i].getOrder() <= right_half[j].getOrder():
                sorted_list.append(left_half[i])
                i += 1
            else:
                sorted_list.append(right_half[j])
                j += 1

        for index in range(len(left_half)-i):
            sorted_list.append(left_half[index + i])

        for index in range(len(right_half)-j):
            sorted_list.append(right_half[index + j])

        return sorted_list
    
    def __generateTileStack(self,tileList):
        for tileObj in tileList:
            self.__tileStack.stack_append(tileObj)

        self.__tileStack.stack_append(tile(self.__tileDataDict[STARTING_TILE],0))
    
game("gameSlots/Slot1.json")
