from Expression import Expression

class RuleEvaluator(object):
    '''
    Evaluate a given rule, grammar for rule defined below:

        Rule    => Expr Expr BinOp | Expr
        Expr    => Expr | Expr UnPo | Expr Expr BinOp | Expr Digit BinOp
        Digit   => [0-9]+
        BinOp   => > | < | = | AND | OR
        UnOp    => NOT
    '''
    def evaluate(self, expressions = []):
        evaluated = []
        #print()
        #print("Start: {0}" .format(expressions))
        i = self.getFirstOccurance(expressions)

        # Handle singular expressions
        if len(expressions) == 1:
            #print("RETURN: {0}" .format(expressions[0]))
            return expressions[0]

        # Base case of recursive function
        if len(expressions) <= 3:
            if expressions[i] == "AND":
                #print("RETURN: {0}" .format(self.evaluateAnd(expressions[i - 1], expressions[i - 2])))
                return self.evaluateAnd(expressions[i - 1], expressions[i - 2])
            elif expressions[i] == "OR":
                #print("RETURN: {0}" .format(self.evaluateOr(expressions[i - 1], expressions[i - 2])))
                return self.evaluateOr(expressions[i - 1], expressions[i - 2])
            elif expressions[i] == "NOT":
                #print("RETURN: {0}" .format(self.evaluateNot(expressions[i])))
                return self.evaluateNot(expressions[i])
            else:
                #print("Invalid operator")
                return None
        elif expressions[i] == "AND":
            newExpression = self.evaluateAnd(expressions[i - 1], expressions[i - 2])
            #print("Evaluating: {0}, {1} AND to {2}" .format(expressions[i - 1], expressions[i - 2], newExpression))
            del expressions[i - 2:i + 1]
            expressions.insert(i - 2, newExpression)
            #print("Passing: {0}" .format(expressions))
        elif expressions[i] == "OR":
            newExpression = self.evaluateOr(expressions[i - 1], expressions[i - 2])
            #print("Evaluating: {0}, {1} OR to {2}" .format(expressions[i - 1], expressions[i - 2], newExpression))
            del expressions[i - 2 :i + 1]
            expressions.insert(i - 2, newExpression)
            #print("Passing: {0}" .format(expressions))  
        else:
            #print("Invalid operator")
            return None

        return self.evaluate(expressions)
    
    '''
    Returns the index of the first occurance of a str
    '''
    def getFirstOccurance(self, expressions):
        for i in range(len(expressions)):
            if isinstance(expressions[i], str):
                return i
        return 0
       
    def evaluateAnd(self, expressionOne, expressionTwo):
        if expressionOne and expressionTwo:
            return True
        return False
    
    def evaluateOr(self, expressionOne, expressionTwo):
        if expressionOne or expressionTwo:
            return True
        return False

    '''
    Update this method to function with the new evaluation rules
    '''
    def evaluateNot(self, expressionOne):
        return not expressionOne
    

    # Update rule evaluation to handle singular expressions