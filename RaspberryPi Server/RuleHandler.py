import time
import Radio as Radio

from Rule import Rule
from RuleList import RuleList
from RuleEvaluator import RuleEvaluator

from Devices import Devices
from DeviceList import DeviceList


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

            for i in range (1, ruleList.counter + 1):
                try:
                    ruleEval = RuleEvaluator()
                    currentRule = ruleList.getRuleByID(i)
                    print("************************************************************************")
                    print("\n RULE HANDLER THREAD \n")
                    print("************************************************************************")

                    targetDevice = currentRule.getTarget()
                    print("Rule Targeting Device: {0}" .format(targetDevice)) 

                    state = ruleEval.parseRule(currentRule.parsableRule)
                    print("Evalauted to {0} \n" .format(state))

                    if state:
                        print("Switching device {0} to {1}" .format(targetDevice, state))
                        Radio.switchSocket(int(targetDevice), state)

                except (ValueError) as e:
                    print("Rule with ID {0} not in rule list" .format(i))
   
            time.sleep(30)



        
    