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
                'C': lambda rule : print("Create rule " + rule[-1]),
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


## Update protocol to allow rules to be entered
## Stop naively getting the last digit when setting state