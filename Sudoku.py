
import re
from cell import *

class Sudoku:
    def __init__(self, content):
        r : int = 0
        c : int = 0
        self.cells = {}
        content = re.sub(r"[\n\t\s]*", "", content)
        for i in content:
            flag = False
            if i != '.':
                flag = True 
            self.cells[(r, c)] = Cell(r, c, i, flag) 
            c = c + 1
            if c > 8:
                c = 0
                r = r + 1

    #Check if two cells are in the same column
    def isSameColumn(self,cell1 : Cell, cell2 : Cell) -> bool :
        return (cell1.index_c == cell2.index_c)

    #Check if two cells are in the same row
    def isSameRow(self,cell1 : Cell, cell2 : Cell) -> bool :
        return (cell1.index_r == cell2.index_r)

    #Check if two cells are in the same box
    def isSameBox(self,cell1 : Cell, cell2 : Cell) -> bool:
        return ((cell1.index_r // 3) == (cell2.index_r // 3)) and ((cell1.index_c // 3) == (cell2.index_c // 3))

    #check if two cells are equal
    def isEqual(self, cell1 : Cell, cell2 : Cell):
        return (cell1.index_r == cell2.index_r) and (cell1.index_c == cell2.index_c)

    #It returns a list containing all the cells inside a given row
    def getRowCells(self,row : int) -> list:
        cells = []
        for i in range(9):
            cell : Cell = self.getCell(row, i)
            cells.append(cell)
        return cells
    
    #It returns a list containing all the cells inside a given column
    def getColumnCells(self,column : int) -> list:
        cells = []
        for i in range(9):
            cell : Cell = self.getCell(i, column)
            cells.append(cell)
        return cells

    #It returns a list containing all the cells inside a given box
    def getBoxCells(self,cell : Cell) -> list: 
        cells = []
        cellss = self.getCells()
        for el in cellss:
            if self.isSameBox(el,cell):
                cells.append(el)
        return cells

    #It returns the index of a cell 
    def getCellIndex(self,row : int ,column : int) -> int:
        return row * 9 + column

    #It returns all cells
    def getCells(self) -> list:
        return list(self.cells.values())

    #It returns a specific cell at given coordinates
    def getCell(self,index_r : int , index_c : int) -> Cell:
        return self.cells[(index_r,index_c)]

    #It returns all  fixed cells
    def getFixedCells(self) -> list:
        list = []
        for i in self.getCells():
            if i.found == True:
                list.append(i)
        return list

    #It returns all  non-choiced cells
    def getNonFixedCells(self) -> list:
        list = []
        for i in self.getCells():
            if i.found == False:
                list.append(i)
        return list  

    #It sets a value to a given cell
    def setFixedCell(self, indexR, indexC,value): 
        self.cells[(indexR,indexC)].setValue(value)
    
    #It removes a specific numbers from the list of possible numbers of a given cell
    def removeNumberOfCell(self,indexR,indexC,value):
        self.cells[(indexR,indexC)].removeNumber(value)
    
    #It sets the possible numbers of a cell equal to a given list
    def setNumberOfCell(self,indexR,indexC,lista : list ):
        self.cells[(indexR,indexC)].numbers = lista.copy()

    #It removes list cleaner from the possible numbers of a given cell
    def refreshNumberOfCell(self,indexR,indexC,cleaner : list) -> bool:
        flag = self.cells[(indexR,indexC)].refreshNumber(cleaner) #It returns false if no elements are deleted
        return flag 

    #It checks if two cells have same possible numbers
    def hasSameNumbers(self,cell1,cell2) -> bool:
        return (cell1.numbers == cell2.numbers)

    #Check if a cell has a value as a possible value
    def hasNumber(self,index_r,index_c, value) -> bool:
        return self.cells[(index_r,index_c)].hasNumber(value)

    #It checks if the given sudoku matrix is completed by only numbers and it checks if they are properly set
    def isComplete(self) -> bool: 
        fixed = self.getFixedCells()
        if len(fixed) != 81: #If exists at least one cell that isn't fixed than sudoku is surely not valid 
            return False
        else:
            for el in fixed:
                cellsRow = self.getRowCells(el.index_r)
                cellsColumn = self.getColumnCells(el.index_c)
                cellsbox = self.getBoxCells(el)
                array = [0,0,0,0,0,0,0,0,0]
                for el2 in cellsRow:
                    if not self.isEqual(el,el2) and el.value == el2.value:
                        return False
                    else: 
                        array[el2.value-1] = 1
                if 0 in array:
                    return False
                array = [0,0,0,0,0,0,0,0,0]
                for el2 in cellsColumn:
                    if not self.isEqual(el,el2) and el.value == el2.value:
                        return False
                    else: 
                        array[el2.value-1] = 1
                if 0 in array:
                    return False
                array = [0,0,0,0,0,0,0,0,0]
                for el2 in cellsbox:
                    if not self.isEqual(el,el2) and el.value == el2.value:
                        return False
                    else: 
                        array[el2.value-1] = 1
                if 0 in array:
                    return False
        return True 
                    
    #It prints the sudoku matrix
    def print(self):
        for i in range(9):
            result = ""
            for j in range(9):
                if j % 3 == 0: 
                    result = result + " "
                result = result + " " +str(self.cells[(i,j)].value)
            print(result+"\n")

    #it prints the available numbers for each cell
    def printNumbers(self):
        for i in range(9):
            for j in range(9):
                #print("With value: ")
                #print(self.cells[(i,j)].value)
                print(self.cells[(i,j)].numbers)


    
        
         