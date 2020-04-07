from Expression import Expression

class Rule:

    def __init__ (self, expressions, evaluated = []):
        self.expressions = expressions
        self.evaluated = []
    
    def evaluate(self, expressions = []):
        evaluated = []

        print("Expressions: {0}" .format(expressions))
        print("Expressions len: {0}" .format(len(expressions)))
        print()
        for i in range(len(expressions)):
            if len(expressions) == 3:
                #print("Less than 3")
                if isinstance(expressions[i], str):
                    if expressions[i] == "AND":
                        print("Return {0}" .format(self.evaluateAnd(expressions[i - 1], expressions[i - 2])))
                        return self.evaluateAnd(expressions[i - 1], expressions[i - 2])
                    elif expressions[i] == "OR":
                        print("Return {0}" .format(self.evaluateOr(expressions[i - 1], expressions[i - 2])))
                        return self.evaluateOr(expressions[i - 1], expressions[i - 2])
            elif isinstance(expressions[i], str):
                if i == len(expressions) - 1 :
                    evaluated.append(expressions[-1])
                elif expressions[i] == "AND":
                    newExpression = self.evaluateAnd(expressions[i - 1], expressions[i - 2])
                    print("Evaluating: {0}, {1} AND" .format(expressions[i - 1], expressions[i - 2]))
                    print("Inserting: {0}"  .format(newExpression))
                    evaluated.append(newExpression)
                elif expressions[i] == "OR":
                    newExpression = self.evaluateOr(expressions[i - 1], expressions[i - 2])
                    print("Evaluating: {0}, {1} OR" .format(expressions[i - 1], expressions[i - 2]))
                    print("Inserting: {0}"  .format(newExpression))
                    evaluated.append(newExpression)

        print("Evaluated: {0}" .format(evaluated))
        print("Evaluated len: {0}" .format(len(evaluated)))
        print()
        return self.evaluate(evaluated)
            
    def evaluateAnd(self, expressionOne, expressionTwo):
        if expressionOne and expressionTwo:
            return True
        return False
    
    def evaluateOr(self, expressionOne, expressionTwo):
        if expressionOne or expressionTwo:
            return True
        return False