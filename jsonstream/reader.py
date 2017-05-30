import json

class stream:
    def __init__(self, path):
        self.path = path
        self.file = open(path, "r")
        self.isArray = False
        self.buffer = ""
        self.bytesPerRead = 2048

        first = self.file.read(1)
        if first == "[":
            self.isArray = True

    def readIntoBuffer(self):
        previousLength = len(self.buffer)
        self.buffer += self.file.read(self.bytesPerRead)
        if previousLength < len(self.buffer):
            return True
        else:
            return False

    def getObjectCloseOffset(self):
        fromBuffer = 0
        balance = 0
        for nextCharacter in self.buffer:
            fromBuffer += 1
            if nextCharacter == "{":
                balance += 1
            elif nextCharacter == "}":
                balance -= 1
                if balance == 0:
                    break

        if balance != 0:
            return False
        return fromBuffer

    def nextObject(self):
        if self.isArray == False:
            return False

        if len(self.buffer) < 1:
            self.readIntoBuffer()

        while self.buffer[0] != "{":
            self.buffer = self.buffer[1:]
            if len(self.buffer) < 1:
                if self.readIntoBuffer() == False:
                    return False

        fromBuffer = self.getObjectCloseOffset()
        while fromBuffer == False:
            if self.readIntoBuffer() == False:
                return False
            fromBuffer = self.getObjectCloseOffset()

        objectString = self.buffer[:fromBuffer]
        self.buffer = self.buffer[fromBuffer:]
        return json.loads(objectString)
