
from Sudoku import *
from cell import *
import numpy as numpy
import random

class relaxationLabelling:
    def __init__(self):
        self.iterations = 0

    def solve(self, sudoku):
        if sudoku.isComplete():
            return sudoku
        self.__alreadyValued(sudoku)
        compatibilities = self.__generateCompatibilityCoefficients(sudoku)
        probabilities = self.__generateProbabilities(sudoku)
        value = 0
        threshold = 1		
        while threshold > 0.001:
            self.iterations +=1
            (probabilities, q) = self.__updateProbabilities(probabilities, compatibilities)
            avg = numpy.sum(probabilities * q)
            threshold = avg - value
            value = avg			            
        probabilities = probabilities.reshape(81, 9) 
        for el in sudoku.getCells():
            if el.found == False:
                el.setValue(numpy.argmax(probabilities[el.index_r * 9 + el.index_c]) + 1)
        if sudoku.isComplete():
            return sudoku
        else:
            return None	

    #This function generates the probabilities for each object, so if an object has already a label then prob 1, else it assigns a random probability to it
    def __generateProbabilities(self, sudoku):
        prob = numpy.ones((81, 9))
        for el in sudoku.getCells():
            vect = numpy.zeros(9) #Set all 0s 
            if el.found == True: #Cell has already a value
                vect[el.value - 1] = 1
            else:
                for n in el.numbers:
                    vect[n - 1] = random.randint(1, 9)
            prob[sudoku.getCellIndex(el.index_r,el.index_c)] = vect / numpy.sum(vect)
        return prob.reshape(729, 1)

    #Generate strength of compatibility between each couple of cells
    def __generateCompatibilityCoefficients(self, sudoku):
        matrix = numpy.zeros((81 * 9, 81 * 9))
        for el1 in sudoku.getCells():
            for n in range(9):
                for el2 in sudoku.getCells():
                    for m in range(9):
                        matrix[(sudoku.getCellIndex(el1.index_r,el1.index_c) * 9) + n][(sudoku.getCellIndex(el2.index_r,el2.index_c) * 9) + m] = self.__updateCompatibilities(sudoku, el1, el2, n, m)
        return matrix
    
    
    #Utility function used to assign a compatibility coefficient
    def __updateCompatibilities(self, sudoku, cell1, cell2, val1, val2):
        if sudoku.isEqual(cell1, cell2):
            return 0
        if val1 != val2:
            return 1
        if sudoku.isSameRow(cell1, cell2) or sudoku.isSameColumn(cell1, cell2) or sudoku.isSameBox(cell1, cell2):
            return 0
        return 1
    
    #Update probabilities of choices
    def __updateProbabilities(self, probabilities, compatibility):
        q = numpy.dot(compatibility, probabilities)
        ProbQ = (probabilities * q).reshape(81, 9)
        # compute sum for every cell
        for n in range(81):
            sum = numpy.sum(ProbQ[n])
            for m in range(9):
                ProbQ[n][m] /= sum
        newP = ProbQ.reshape(729, 1)
        return (newP, q)
    
    #Delete all numbers that can't be chosen into a cell
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

    