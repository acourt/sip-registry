import json

class SipRegistry:
    def __init__(self, fileName):
        self.recordDict = {}
        for line in open(fileName, 'r') :
            sipRecord = json.loads(line)
            self.recordDict[sipRecord['addressOfRecord']] = line

    def getSipDataString(self, aor):
        """
        docstring
        """
        return self.recordDict[aor]

