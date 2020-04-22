import unittest
import sys
sys.path.append('../')
from RuleEvaluator import RuleEvaluator
from Expression import Expression
from Sensor import Sensor
from Rule import Rule

'''
Unit tests for rule evaluator
'''
class TestRuleEvaluator(unittest.TestCase):

    '''
    Sets up sensor and rule objects which will be used in the expression
    '''
    def setUp(self):
        self.s1 = Sensor(0, "Kitchen Sensor")
        self.s2 = Sensor(1, "Toilet Sensor")
        self.evaluator = RuleEvaluator()
    
    '''
    Test evaulator for know true values
    '''
    def test_evaluation_true(self):
        self.assertTrue(self.evaluator.evaluate( [Expression().equalsTo(self.s1, 0), Expression().equalsTo(self.s2, 0), "AND"]))
        self.assertTrue(self.evaluator.evaluate( [Expression().greaterThan(self.s1, 12), Expression().equalsTo(self.s2, 0), "OR"]))
        self.assertTrue(self.evaluator.evaluate( [Expression().lessThan(self.s1, 1), Expression().equalsTo(self.s2, 0), "AND"]))
        self.assertTrue(self.evaluator.evaluate( [Expression().equalsTo(self.s1, 0), Expression().lessThan(self.s2, 2), "AND"]))
        self.assertTrue(self.evaluator.evaluate( [Expression().equalsTo(self.s1, 0), Expression().greaterThan(self.s2, 12), "OR"]))

    '''
    Test evaulator for know false values
    '''
    def test_evaluation_false(self):
        self.assertFalse(self.evaluator.evaluate( [Expression().greaterThan(self.s1, 0), Expression().lessThan(self.s2, 0), "OR"]))
        self.assertFalse(self.evaluator.evaluate( [Expression().greaterThan(self.s1, 12), Expression().equalsTo(self.s2, 0), "AND"]))
        self.assertFalse(self.evaluator.evaluate( [Expression().lessThan(self.s1, 1), Expression().greaterThan(self.s2, 0), "AND"]))
        self.assertFalse(self.evaluator.evaluate( [Expression().equalsTo(self.s1, 4), Expression().lessThan(self.s2, 2), "AND"]))
        self.assertFalse(self.evaluator.evaluate( [Expression().equalsTo(self.s1, 62), Expression().greaterThan(self.s2, 12), "OR"]))

    '''
    Test evaulator for know nested true values
    '''
    def test_evaluation_nested_true(self):
        self.assertTrue(self.evaluator.evaluate( [Expression().lessThan(self.s1, 23), Expression().equalsTo(self.s2, 0), "AND", Expression().greaterThan(self.s1, 12), Expression().equalsTo(self.s2, 0), "OR", Expression().lessThan(self.s1, 12), Expression().lessThan(self.s2, 15), "OR", "OR", "AND"]))
        self.assertTrue(self.evaluator.evaluate( [Expression().equalsTo(self.s1, 0), Expression().greaterThan(self.s2, 3), "OR", Expression().lessThan(self.s1, 12), Expression().equalsTo(self.s2, 0), "AND", Expression().lessThan(self.s1, 12), Expression().greaterThan(self.s2, 15), "OR", "OR", "AND"]))
        self.assertTrue(self.evaluator.evaluate( [Expression().equalsTo(self.s1, 0), Expression().lessThan(self.s2, 24), "AND", Expression().equalsTo(self.s1, 0), Expression().greaterThan(self.s2, 12), "OR", Expression().lessThan(self.s1, 12), Expression().lessThan(self.s2, 15), "AND", "OR", "AND"]))
        self.assertTrue(self.evaluator.evaluate( [Expression().lessThan(self.s1, 21), Expression().lessThan(self.s2, 3), "AND", Expression().lessThan(self.s1, 12), Expression().equalsTo(self.s2, 0), "AND", Expression().lessThan(self.s1, 12), Expression().lessThan(self.s2, 15), "AND", "OR", "AND"]))
        self.assertTrue(self.evaluator.evaluate( [Expression().greaterThan(self.s1, 21), Expression().lessThan(self.s2, 3), "OR", Expression().lessThan(self.s1, 12), Expression().equalsTo(self.s2, 0), "AND", Expression().greaterThan(self.s1, 12), Expression().lessThan(self.s2, 15), "OR", "OR", "AND"]))

    '''
    Test evaulator for know nested false values
    '''
    def test_evaluation_nested_false(self):
        self.assertFalse(self.evaluator.evaluate( [Expression().greaterThan(self.s1, 23), Expression().equalsTo(self.s2, 5), "OR", Expression().greaterThan(self.s1, 12), Expression().equalsTo(self.s2, 0), "OR", Expression().lessThan(self.s1, 12), Expression().lessThan(self.s2, 15), "OR", "OR", "AND"]))
        self.assertFalse(self.evaluator.evaluate( [Expression().equalsTo(self.s1, 0), Expression().greaterThan(self.s2, 3), "AND", Expression().lessThan(self.s1, 12), Expression().equalsTo(self.s2, 0), "AND", Expression().equalsTo(self.s1, 12), Expression().greaterThan(self.s2, 15), "OR", "OR", "AND"]))
        self.assertFalse(self.evaluator.evaluate( [Expression().equalsTo(self.s1, 0), Expression().lessThan(self.s2, 24), "AND", Expression().equalsTo(self.s1, 0), Expression().greaterThan(self.s2, 12), "AND", Expression().lessThan(self.s1, 12), Expression().equalsTo(self.s2, 15), "AND", "OR", "AND"]))
        self.assertFalse(self.evaluator.evaluate( [Expression().lessThan(self.s1, 21), Expression().lessThan(self.s2, 3), "AND", Expression().lessThan(self.s1, 12), Expression().equalsTo(self.s2, 13), "AND", Expression().lessThan(self.s1, 12), Expression().lessThan(self.s2, 15), "AND", "AND", "AND"]))
        self.assertFalse(self.evaluator.evaluate( [Expression().greaterThan(self.s1, 21), Expression().lessThan(self.s2, 3), "OR", Expression().lessThan(self.s1, 12), Expression().greaterThan(self.s2, 0), "AND", Expression().greaterThan(self.s1, 12), Expression().lessThan(self.s2, 15), "AND", "OR", "AND"]))

    '''
    Test evaluator for known singualr true values
    '''
    def test_evaluation_singular_true(self):
        self.assertTrue(self.evaluator.evaluate( [Expression().lessThan(self.s1, 23)]))
        self.assertTrue(self.evaluator.evaluate([Expression().equalsTo(self.s1, 0)]))
        self.assertTrue(self.evaluator.evaluate([Expression().lessThan(self.s1, 14)]))
        self.assertTrue(self.evaluator.evaluate([Expression().equalsTo(self.s1, 0)]))
        self.assertTrue(self.evaluator.evaluate([Expression().lessThan(self.s1, 45)]))

    '''
    Test evaluator for known singualr false values
    '''
    def test_evaluation_singular_false(self):
        self.assertFalse(self.evaluator.evaluate([Expression().greaterThan(self.s1, 23)]))
        self.assertFalse(self.evaluator.evaluate([Expression().equalsTo(self.s1, 23)]))
        self.assertFalse(self.evaluator.evaluate([Expression().lessThan(self.s1, -14)]))
        self.assertFalse(self.evaluator.evaluate([Expression().equalsTo(self.s1, 34)]))
        self.assertFalse(self.evaluator.evaluate([Expression().lessThan(self.s1, -45)]))

if __name__ == '__main__': 
    unittest.main() 