import time
import Radio as Radio

from Rule import Rule
from RuleList import RuleList
from RuleEvaluator import RuleEvaluator

from Devices import Devices
from DeviceList import DeviceList

from SensorList import SensorList


class RuleHandler():

    currentTagret = None

    '''
    Separate thread

    Loops through all rules and evaluates them using the RuleEvaluator class, if a rule evaluates to True
    the target decive is turned on. Target devices are tied to each rule.
    '''
    @classmethod
    def beginEvaluation(cls):
        while True:
            
            deviceList = DeviceList().getDevicesObject()
            ruleList = RuleList().getRuleObject()
            sensorList = SensorList().getSensorObject()

            for i in range (1, ruleList.counter + 1):
                try:
                    sensorList.updateSensors()

                    ruleEval = RuleEvaluator()
                    currentRule = ruleList.getRuleByID(i)
                    print("************************************************************************")
                    print("\n RULE {0} HANDLER THREAD \n" .format(i))
                    print("************************************************************************")

                    print(sensorList.toStringFormat())

                    targetDevice = currentRule.getTarget()
                    targetDeviceObject = deviceList.getDeviceByID(targetDevice)
                    targetState = currentRule.getState()
                    print("Rule: {0}" .format(currentRule.rule))
                    print("Rule Targeting Device: {0}" .format(targetDevice)) 
                    print("Rule Targeting State: {0}" .format(targetState)) 

                    state = bool(ruleEval.parseRule(currentRule.parsableRule))
                    print("Evalauted to {0} \n" .format(state))

                    if state:
                        print("Switching device {0} to {1}" .format(int(targetDevice), bool(targetState)))
                        targetDeviceObject.lastKnownState = bool(targetState)
                        Radio.switchSocket(int(targetDevice), bool(targetState))
                        deviceList.setDevicesObject()

                except (ValueError) as e:
                    print("Rule with ID {0} not in rule list" .format(i))
   
            time.sleep(30)



        
    