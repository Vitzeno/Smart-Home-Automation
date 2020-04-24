from Expression import Expression
from ParserException import ParserException
from Sensor import Sensor
from SensorList import SensorList

class RuleEvaluator(object):

    ruleList = []

    '''
    Evaluate a given rule, grammar for rule defined below:

        Rule    => Expr Expr BinOp | Expr
        Expr    => Expr | Expr UnPo | Expr Expr BinOp | Expr Digit BinOp
        Digit   => [0-9]+
        BinOp   => > | < | = | AND | OR
        UnOp    => NOT
    
    Raises a ParserExpresion on fail
    
    expression: list of expressions and binary operators
    '''
    def evaluate(self, expressions = []):
        evaluated = []
        print()
        print("Start: {0}" .format(expressions))
        i = self.getFirstOccurance(expressions)

        # Handle singular expressions
        if len(expressions) == 1:
            print("RETURN: {0}" .format(expressions[0]))
            return expressions[0]

        # Base case of recursive function
        if len(expressions) <= 3:
            if expressions[i] == "AND":
                print("RETURN: {0}" .format(self.evaluateAnd(expressions[i - 1], expressions[i - 2])))
                return self.evaluateAnd(expressions[i - 1], expressions[i - 2])
            elif expressions[i] == "OR":
                print("RETURN: {0}" .format(self.evaluateOr(expressions[i - 1], expressions[i - 2])))
                return self.evaluateOr(expressions[i - 1], expressions[i - 2])
            elif expressions[i] == "NOT":
                print("RETURN: {0}" .format(self.evaluateNot(expressions[i])))
                return self.evaluateNot(expressions[i])
            else:
                print("Invalid operator")
                return None
        elif expressions[i] == "AND":
            newExpression = self.evaluateAnd(expressions[i - 1], expressions[i - 2])
            print("Evaluating: {0}, {1} AND to {2}" .format(expressions[i - 1], expressions[i - 2], newExpression))
            del expressions[i - 2:i + 1]
            expressions.insert(i - 2, newExpression)
            print("Passing: {0}" .format(expressions))
        elif expressions[i] == "OR":
            newExpression = self.evaluateOr(expressions[i - 1], expressions[i - 2])
            print("Evaluating: {0}, {1} OR to {2}" .format(expressions[i - 1], expressions[i - 2], newExpression))
            del expressions[i - 2 :i + 1]
            expressions.insert(i - 2, newExpression)
            print("Passing: {0}" .format(expressions))  
        else:
            print("Invalid operator")
            return None

        return self.evaluate(expressions)
    
    '''
    Parser a rule with grammar defined below from the parsed string/list provided, raises a 
    ValueError or ParserException on fail

        Rule    => Expr Expr BinOp | Expr
        Expr    => Expr | Expr UnPo | Expr Expr BinOp | Expr Digit BinOp
        Digit   => [0-9]+
        BinOp   => > | < | = | AND | OR
        UnOp    => NOT

    rule: list containing rule to parse
    '''
    def parseRule(self, rule):
        sensors = SensorList().getSensorObject()
        print(sensors.getSensorByID(1).temperature)
        
        print("Passing in rule list {0}" .format(rule))
        index = self.getFirstBinOperator(rule)
        print("Operator {0} at index: {1}" .format(rule[index], index))
        try:
            # Handling base case of recursive function
            if len(rule) == 1:
                if (rule[index] == "AND"):
                    self.ruleList.append("AND")
                elif (rule[index] == "OR"):
                    self.ruleList.append("OR")
                else:
                    raise ParserException("Invalid binary operator")
            elif (rule[index] == "GE"):
                try:
                    self.ruleList.append(Expression().greaterThan(sensors.getSensorByID(rule[index - 2]), int(rule[index - 1])))
                except (ValueError) as e:
                    pass
                print("{0} greater than {1}" .format(rule[index - 2], rule[index - 1]))
                if len(rule[index + 1:]) > 0:
                    self.parseRule(rule[index + 1:])
            elif (rule[index] == "LE"):
                try:
                    self.ruleList.append(Expression().lessThan(sensors.getSensorByID(rule[index - 2]), int(rule[index - 1])))
                except (ValueError) as e:
                    pass
                print("{0} less than {1}" .format(rule[index - 2], rule[index - 1]))
                if len(rule[index + 1:]) > 0:
                    self.parseRule(rule[index + 1:])
            elif (rule[index] == "EQ"):
                try:
                    self.ruleList.append(Expression().equalsTo(sensors.getSensorByID(rule[index - 2]), int(rule[index - 1])))
                except (ValueError) as e:
                    pass
                print("{0} equals to {1}" .format(rule[index - 2], rule[index - 1]))
                if len(rule[index + 1:]) > 0:
                    self.parseRule(rule[index + 1:])
            elif (rule[index] == "AND"):
                self.ruleList.append("AND")
                if len(rule[index + 1:]) > 0:
                    self.parseRule(rule[index + 1:])
            elif (rule[index] == "OR"):
                self.ruleList.append("OR")
                if len(rule[index + 1:]) > 0:
                    self.parseRule(rule[index + 1:])
            else:
                raise ParserException("Invalid binary operator")
        except (ValueError) as e:
            raise ParserException("Syntax validation failed")

        self.evaluate(self.ruleList)
    
    '''
    Returns the index of the first occurance of a str

    expression: expression to search

    return: 0 or index of expression
    '''
    def getFirstOccurance(self, expressions):
        for i in range(len(expressions)):
            if isinstance(expressions[i], str):
                return i
        return 0
    
    '''
    Returns the first occurance of a binary operator in a give list or 0
    if no relavent operator is present

    list: list to search

    return: index of binary operator or last element in list
    '''
    def getFirstBinOperator(self, list):
        listLength = len(list)
        index = listLength
        for i in range(listLength):
            if list[i] == "GE":
                index = min(index, i)
            elif list[i] == "LE":
                index = min(index, i)
            elif list[i] == "EQ":
                index = min(index, i)
            elif list[i] == "AND":
                index = min(index, i)
            elif list[i] == "OR":
                index = min(index, i)
            elif i == listLength - 1:
                print("No valid operator found in current iteration")
                print("Make sure to use one of the following: GE, LE, EQ, AND, OR")
                return 0
        
        return index
    
    '''
    Evaluates AND for two expressions

    expressionOne: first expression
    expressionTwo: second expression

    return: boolean result
    '''
    def evaluateAnd(self, expressionOne, expressionTwo):
        if expressionOne and expressionTwo:
            return True
        return False
    
    '''
    Evaluates OR for two expressions

    expressionOne: first expression
    expressionTwo: second expression

    return: boolean result
    '''
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