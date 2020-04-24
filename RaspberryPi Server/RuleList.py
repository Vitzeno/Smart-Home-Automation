from RuleEvaluator import RuleEvaluator
from Rule import Rule
from Expression import Expression
import Serialise as Serialise

def Singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

@Singleton
class RuleList(object):

    ruleList = []
    FILE_DIR = "config/"
    FILE_TYPE = ".txt"
    FILE_NAME = "RuleList"

    def __init__(self, rules = []):
        print("Init Singleton Rule List Object")
        self.ruleList = rules
        self.counter = 0
    
    def createRule(self, name, rule):
        self.counter += 1
        rule = Rule(self.counter, name, rule)
        self.ruleList.append(rule)
    
    '''
    Since the constructor cannot be called agiain in a singleton, this method sets up the default
    '''
    def setUpDefaultData(self):
        print("Add default data to object")
        self.createRule("Rule One", ("C:R:C:1:0:EQ:1:12:LE:OR").split(":"))
        self.createRule("Rule Two", ("C:R:C:S1:21:LE").split(":"))
        self.counter = 2

    '''
    Init the rule list JSON file and write to disk, default parameters are used
    '''
    def initRuleList(self):
        print("Init rule list and write to file")
        try:
            self.setUpDefaultData()
            Serialise.serialiseObjectToFile(self, self.FILE_NAME, self.FILE_DIR)
        except (IOError, OSError, FileNotFoundError) as e:
            print("Failed to init {0}" .format(self.FILE_NAME))
    
    '''
    Read device list from disk, if it does not exist call init to create one with default parameters

    Use this method to access the devices list object
    '''
    def getRuleObject(self):
        try:
            rlObject = Serialise.deserialiseObjectFromFile(self.FILE_NAME, self.FILE_DIR)
        except (IOError, OSError, FileNotFoundError) as e:
            print("File {0} not found, init default data" .format(self.FILE_NAME))
            self.initRuleList()
        
        rlObject = Serialise.deserialiseObjectFromFile(self.FILE_NAME, self.FILE_DIR)
        return rlObject

    '''
    Write object to file
    '''
    def setRuleObject(self):
        try:
            Serialise.serialiseObjectToFile(self, self.FILE_NAME, self.FILE_DIR)
        except (IOError, OSError, FileNotFoundError) as e:
            print("Failed to write new object {0} to file" .format(self.FILE_NAME))
    
    '''
    Prints out rule data in string format
    '''
    def toStringFormat(self):
        allRules = ""
        for i in self.ruleList:
            allRules = allRules + i.toStringFormat()
        return allRules

    '''
    Search for a rule object by ID, possible that ID and list index are the same

    If it fails it will raise a ValueError exception
    '''
    def getRuleByID(self, id):
        if int(id) > int(self.counter):
            raise ValueError("ID not in range")
        for rule in self.ruleList:
            if int(rule.id) == int(id):
                return rule
        
        raise ValueError("ID not found in list")
