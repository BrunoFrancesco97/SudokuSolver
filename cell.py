class Cell:
    def __init__(self, index_r : int,index_c : int,value : any, found : bool):
        self.index_r : int = index_r 
        self.index_c : int = index_c
        self.numbers = [] #All possible values the cell can have
        self.found : bool = found
        if found:
            self.value = int(value)
        else: self.value = '.'
        if not found:
            self.numbers = [1,2,3,4,5,6,7,8,9] #If there is no number, so I read a . then I generate all possible numbers for the cell
    
    #It sets the value of the cell
    def setValue(self,value):
        if(value > 0 and value < 10 ):
            self.value = value
        else: self.value = '.'
        self.found = True
        self.numbers = []

    #It checks if a given number is contained inside the cell numbers
    def hasNumber(self,value):
        flag = False 
        for i in self.numbers:
            if i == value:
                flag = True 
                break 
        return flag 

    #It removes a given number from the cell numbers
    def removeNumber(self,value):
        list = []
        for i in self.numbers:
            if i != value:
                list.append(i)
        self.numbers = list.copy() 

    #It removes a list of numbers from the cell numbers
    def refreshNumber(self, cleaner : list):
        flag = True
        copy : list = self.numbers 
        self.numbers = [el for el in self.numbers if el not in cleaner]
        self.numbers.sort()
        if copy == self.numbers:
            flag = False 
        return flag 

    #It checks if a given number is inside the cell numbers
    def containsNumber(self,value): 
        occurences = False 
        for i in self.numbers:
            if(value == i):
                occurences = True
        return occurences 
    
    #it prints the info of a cell
    def print(self):
        print("COORDINATES: "+str(self.index_r+1)+";"+str(self.index_c+1))
        print("VALUE: "+str(self.value))
        print("Numbers:")
        print(self.numbers)
