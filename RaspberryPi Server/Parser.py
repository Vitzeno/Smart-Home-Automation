from Expression import Expression
from Rule import Rule
from Sensor import Sensor

class Parser:

    ruleList = []

    def parseInput(self, input):
        list = input.split(":")
        if(list[0] == "C"):
            self.handleCommand(list[1:])
        elif(list[0] == "R"):
            self.handleRequest(list[1:])
        else:
            print("Invalid input")

    def handleCommand(self, command):
        if(command[0] == "D"):
            print("Switch device {0}" .format(command[1:]))
        elif(command[0] == "G"):
            print("Switch group {0}" .format(command[1:]))
        elif(command[0] == "R"):
            self.handleRule(command[1:])
        else:
            print("Invalid command")

    def handleRule(self, rule):
        if(rule[0] == "C"):
            self.ruleList = []
            self.createRule(rule[1:])
        elif(rule[0] == "D"):
            print("Delete rule {0}" .format(rule[1:]))
        else:
            print("Invalid rule")

    def handleRequest(self, request):
        if(request[0] == "S"):
            print("Request sensor {0}" .format(request[1:]))
        elif(request[0] == "A"):
            print("Request all sensor data {0}" .format(request[1:]))
        else:
            print("Invalid request")

    '''
    Fix so that actual sensor objects are passed in instead of stand in

    Constructs with grammar defined below from the parsed string/list provided

        Rule    => Expr Expr BinOp | Expr
        Expr    => Expr | Expr UnPo | Expr Expr BinOp | Expr Digit BinOp
        Digit   => [0-9]+
        BinOp   => > | < | = | AND | OR
        UnOp    => NOT
    '''
    def createRule(self, rule):
        s1 = Sensor(0, "Temp")
        s2 = Sensor(1, "Humid")
        
        print("Passing in rule list {0}" .format(rule))
        index = self.getFirstBinOperator(rule)
        print("Operator {0} at index: {1}" .format(rule[index], index))

        # Handling base case of recursive function
        if len(rule) == 1:
            if (rule[index] == "AND"):
                self.ruleList.append("AND")
            elif (rule[index] == "OR"):
                self.ruleList.append("OR")
            else:
                print("Invalid binary operator")
        elif (rule[index] == "GE"):
            self.ruleList.append(Expression().greaterThan(s1, int(rule[index - 1])))
            print("{0} greater than {1}" .format(rule[index - 2], rule[index - 1]))
            if len(rule[index + 1:]) > 0:
                self.createRule(rule[index + 1:])
        elif (rule[index] == "LE"):
            self.ruleList.append(Expression().lessThan(s2, int(rule[index - 1])))
            print("{0} less than {1}" .format(rule[index - 2], rule[index - 1]))
            if len(rule[index + 1:]) > 0:
                self.createRule(rule[index + 1:])
        elif (rule[index] == "EQ"):
            self.ruleList.append(Expression().equalsTo(s1, int(rule[index - 1])))
            print("{0} equals to {1}" .format(rule[index - 2], rule[index - 1]))
            if len(rule[index + 1:]) > 0:
                self.createRule(rule[index + 1:])
        elif (rule[index] == "AND"):
            self.ruleList.append("AND")
            if len(rule[index + 1:]) > 0:
                self.createRule(rule[index + 1:])
        elif (rule[index] == "OR"):
            self.ruleList.append("OR")
            if len(rule[index + 1:]) > 0:
                self.createRule(rule[index + 1:])
        else:
            print("Invalid binary operator")
        
        print("Created rule {0}" .format(self.ruleList))
    
    
    '''
    Returns the first occurance of a binary operator in a give list or 0
    if no relavent operator is present
    '''
    def getFirstBinOperator(self, list):
        listLength = len(list)
        index = listLength
        for i in range(listLength):
            if list[i] == "GE":
                index = min(index, i)
            elif list[i] == "LE":
                index = min(index, i)
            elif list[i] == "EQ":
                index = min(index, i)
            elif list[i] == "AND":
                index = min(index, i)
            elif list[i] == "OR":
                index = min(index, i)
            elif i == listLength - 1:
                print("No valid operator found in current iteration")
                print("Make sure to use one of the following: GE, LE, EQ, AND, OR")
                return 0
        
        return index

## Update protocol to allow rules to be entered