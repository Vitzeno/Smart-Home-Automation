from Expression import Expression
from Rule import Rule
from Sensor import Sensor

class Parser:

    def parseInput(self, input):
        try:
            index = input.index(":")
            switch = {
                'C': lambda input : self.handleCommand(input),
                'R': lambda input : self.handleRequest(input)
            }[input[:index]](input[index + 1:])
        except (KeyError, ValueError) as e:
            print("Invalid input")

    def handleCommand(self, command):
        try:
            index = command.index(":")            
            switch = {
                'D': lambda command : print("Set Device " + command[:command.index(":")] + " to state " + command[-1]),
                'G': lambda command : print("Set Group " + command[:command.index(":")] + " to state " + command[-1]),
                'R': lambda command : self.handleRule(command)
            }[command[:index]](command[index + 1:])
        except (KeyError, ValueError) as e:
            print("Invalid command")
    
    def handleRule(self, rule):
        try:
            index = rule.index(":")
            switch = {
                'C': lambda rule : self.createRule(rule),
                'E': lambda rule : print("Replace rule with ID " + rule[:rule.index(":")] + " with new rule " + rule[-1]),
                'D': lambda rule : print("Delete rule with ID " + rule[-1])
            }[rule[:index]](rule[index + 1:])
        except (KeyError, ValueError) as e:
            print("Invalid rule")

    ## Request ALL must end with a colon
    def handleRequest(self, request):
        try:
            index = request.index(":")
            switch = {
                'S': lambda request : print("Get data for sensor with ID " +  request[-1]),
                'A': lambda request : print("Return all sensor data")
            }[request[:index]](request[index + 1:])
        except (KeyError, ValueError) as e:
            print("Invalid request")

    '''
    Fix so that actual sensor objects are passed in instead of stand in
    '''
    def createRule(self, rule):
        ruleList = []
        s1 = Sensor(0, "Temp")
        s2 = Sensor(1, "Humid")

        list = rule.split(":")
        print("Passed in {0}" .format(list))
        index = self.getFirstBinOperator(list)
        print(index)

        if (list[index] == "GE"):
            ruleList.append(Expression().greaterThan(s1, int(list[index - 1])))
            print("{0} greater than {1}" .format(list[index - 2], list[index - 1]))
        elif (list[index] == "LE"):
            ruleList.append(Expression().lessThan(s2, int(list[index - 1])))
            print("{0} less than {1}" .format(list[index - 2], list[index - 1]))
        elif (list[index] == "EQ"):
            ruleList.append(Expression().equalsTo(s1, int(list[index - 1])))
            print("{0} equals to {1}" .format(list[index - 2], list[index - 1]))
        elif (list[index] == "AND"):
            ruleList.append("AND")
        elif (list[index] == "OR"):
            ruleList.append("OR")
        else:
            print("Invalid binary operator")
        
        print("Created rule {0}" .format(ruleList))
    
    def getFirstBinOperator(self, list):
        index = list.index("GE")
        index = list.index("LE") if list.index("LE") < index else index
        index = list.index("EQ") if list.index("LE") < index else index
        index = list.index("AND") if list.index("AND") < index else index
        index = list.index("OR") if list.index("OR") < index else index

        return index

## Update protocol to allow rules to be entered
## Stop naively getting the last digit when setting state