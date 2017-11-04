import json

class Config(object):
    """Config object"""
    def __init__(self, file):
        with open(file) as json_data:
            self.__json = json.load(json_data)
    
    def validateSelf(self):
        # Client ID
        if self.clientID == None or self.clientID == "":
            print("No clientID found in config file")
            return False
        # Channel name
        if self.channelName == None or self.channelName == "":
            print("No channelName found in config file")
            return False

        return True

    @property
    def clientID(self):
        """Client ID for twitch API"""
        if self.__json != None and self.__json["clientID"] != None:
            return self.__json["clientID"]
        return ""

    @property
    def channelName(self):
        """Name of the channel to hook onto"""
        if self.__json != None and self.__json["channelName"] != None:
            return self.__json["channelName"]
        return ""
