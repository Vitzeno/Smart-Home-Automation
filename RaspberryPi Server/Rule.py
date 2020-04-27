
class Rule(object):

    def __init__(self, id, name, rule, parsableRule, state = True):
        self.id = id
        self.name = name
        self.rule = rule
        self.parsableRule = parsableRule
        self.state = state

    def getTarget(self):
        return self.rule[3]
    
    def getState(self):
        self.state = bool(int(self.rule[4]))
        return self.state
    
    '''
    Converts object to string

    return: string representation of object
    '''
    def toStringFormat(self):
        return "Name: " + str(self.name) + " ID: " + str(self.id) + " Rule: [" + ':'.join(self.rule) + "] "
        #return "Name: " + str(self.name) + " ID: " + str(self.id)