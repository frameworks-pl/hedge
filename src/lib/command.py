

class Command:

    def __init__(self, commandItems, runWithSudo=False):

        # if command is string, convert it to array
        if isinstance(commandItems, str):
            commandItems = commandItems.split(" ")

        self.commandItems = commandItems
        self.runWithSudo = runWithSudo

    def getArray(self):

        # check if we need to run with sudo
        if self.runWithSudo:

            # check if sudo is already in command
            if self.commandItems[0] != 'sudo':
                self.commandItems.insert(0, 'sudo')

        return self.commandItems

    def getAsString(self):
        """
        Returns final version of command as string
        """
        return " ".join(self.getArray())

    def add(self, params):
        self.commandItems.extend(params)