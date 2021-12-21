#
#  main.py
#  Duomino
#
#  Created by Ali Emre Şenel on 09.11.2021.
#  Copyright (c) 2021 Ali Emre Şenel. All rights reserved.
#

import numpy as np
from itertools import repeat
from scipy import ndimage
import os

totalTestedShapes = 0
doPrint = False
allShapes = []

np.set_printoptions(threshold=np.inf, linewidth=os.get_terminal_size().columns)

def createShape(size):
    arr = np.zeros((size, size * 2), dtype=int)
    arr[0,size] = 1
    return arr

def isDuplicate(shapes, shapeArr):
    for a in range(4):
        shapeArr = np.rot90(shapeArr)
        for shape in shapes:
            if np.array_equal(shape, shapeArr):
                return True
    return False

def isPosFilled(shape, size, x, y):
    if x < 0:
        return True
    if y < 0:
        return True
    if x > size:
        return True
    if y > size * 2:
        return True
    return shape[x, y] != 0

def isSurrounded(shape, size, pos):
    return isPosFilled(shape, size, pos[0] + 1, pos[1]) and isPosFilled(shape, size, pos[0] - 1, pos[1]) and isPosFilled(shape, size, pos[0], pos[1] + 1) and isPosFilled(shape, size, pos[0], pos[1] - 1)


def buildShape(shapeArr: np.ndarray, shapeSize, size):
    global totalTestedShapes, doPrint, allShapes
    ret = 0
    if size == 0:
        strippedArr = shapeArr[~np.all(shapeArr == 0, axis = 1)]
        strippedArr = np.delete(strippedArr, np.where(~strippedArr.any(axis = 0))[0], axis = 1) 
        totalTestedShapes += 1
        if isDuplicate(allShapes, strippedArr):
            return 0
        else:
            if doPrint:
                print(strippedArr)
            allShapes.append(strippedArr)
            return 1
    else:
        for pos in np.argwhere(shapeArr):
            if not isSurrounded(shapeArr, shapeSize, pos):
                for i in range(4):
                    xOffset = 0
                    yOffset = 0
                    if i == 0:
                        xOffset = 1
                    elif i == 1:
                        yOffset = -1
                    elif i == 2:
                        xOffset = -1
                    elif i == 3:
                        yOffset = 1
                    if not isPosFilled(shapeArr, shapeSize, pos[0] + xOffset, pos[1] + yOffset):
                        shape = np.copy(shapeArr)
                        shape[pos[0] + xOffset, pos[1] + yOffset] = 1
                        ret += buildShape(shape, shapeSize, size - 1)
        return ret
                    

arraySize = 5
shapeSize = 5
print(buildShape(createShape(arraySize + 1), arraySize, shapeSize))
for shape in allShapes:
    print(shape)
print(len(allShapes))
print(totalTestedShapes)