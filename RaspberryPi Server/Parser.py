import Radio as Radio

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
        deviceList = DeviceList().getDevicesObject()

        if(device[0] == "C"):
            try:
                print("Create deivice named {0}" .format(device[1]))
                deviceList.addDevice(str(device[1]))
                deviceList.setDevicesObject()
            except (ValueError) as e:
                print(e)
        elif(device[0] == "S"):
            try:
                print("Switch deivice {0} to {1}" .format(device[1], device[2]))
                Radio.switchSocket(int(device[1]), bool(int(device[2])))
                toSwitch = deviceList.getDeviceByID(device[1])
                toSwitch.lastKnownState = bool(int(device[2]))
                deviceList.setDevicesObject()
            except (ValueError) as e:
                print(e)
        elif(device[0] == "D"):
            try:
                print("Delete Device with ID: {0}" .format(device[1]))
                toRemove = deviceList.getDeviceByID(device[1])
                deviceList.devicesList.remove(toRemove)
                deviceList.setDevicesObject()
            except (ValueError) as e:
                print(e)
        elif(device[0] == "E"):
            try:
                print("Rename devie with ID {0} to {1}" .format(device[1], device[2]))
                toEdit = deviceList.getDeviceByID(device[1])
                toEdit.name = str(device[2])
                deviceList.setDevicesObject()
            except (ValueError) as e:
                print(e)
        else:
            raise ParserException("Invalid device command")
    
    '''
    Handles group or raises a ParserException
    '''     
    def handleGroups(self, group):
        groupList = GroupList().getGroupObject()
        deviceList = DeviceList().getDevicesObject()

        if(group[0] == "C"):
            try:
                print("Create group named {0} with devices {1}" .format(group[1], group[2:]))
                toAdd = []
                for i in group[2:]:
                    toAdd.append(deviceList.getDeviceByID(i))
                groupList.createGroup(str(group[1]), toAdd)
                groupList.setGroupObject()
            except (ValueError) as e:
                print(e)
        elif(group[0] == "D"):
            try:
                print("Delete group with ID {0}" .format(group[1]))
                toRemove = groupList.getGroupByID(group[1])
                groupList.groupList.remove(toRemove)
                groupList.setGroupObject()
            except (ValueError) as e:
                print(e)
        elif(group[0] == "S"):
            try:
                print("Switch group {0} " .format(group[1]))
                toSwitch = groupList.getGroupByID(group[1])
                toSwitch.switchAll(bool(int(group[2])))
            except (ValueError) as e:
                print(e)
        elif(group[0] == "E"):
            try:
                print("Rename group with ID {0} to {1}" .format(group[1], group[2]))
                toEdit = groupList.getGroupByID(group[1])
                toEdit.name = str(group[2])
                groupList.setGroupObject()
            except (ValueError) as e:
                print(e)
        else:
            raise ParserException("Invalid group command")

    '''
    Handles rule or raises a ParserException
    '''
    def handleRule(self, rule):
        ruleList = RuleList().getRuleObject()

        if(rule[0] == "C"):
            self.ruleList = []
            self.isValidPostFixNotation(rule)
            self.createRule(rule[1:])
        elif(rule[0] == "D"):
            try:
                print("Delete rule ID {0}" .format(rule[1]))
                toRemove = ruleList.getRuleByID(rule[1])
                ruleList.ruleList.remove(toRemove)
                ruleList.setRuleObject()
            except (ValueError) as e:
                print(e)  
        elif(rule[0] == "E"):
            try:
                print("Rename rule with ID {0} to {1}" .format(rule[1], rule[2]))
                toEdit = ruleList.getRuleByID(rule[1])
                toEdit.name = str(rule[2])
                ruleList.setRuleObject()
            except (ValueError) as e:
                print(e) 
        else:
            raise ParserException("Invalid rule")
    
    '''
    Parses reques or raises a ParserException
    '''
    def handleRequest(self, request):
        ruleList = RuleList().getRuleObject()
        deviceList = DeviceList().getDevicesObject()
        sensorList = SensorList().getSensorObject()
        groupList = GroupList().getGroupObject()

        if(request[0] == "S"):
            try:
                return(sensorList.getSensorByID(request[-1]).toStringFormat())
            except (ValueError) as e:
                return("Cannot find sensor with id {0}" .format(request[-1]))
        elif(request[0] == "AS"):
            return(sensorList.toStringFormat())
        elif(request[0] == "D"):
            try:
                return(deviceList.getRuleByID(request[-1]).toStringFormat())
            except (ValueError) as e:
                return("Cannot find device with id {0}" .format(request[-1]))
        elif(request[0] == "AD"):
            return(deviceList.toStringFormat())
        elif(request[0] == "R"):
            try:
                return(ruleList.getRuleByID(request[-1]).toStringFormat())
            except (ValueError) as e:
                return("Cannot find rule with id {0}" .format(request[-1]))
        elif(request[0] == "AR"):
            return(ruleList.toStringFormat())
        elif(request[0] == "G"):
            try:
                return(groupList.getGroupByID(request[-1]).toStringFormat())
            except (ValueError) as e:
                return("Cannot find group with id {0}" .format(request[-1]))
        elif(request[0] == "AG"):
            return(groupList.toStringFormat())
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
        ruleList.createRule("", self.input.split(":"), self.input.split(":")[5:])
        ruleList.setRuleObject()

        print("Created rule {0}" .format(self.input.split(":")))
    