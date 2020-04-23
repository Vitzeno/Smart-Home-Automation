
class Rule(object):

    def __init__(self, id, name, rule, mobileFormattedRule = []):
        self.id = id
        self.name = name
        self.rule = rule
        self.mobileFormattedRule = mobileFormattedRule
    
    def toStringFormat(self):
        return "Name: " + str(self.name) + " ID: " + str(self.id) + " Rule: " + str(self.rule)
        #return "Name: " + str(self.name) + " ID: " + str(self.id)