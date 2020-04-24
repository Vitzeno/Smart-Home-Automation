from Expression import Expression
from RuleEvaluator import RuleEvaluator
from RuleList import RuleList
from Sensor import Sensor
from SensorList import SensorList
from Group import Group
from GroupList import GroupList
from Devices import Devices
from DeviceList import DeviceList
import Serialise as Serialise
from ParserException import ParserException

class Parser:

    input = []


    '''
    First step in the parsing process, parses input or raises a ParserException
    '''
    def parseInput(self, input):
        self.input = input
        list = input.split(":")
        if(list[0] == "C"):
            self.handleCommand(list[1:])
        elif(list[0] == "R"):
            return self.handleRequest(list[1:])
        else:
            raise ParserException("Invalid input")
    
    '''
    Parses command or raises a ParserException
    '''
    def handleCommand(self, command):
        if(command[0] == "D"):
            self.handleDevices(command[1:])
        elif(command[0] == "G"):
            self.handleGroups(command[1:])
        elif(command[0] == "R"):
            self.handleRule(command[1:])
        else:
            raise ParserException("Invalid command")
    
    '''
    Handles devices or raises a ParserException
    '''
    def handleDevices(self, device):
        if(device[0] == "E"):
            print("Edit deivice {0}" .format(device[1:]))
        elif(device[0] == "S"):
            print("Switch deivice {0}" .format(device[1:]))
        else:
            raise ParserException("Invalid device command")
    
    '''
    Handles group or raises a ParserException
    '''     
    def handleGroups(self, group):
        if(group[0] == "C"):
            print("Create group {0} with devices {1}" .format(group[1], group[2:]))
        elif(group[0] == "D"):
            print("Delete group {0}" .format(group[1]))
        elif(group[0] == "S"):
            print("Switch group {0} " .format(group[1:]))
        else:
            raise ParserException("Invalid group command")

    '''
    Handles rule or raises a ParserException
    '''
    def handleRule(self, rule):
        if(rule[0] == "C"):
            self.ruleList = []
            self.isValidPostFixNotation(rule)
            self.createRule(rule[1:])
        elif(rule[0] == "D"):
            print("Delete rule {0}" .format(rule[1:]))
        else:
            raise ParserException("Invalid rule")
    
    '''
    Parses reques or raises a ParserException
    '''
    def handleRequest(self, request):
        ruleList = RuleList().getRuleObject()

        if(request[0] == "S"):
            return("Request sensor {0}" .format(request[-1]))
        elif(request[0] == "AS"):
            return("Request all sensor data {0}" .format(request[-1]))
        elif(request[0] == "D"):
            return("Request device {0}" .format(request[-1]))
        elif(request[0] == "AD"):
            return("Request all device data {0}" .format(request[-1]))
        elif(request[0] == "R"):
            try:
                return(ruleList.getRuleByID(request[-1]).toStringFormat())
            except (ValueError) as e:
                return("Cannot find rule with id {0}" .format(request[-1]))
        elif(request[0] == "AR"):
            return(ruleList.toStringFormat())
        elif(request[0] == "G"):
            return("Request group {0}" .format(request[1:]))
        elif(request[0] == "AG"):
            return("Request all group data {0}" .format(request[-1]))
        else:
            raise ParserException("Invalid request")

    def isValidPostFixNotation(self, rule):
        return("Validating notation")

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
        ruleList = RuleList().getRuleObject()
        ruleList.createRule("", self.input.split(":"))
        ruleList.setRuleObject()

        print("Created rule {0}" .format(self.input.split(":")))
    

## Update protocol to allow rules to be entered