import unittest
import sys
import os
sys.path.append('../')
from SensorList import SensorList
from GroupList import GroupList
from DeviceList import DeviceList
from RuleList import RuleList

'''
Unit tests for singleton list objects from file
'''
class TestSingletons(unittest.TestCase):

    '''
    Set up singleton objects to be used in tests
    '''
    def setUp(self):
        self.deviceList = DeviceList().getDevicesObject()
        self.groupList = GroupList().getGroupObject() 
        self.ruleList = RuleList().getRuleObject()
        self.sensorList = SensorList().getSensorObject()

    '''
    Ensureing object created or read from file are of correct type
    '''
    def test_object_type(self):
        self.assertIs(self.deviceList, DeviceList().getDevicesObject())
        self.assertIs(self.sensorList, SensorList().getSensorObject())
        self.assertIs(self.groupList, GroupList().getGroupObject() )
        self.assertIs(self.ruleList, RuleList().getRuleObject())

    '''
    Deletes new files created for testing purposes
    '''
    def tearDown(self):
        try:
            os.remove("SensorList")
            os.remove("RuleList")
            os.remove("GroupList")
            os.remove("DeviceList")
        except (IOError, OSError, FileNotFoundError) as e:
            print(e)
        
if __name__ == '__main__': 
    unittest.main() 