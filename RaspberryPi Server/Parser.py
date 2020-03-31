class Parser:

    def parseInput(self, input):
        try:
            switch = {
                'C': lambda input : self.handleCommand(input[1:]),
                'R': lambda input : self.handleRequest(input[1:])
            }[input[0]](input)
        except (KeyError) as e:
            print("Invalid input")

    def handleCommand(self, command):
        try:
            switch = {
                'D': lambda command : print("Set Device " + command[1:2] + " to state " + command[-1]),
                'G': lambda command : print("Set Group " + command[1:2] + " to state " + command[-1]),
                'R': lambda command : self.handleRule(command[1:])
            }[command[0]](command)
        except (KeyError) as e:
            print("Invalid command")
    
    def handleRule(self, rule):
        try:
            switch = {
                'C': lambda rule : print("Create rule " + rule[-1]),
                'E': lambda rule : print("Replace rule with ID " + rule[1:2] + " with new rule " + rule[-1]),
                'D': lambda rule : print("Delete rule with ID " + rule[-1])
            }[rule[0]](rule)
        except (KeyError) as e:
            print("Invalid rule")

    def handleRequest(self, request):
        try:
            switch = {
                'S': lambda request : print("Sensor ID " + request[1:2] + " with state " + request[-1]),
                'A': lambda request : print("Return all sensor data")
            }[request[0]](request)
        except (KeyError) as e:
            print("Invalid request")


## Update protocol to colon separate to allow for ID's with more than one digit
## Stop naively getting the last digit when setting state