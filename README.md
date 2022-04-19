
Assignment solved in "**Artificial Intelligence: Knowledge Representation and planning**" course at Ca'Foscari University, see **REPORT.pdf** for a project explanation.

**Requirements**:

Write a solver for sudoku puzzles using a constraint satisfaction approach based on constraint propagation and backtracking, and one based on Relaxation Labeling. compare the approaches, their strengths and weaknesses.
A sudoku puzzle is composed of a square 9x9 board divided into 3 rows and 3 columns of smaller 3x3 boxes. The goal is to fill the board with digits from 1 to 9 such that
- each number appears only once for each row column and 3x3 box;
- each row, column, and 3x3 box should containg all 9 digits.
The solver should take as input a matrix withwhere empty squares are represented by a standars symbol (e.g., ".", "_", or "0"), while known square should be represented by the corresponding digit (1,...,9).
