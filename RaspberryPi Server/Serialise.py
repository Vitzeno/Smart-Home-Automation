import jsonpickle
import os

def serialiseObject(object):
    return jsonpickle.encode(object)

def serialiseObjectToFile(object, filename, directory='config/'):
    f = open(filename, 'w')
    f.write(jsonpickle.encode(object))
    f.close()

'''
Any call to this method should hanlde its own exceptions
'''
def deserialiseObjectFromFile(filename, directory='config/'):
    f = open(filename, 'r')
    object = jsonpickle.decode(f.read())
    f.close()
    return object

def deserialiseObject(JSONString):
    return jsonpickle.decode(JSONString)

def setDirectory(directory='config/'):
    os.chdir(directory)
