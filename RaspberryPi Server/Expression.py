class Expression:

    def equalsTo(self, expressionOne, comparison):
        if expressionOne.temperature == comparison:
            return True
        return False
    
    def greaterThan(self, expressionOne, comparison):
        if expressionOne.temperature > comparison:
            return True
        return False
    
    def lessThan(self, expressionOne, comparison):
        if expressionOne.temperature < comparison:
            return True
        return False

    def equalsToExpr(self, expressionOne, expressionTwo):
        if expressionOne.temperature == expressionTwo.temperature:
            return True
        return False
    
    def greaterThanExpr(self, expressionOne, expressionTwo):
        if expressionOne.temperature > expressionTwo.temperature:
            return True
        return False

    def lessThanExpr(self, expressionOne, expressionTwo):
        if expressionOne.temperature < expressionTwo.temperature:
            return True
        return False
    
    