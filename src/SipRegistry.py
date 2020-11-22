import json
import logging

class SipRegistry:
    def __init__(self, fileName):
        """
        Registry constructor that reads a file and builds a hashmap
        containing the links between the addresseses of records and the 
        string containing the entire records.
        """
        self.recordDict = {}
        for line in open(fileName, 'r') :
            sipRecord = json.loads(line)
            self.recordDict[sipRecord['addressOfRecord']] = line

    def getSipDataString(self, aor):
        """
        Returns the Sip record when given an address of record
        """
        try:
            sipDataString = self.recordDict[aor]
        except KeyError:
            logging.error(f"Sip address {aor} not found")
            sipDataString = "\n"
        return sipDataString
