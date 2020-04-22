import unittest
import sys
sys.path.append('../')
from Expression import Expression
from Sensor import Sensor

'''
Unit tests for expressions
'''
class TestExpressions(unittest.TestCase):

    '''
    Set up sensor objects used by expressions
    '''
    def setUp(self):
        self.s1 = Sensor(0, "Kitchen Sensor")
        self.s2 = Sensor(1, "Toilet Sensor")

    '''
    Test expression to digit for known true values
    '''
    def test_expr_digit_true(self):
        self.assertTrue(Expression().lessThan(self.s1, 23))
        self.assertTrue(Expression().equalsTo(self.s1, 0))
        self.assertTrue(Expression().greaterThan(self.s1, -15))
        self.assertTrue(Expression().lessThan(self.s1, 65))
        self.assertTrue(Expression().equalsTo(self.s2, 0))

    '''
    Test expression to digit for known false values
    '''
    def test_expr_digit_false(self):
        self.assertFalse(Expression().greaterThan(self.s1, 25))
        self.assertFalse(Expression().equalsTo(self.s2, 8))
        self.assertFalse(Expression().lessThan(self.s1, -14))
        self.assertFalse(Expression().greaterThan(self.s2, 5))
        self.assertFalse(Expression().equalsTo(self.s1, 12))

    '''
    Test expression to expression for known true values
    '''
    def test_expr_expr_true(self):
        self.assertTrue(Expression().equalsToExpr(self.s1, self.s2))
        self.assertTrue(Expression().equalsToExpr(self.s2, self.s1))
        self.assertTrue(Expression().equalsToExpr(self.s1, self.s1))
        self.assertTrue(Expression().equalsToExpr(self.s2, self.s2))

        '''
    Test expression to expression for known false values
    '''
    def test_expr_expr_false(self):
        self.assertFalse(Expression().lessThanExpr(self.s1, self.s2))
        self.assertFalse(Expression().greaterThanExpr(self.s2, self.s1))
        self.assertFalse(Expression().greaterThanExpr(self.s1, self.s1))
        self.assertFalse(Expression().lessThanExpr(self.s2, self.s2))
        self.assertFalse(Expression().greaterThanExpr(self.s2, self.s2))

if __name__ == '__main__': 
    unittest.main() 