class Expression:

    '''
    Compares a sensor and a numeric value, tests for equality

    expressionOne: sensor
    comparison: numneric value
    '''
    def equalsTo(self, expressionOne, comparison):
        if expressionOne.temperature == comparison:
            return True
        return False
    
    '''
    Compares a sensor and a numeric value, tests for greater than

    expressionOne: sensor
    comparison: numneric value
    '''
    def greaterThan(self, expressionOne, comparison):
        if expressionOne.temperature > comparison:
            return True
        return False
    
    '''
    Compares a sensor and a numeric value, tests for less than

    expressionOne: sensor
    comparison: numneric value
    '''
    def lessThan(self, expressionOne, comparison):
        if expressionOne.temperature < comparison:
            return True
        return False

    '''
    Compares a sensor and a sensor, tests for equlity

    expressionOne: sensor
    expressionTwo: sensor
    '''
    def equalsToExpr(self, expressionOne, expressionTwo):
        if expressionOne.temperature == expressionTwo.temperature:
            return True
        return False
    
    '''
    Compares a sensor and a sensor, tests for greater than

    expressionOne: sensor
    expressionTwo: sensor
    '''
    def greaterThanExpr(self, expressionOne, expressionTwo):
        if expressionOne.temperature > expressionTwo.temperature:
            return True
        return False

    '''
    Compares a sensor and a sensor, tests for less than

    expressionOne: sensor
    expressionTwo: sensor
    '''
    def lessThanExpr(self, expressionOne, expressionTwo):
        if expressionOne.temperature < expressionTwo.temperature:
            return True
        return False
    
    