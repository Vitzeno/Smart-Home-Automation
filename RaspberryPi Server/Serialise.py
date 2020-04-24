import jsonpickle
import os

'''
Serailises an object

return: serialised object
'''
def serialiseObject(object):
    return jsonpickle.encode(object)

'''
Serailises an object and saves to file
CALLER MUST HANDLE IO EXCEPTIONS

object: object to serailises
filename: file to save to
directory: directory to save to

'''
def serialiseObjectToFile(object, filename, directory='config/'):
    f = open(filename, 'w')
    f.write(jsonpickle.encode(object))
    f.close()

'''
De-serailises an object from file
CALLER MUST HANDLE IO EXCEPTIONS

retunr: De-serailised object
'''
def deserialiseObjectFromFile(filename, directory='config/'):
    f = open(filename, 'r')
    object = jsonpickle.decode(f.read())
    f.close()
    return object

'''
De-serailises an object  

JSONString: sting to De-serailise

retunr: De-serailised object
'''
def deserialiseObject(JSONString):
    return jsonpickle.decode(JSONString)

'''
Sets to gloabal directory

directory: directory to set to 
'''
def setDirectory(directory='config/'):
    os.chdir(directory)
