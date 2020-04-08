class Expression:

    def equalsTo(self, expressionOne, comparison):
        if expressionOne.reading == comparison:
            return True
        return False
    
    def greaterThan(self, expressionOne, comparison):
        if expressionOne.reading > comparison:
            return True
        return False
    
    def lessThan(self, expressionOne, comparison):
        if expressionOne.reading < comparison:
            return True
        return False

    def equalsToExpr(self, expressionOne, expressionTwo):
        if expressionOne.reading == expressionTwo.reading:
            return True
        return False
    
    def greaterThanExpr(self, expressionOne, expressionTwo):
        if expressionOne.reading > expressionTwo.reading:
            return True
        return False

    def lessThanExpr(self, expressionOne, expressionTwo):
        if expressionOne.reading < expressionTwo.reading:
            return True
        return False
    
    