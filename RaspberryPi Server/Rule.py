
class Rule(object):

    def __init__(self, id, name, rule):
        self.id = id
        self.name = name
        self.rule = rule
    
    '''
    Converts object to string

    return: string representation of object
    '''
    def toStringFormat(self):
        return "Name: " + str(self.name) + " ID: " + str(self.id) + " Rule: [" + ':'.join(self.rule) + "] "
        #return "Name: " + str(self.name) + " ID: " + str(self.id)