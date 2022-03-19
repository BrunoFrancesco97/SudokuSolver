
from Sudoku import *
import copy
import random
from cell import *

class constraintPropagation:
    def __init__(self) -> None:
        self.backtracking = 0
        self.iterations = 0
    #It solves the sudoku by using constraint propagation and backtracking
    def solve(self, sudoku):
        if sudoku.isComplete():
            return sudoku
        else:
            self.__stableMatrix(sudoku)
            if sudoku.isComplete():
                return sudoku
            else:
                if self.__invalid(sudoku):
                    self.backtracking += 1
                    return None 
                goodCell = self.__getBestCell(sudoku)
                if goodCell is None:
                    self.backtracking += 1 
                    return None
                random.shuffle(goodCell.numbers)
                for n in goodCell.numbers:
                    self.iterations += 1
                    newSudoku = copy.deepcopy(sudoku)
                    newSudoku.setFixedCell(goodCell.index_r,goodCell.index_c,n)
                    newSudoku = self.solve(newSudoku)
                    if newSudoku is not None and newSudoku.isComplete():
                        return newSudoku
        return None 

    #Check if there are changes into my sudoky, meanwhile there are changes the algorithm updates the values in real time in order to simplify the sudoku
    def __stableMatrix(self, sudoku) -> None:
        stable = False
        while not stable:
            stable1 = self.__alreadyValued(sudoku)
            stable2 = self.__loneSingle(sudoku)
            stable3 = self.__hiddenSingle(sudoku)
            stable4 = self.__nakedPairs(sudoku)
            stable5 = self.__hiddenPairs(sudoku)
            stable = stable1 and stable2  and stable3 and stable4 and stable5 

    #Check if my sudoku is invalid 
    def __invalid(self, sudoku) -> bool:
        for el in sudoku.getNonFixedCells():
            if len(el.numbers) == 0:
                return True
        return False

    #It returns the best cell with no value assigned of the given sudoku, so it returns a cell with minimum number of values inside the list of numbers that cell can have 
    def __getBestCell(self, sudoku) -> Cell:
        element = None
        numbers = None
        for cell in sudoku.getNonFixedCells():
            if len(cell.numbers) > 0:
                if len(cell.numbers) == 2:
                    return cell
                if (element is None or len(cell.numbers) < numbers):
                    element = cell
                    numbers = len(cell.numbers)
        return element

    #It simplify the given sudoku by removing the non possible choices from the list of numbers of each cell, it returns False if at least one element is deleted, True otherwise
    def __alreadyValued(self, sudoku) -> bool:
        flag = True
        fixed = sudoku.getFixedCells()
        nonfixed = sudoku.getNonFixedCells()
        for i in fixed:
            for j in nonfixed:
                if i.value in j.numbers and (sudoku.isSameBox(i,j) or sudoku.isSameRow(i,j) or  sudoku.isSameColumn(i,j)):
                    sudoku.removeNumberOfCell(j.index_r,j.index_c, i.value)
                    flag = False
        return flag

    #It returns True iff there are no lone singles or if the algo has found an invalid cell, otherwise it returns False
    def __loneSingle(self, sudoku) -> bool:
        flag = True
        cells : list = sudoku.getNonFixedCells()
        for i in cells:
            if len(i.numbers) == 0:
                flag = True 
                break  
            if len(i.numbers) == 1:
                for j in cells: #Reduce choices of cells
                    if not sudoku.isEqual(i,j) and sudoku.isSameBox(i,j): #Removes from all cells inside my box the value I just have assigned to one cell
                        j.removeNumber(i.numbers[0])
                    if not sudoku.isEqual(i,j) and sudoku.isSameRow(i,j): #Removes from all cells inside my row the value I just have assigned to one cell
                        j.removeNumber(i.numbers[0])
                    if not sudoku.isEqual(i,j) and sudoku.isSameColumn(i,j): #Removes from all cells inside my row the value I just have assigned to one cell
                        j.removeNumber(i.numbers[0])
                flag = False #Sudoku wasn't stable, I've removed something
                sudoku.setFixedCell(i.index_r,i.index_c,i.numbers[0])
        return flag

    #It returns True iff there are no hidden singles or if the algo has found an invalid cell, otherwise it returns False
    def __hiddenSingle(self, sudoku) -> bool: 
        flag = True
        cells = sudoku.getNonFixedCells()
        #SAME BOX
        for i in cells:
            if len(i.numbers) == 0:
                flag = True 
                break  
            for j in i.numbers: 
                cont = 0  
                for z in cells:  
                    if sudoku.isSameBox(i,z) and z.containsNumber(j):
                        cont = cont + 1
                        xx = i.index_r
                        yy = i.index_c
                if cont == 1:
                    sudoku.setFixedCell(xx,yy,j)
                    flag = False
                    self.__alreadyValued(sudoku)
                    return flag 
        #SAME ROW
        for i in cells:
            if len(i.numbers) == 0:
                flag = True 
                break  
            for j in i.numbers:
                cont = 0
                for z in cells:
                    if sudoku.isSameRow(i,z) and z.containsNumber(j):
                        cont = cont + 1
                        xx = i.index_r
                        yy = i.index_c
                if cont == 1:
                    sudoku.setFixedCell(xx,yy,j)
                    flag = False
                    self.__alreadyValued(sudoku)
                    return flag 
        #SAME COLUMN
        for i in cells:
            if len(i.numbers) == 0:
                flag = True 
                break  
            for j in i.numbers:
                cont = 0
                for z in cells:
                    
                    if sudoku.isSameColumn(i,z) and z.containsNumber(j):
                        cont = cont + 1
                        xx = i.index_r
                        yy = i.index_c
                if cont == 1:
                    sudoku.setFixedCell(xx,yy,j)
                    flag = False
                    self.__alreadyValued(sudoku)
                    return flag 
        return flag

    #It returns True iff there are no naked pairs or if the algo has found an invalid cell, otherwise it returns False
    def __nakedPairs(self, sudoku) -> bool:
        cells = sudoku.getNonFixedCells()
        flag = True
        for i in cells:
            if len(i.numbers)==0: #Sudoku is invalid, I break the circle inside stableMatrix and  self.isValid inside solve function will figure out that the Sudoku isn't valid
                flag = True 
                break
            cellRow : list = sudoku.getRowCells(i.index_r)
            cellColumn : list = sudoku.getColumnCells(i.index_c)
            cellsBox : list = sudoku.getBoxCells(i)
            foundRow : bool = self.__nakedPairsSpec(cellRow,i, sudoku)
            foundColumn : bool = self.__nakedPairsSpec(cellColumn,i, sudoku)
            foundBox : bool = self.__nakedPairsSpec(cellsBox,i, sudoku)
            flag = foundRow and foundColumn and foundBox
        return flag

    #It returns True iff there are no hidden pairs, otherwise it returns False
    def __hiddenPairs(self, sudoku) -> bool:
        return self.__hiddenPairsBox(sudoku) and self.__hiddenPairsRow(sudoku) and self.__hiddenPairsColumn(sudoku)

    #Utility function used in order to find naked pairs inside the sudoku
    def __nakedPairsSpec(self,lista : list, cell, sudoku) -> bool:
        flag = True
        isPresent = False
        listAp = []
        for el in lista:
            if len(el.numbers) != 0 and len(cell.numbers) != 0 and sudoku.hasSameNumbers(cell,el) and len(cell.numbers) == 2 and not sudoku.isEqual(cell,el):
                isPresent = True
                listAp = cell.numbers.copy()
                break
        if isPresent == True:
            for element in lista:
                if len(element.numbers) != 0 and element.numbers != listAp:
                    flagg = sudoku.refreshNumberOfCell(element.index_r,element.index_c,listAp) #It returns false if no elements are deleted
                    if flagg == True: #If at least one element is deleted matrix isn't stable, it can happend naked pairs are found but other elements are already cleaned 
                        flag = False
        return flag

    #Utility function used in order to find hidden pairs inside the sudoku
    def __hiddenPairsBox(self, sudoku):
        flag = True
        cells = sudoku.getNonFixedCells()
        for i in cells:
            if len(i.numbers)==0:
                flag = True 
                break 
            cellsBox : list = sudoku.getBoxCells(i)
            contCells = 0
            indexX = -1
            indexY = -1
            for el in cellsBox:
                contN = 0
                for n in i.numbers:
                    if sudoku.hasNumber(el.index_r,el.index_c,n):
                        contN = contN + 1
                if contN > 2: #i has with el more than 2 numbers in common, it could be an hidden pair
                    contCells = contCells + 1 #I count that could be an hidden pair
                    if not sudoku.isEqual(i,el): #I save the coordinates of the other cell
                        indexX = el.index_r
                        indexY = el.index_c
            if contCells == 2: #If it's an hidden pair
                listResult : list = []
                if len(sudoku.cells[(indexX,indexY)].numbers) > len(i.numbers): #If that cell has more numbers than i
                    for num in sudoku.cells[(indexX,indexY)].numbers: #Iterate over those numbers
                        flagNum = False
                        for celll in cellsBox: #For each cell in the box that isn't equal to i or cell and that has num inside it
                            if not sudoku.isEqual(celll, sudoku.cells[(indexX,indexY)]) and not sudoku.isEqual(celll, i) and  num in celll.numbers:  #I have to remove that num from i and cell
                                flagNum = True
                        if flagNum == False:
                            listResult.append(num)
                else:
                    for num in i.numbers: #Iterate over those numbers
                        flagNum = False
                        for celll in cellsBox: #For each cell in the box that isn't equal to i or cell and that has num inside it
                            if not sudoku.isEqual(celll, sudoku.cells[(indexX,indexY)]) and not sudoku.isEqual(celll, i) and  num in celll.numbers:  #I have to remove that num from i and cell
                                flagNum = True
                        if flagNum == False:
                            listResult.append(num)
                if  len(listResult) == 2:
                    sudoku.setNumberOfCell(i.index_r,i.index_c,listResult)
                    sudoku.setNumberOfCell(sudoku.cells[(indexX,indexY)].index_r,sudoku.cells[(indexX,indexY)].index_c,listResult)
                    listResult = []
                    flag = False
        return flag
    
    #Utility function used in order to find hidden pairs inside the sudoku
    def __hiddenPairsRow(self, sudoku):
        flag = True
        cells = sudoku.getNonFixedCells()
        for i in cells:
            if len(i.numbers)==0:
                flag = True 
                break
            cellsRow : list = sudoku.getRowCells(i.index_r)
            contCells = 0
            indexX = -1
            indexY = -1
            for el in cellsRow:
                contN = 0
                for n in i.numbers:
                    if sudoku.hasNumber(el.index_r,el.index_c,n):
                        contN = contN + 1
                if contN > 2: #i has with el more than 2 numbers in common, it could be an hidden pair
                    contCells = contCells + 1 #I count that could be an hidden pair
                    if not sudoku.isEqual(i,el): #I save the coordinates of the other cell
                        indexX = el.index_r
                        indexY = el.index_c
            if contCells == 2: #If it's an hidden pair
                listResult : list = []
                if len(sudoku.cells[(indexX,indexY)].numbers) > len(i.numbers): #If that cell has more numbers than i
                    for num in sudoku.cells[(indexX,indexY)].numbers: #Iterate over those numbers
                        flagNum = False
                        for celll in cellsRow: #For each cell in the box that isn't equal to i or cell and that has num inside it
                            if not sudoku.isEqual(celll, sudoku.cells[(indexX,indexY)]) and not sudoku.isEqual(celll, i) and  num in celll.numbers:  #I have to remove that num from i and cell
                                flagNum = True
                        if flagNum == False:
                            listResult.append(num)
                else:
                    for num in i.numbers: #Iterate over those numbers
                        flagNum = False
                        for celll in cellsRow: #For each cell in the box that isn't equal to i or cell and that has num inside it
                            if not sudoku.isEqual(celll, sudoku.cells[(indexX,indexY)]) and not sudoku.isEqual(celll, i) and  num in celll.numbers:  #I have to remove that num from i and cell
                                flagNum = True
                        if flagNum == False:
                            listResult.append(num)
                if  len(listResult) == 2:
                    sudoku.setNumberOfCell(i.index_r,i.index_c,listResult)
                    sudoku.setNumberOfCell(sudoku.cells[(indexX,indexY)].index_r,sudoku.cells[(indexX,indexY)].index_c,listResult)
                    listResult = []
                    flag = False
        return flag

    #Utility function used in order to find hidden pairs inside the sudoku
    def __hiddenPairsColumn(self, sudoku):
        flag = True
        cells = sudoku.getNonFixedCells()
        for i in cells:
            if len(i.numbers)==0:
                flag = True 
                break
            cellsColumn : list = sudoku.getColumnCells(i.index_c)
            contCells = 0
            indexX = -1
            indexY = -1
            for el in cellsColumn:
                contN = 0
                for n in i.numbers:
                    if sudoku.hasNumber(el.index_r,el.index_c,n):
                        contN = contN + 1
                if contN > 2: #i has with el more than 2 numbers in common, it could be an hidden pair
                    contCells = contCells + 1 #I count that could be an hidden pair
                    if not sudoku.isEqual(i,el): #I save the coordinates of the other cell
                        indexX = el.index_r
                        indexY = el.index_c
            if contCells == 2: #If it's an hidden pair
                listResult : list = []
                if len(sudoku.cells[(indexX,indexY)].numbers) > len(i.numbers): #If that cell has more numbers than i
                    for num in sudoku.cells[(indexX,indexY)].numbers: #Iterate over those numbers
                        flagNum = False
                        for celll in cellsColumn: #For each cell in the box that isn't equal to i or cell and that has num inside it
                            if not sudoku.isEqual(celll, sudoku.cells[(indexX,indexY)]) and not sudoku.isEqual(celll, i) and  num in celll.numbers:  #I have to remove that num from i and cell
                                flagNum = True
                        if flagNum == False:
                            listResult.append(num)
                else:
                    for num in i.numbers: #Iterate over those numbers
                        flagNum = False
                        for celll in cellsColumn: #For each cell in the box that isn't equal to i or cell and that has num inside it
                            if not sudoku.isEqual(celll, sudoku.cells[(indexX,indexY)]) and not sudoku.isEqual(celll, i) and  num in celll.numbers:  #I have to remove that num from i and cell
                                flagNum = True
                        if flagNum == False:
                            listResult.append(num)
                if  len(listResult) == 2:
                    sudoku.setNumberOfCell(i.index_r,i.index_c,listResult)
                    sudoku.setNumberOfCell(sudoku.cells[(indexX,indexY)].index_r,sudoku.cells[(indexX,indexY)].index_c,listResult)
                    listResult = []
                    flag = False
        return flag

