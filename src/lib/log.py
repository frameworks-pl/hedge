from colorama import init, Fore, Back, Style

class Log:    

    def __init__(self, autoFlush = True):
        init(autoreset=True)
        self.autoFlush = autoFlush

    def addPending(self, entry):
        self.entry = entry

    def commitOK(self):
        self.result = "OK"
        if self.autoFlush == True:
            self.flush()        

    def commitFAIL(self):
        self.result = "FAIL"
        if self.autoFlush == True:
            self.flush()        

    def flush(self):
        output = "{entry} {result}".format(entry=self.entry,result=self.result)        
        c = Fore.GREEN if self.result == "OK" else Fore.RED
        print(self.entry + " " + c + self.result)
        self.entry = None
        return output
