class Devices:

    def __init__(self, id, name, lastKnownState = 0):
        self.id = id
        self.name = name
        self.lastKnownState = lastKnownState
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)