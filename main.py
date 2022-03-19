from turtle import back
from Sudoku import Sudoku
from constraintPropagation import constraintPropagation
from relaxationLabelling import relaxationLabelling
import datetime
import copy 

#How many times the algorithm test the sudoku inside the file
N_TIMES_TESTING = 100

if __name__ == "__main__":
	filename = "sudoku/medium2.txt" #put here a file containing a sudoku
	stream = open(filename, mode='r')
	content = stream.read()
	stream.close()
	sudoku = Sudoku(content)
	i = 0
	totalTime = 0
	cont = 0
	print("INPUT MATRIX: ")
	sudoku.print()
	print("LET'S SOLVE IT "+str(N_TIMES_TESTING)+" TIMES WITH CONSTRAINT PROPAGATION AND BACKTRACKING!")
	iterations = 0
	backtracking = 0
	iterations2 = 0
	while i < N_TIMES_TESTING:
		constraintPropagationSolver : constraintPropagation = constraintPropagation()
		sudokuPass = copy.deepcopy(sudoku)
		timeStartConstraintPropagation : datetime = datetime.datetime.now()
		sudokuSolved = constraintPropagationSolver.solve(sudokuPass)
		timeEndConstraintPropagation : datetime = datetime.datetime.now()
		delta = (timeEndConstraintPropagation - timeStartConstraintPropagation)
		delta_ms = int(delta.total_seconds() * 1000)
		totalTime = totalTime + delta_ms
		i = i + 1 
		iterations = iterations + constraintPropagationSolver.iterations
		backtracking = backtracking + constraintPropagationSolver.backtracking
		if sudokuSolved is not None:
			cont = cont + 1 
	print("SUDOKU IS SOLVED WITH CONSTRAINT PROPAGATION AND BACKTRACKING "+str(cont)+"/"+str(N_TIMES_TESTING)+" times")
	if sudokuSolved is not None: 
		sudokuSolved.print()
	else:
		print("None")
	result = totalTime / N_TIMES_TESTING
	print("Solving time is about "+str(result)+"ms")
	print("Avg backtracking calls: "+str(backtracking/N_TIMES_TESTING))
	print("Avg iterations: "+str(iterations/N_TIMES_TESTING))
	print("***************")
	i = 0
	totalTime = 0
	cont = 0
	sudokuL = None
	print("LET'S SOLVE IT "+str(N_TIMES_TESTING)+" TIMES WITH RELAXATION LABELLING!")
	while i < N_TIMES_TESTING:
		sudokuPass2 = copy.deepcopy(sudoku)
		timeStartRelaxationLabelling : datetime = datetime.datetime.now()
		relaxationLabel : relaxationLabelling = relaxationLabelling()
		sudokuSolved2 = relaxationLabel.solve(sudokuPass2)
		timeEndRelaxationLabelling : datetime = datetime.datetime.now()
		i = i + 1
		delta = (timeEndRelaxationLabelling - timeStartRelaxationLabelling)
		delta_ms = int(delta.total_seconds() * 1000)
		totalTime = totalTime + delta_ms
		iterations2 = iterations2 + relaxationLabel.iterations
		if sudokuSolved2 is not None:
			sudokuL = sudokuSolved2
			cont = cont + 1
	print("SUDOKU IS SOLVED WITH RELAXATION LABELLING "+str(cont)+"/"+str(N_TIMES_TESTING)+" times")
	if sudokuL is not None:
		sudokuL.print()
	else:
		print("None")
	result = totalTime / N_TIMES_TESTING
	print("Solving time is about "+str(result)+"ms")
	print("Avg iterations: "+str(iterations2/N_TIMES_TESTING))
	print("***************")	
