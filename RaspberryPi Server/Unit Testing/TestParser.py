import unittest
import sys
sys.path.append('../')
from Parser import Parser
from ParserException import ParserException

'''
Unit tests for the parser

Since parser performs and action on suceess and does not return anything, the only way
to test it is to try invalid commands
'''
class TestParser(unittest.TestCase):

    def setUp(self):
        self.p = Parser()

    def test_invalid_input(self):
        self.assertRaises(ParserException, self.p.parseInput, "F:32")
        self.assertRaises(ParserException, self.p.parseInput, "G:3:2")
        self.assertRaises(ParserException, self.p.parseInput, "D:F:3:2")
        self.assertRaises(ParserException, self.p.parseInput, "g2")
        self.assertRaises(ParserException, self.p.parseInput, "S1:0:EQ:S2:12:LE:OR")
    
    def test_invalid_command(self):
        self.assertRaises(ParserException, self.p.parseInput, "C:32")
        self.assertRaises(ParserException, self.p.parseInput, "C:3:2")
        self.assertRaises(ParserException, self.p.parseInput, "C:F:3:2")
        self.assertRaises(ParserException, self.p.parseInput, "C:2")
        self.assertRaises(ParserException, self.p.parseInput, "C::0:EQ:S2:12:LE:OR")

    def test_invalid_device(self):
        self.assertRaises(ParserException, self.p.parseInput, "C:D:32")
        self.assertRaises(ParserException, self.p.parseInput, "C:D:3:2")
        self.assertRaises(ParserException, self.p.parseInput, "C:D:F:3:2")
        self.assertRaises(ParserException, self.p.parseInput, "C:D:2")
        self.assertRaises(ParserException, self.p.parseInput, "C:D:0:EQ:S2:12:LE:OR")

    def test_invalid_group(self):
        self.assertRaises(ParserException, self.p.parseInput, "C:G:3;32")
        self.assertRaises(ParserException, self.p.parseInput, "C:G:R:3:2")
        self.assertRaises(ParserException, self.p.parseInput, "C:G:F:3:2")
        self.assertRaises(ParserException, self.p.parseInput, "C:G:2:T")
        self.assertRaises(ParserException, self.p.parseInput, "C:G:0:EQ:S2:12:LE:OR")

    def test_invalid_rule(self):
        self.assertRaises(ParserException, self.p.parseInput, "C:R:G;34:")
        self.assertRaises(ParserException, self.p.parseInput, "C:R:3:2")
        self.assertRaises(ParserException, self.p.parseInput, "C:R:F:4:OR:AND")
        self.assertRaises(ParserException, self.p.parseInput, "C:R:2")
        self.assertRaises(ParserException, self.p.parseInput, "C:R:0:EQ:S2:12:LE:OR")

    def test_invalid_request(self):
        pass

if __name__ == '__main__': 
    unittest.main() 