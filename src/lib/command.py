

class Command:

    def __init__(self, commandItems):
        self.commandItems = commandItems

    def getArray(self):
        return self.commandItems

    def add(self, params):
        self.commandItems.extend(params)