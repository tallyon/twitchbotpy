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
        # Chat token
        if self.chatToken == None or self.chatToken == "":
            print("No chatToken found in config file")
            return False
        # Chat username
        if self.chatUsername == None or self.chatUsername == "":
            print("No chatUsername found in config file")
            return False
        # Data update interval
        if self.updateDataInterval == None or self.updateDataInterval <= 0:
            print("No updateDataInterval found in config file")
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

    @property
    def chatToken(self):
        """Twitch chat user token to connect with"""
        if self.__json != None and self.__json["chatToken"] != None:
            return self.__json["chatToken"]
        return ""

    @property
    def chatUsername(self):
        """Twitch chat username to connect with"""
        if self.__json != None and self.__json["chatUsername"] != None:
            return self.__json["chatUsername"]
        return ""

    @property
    def updateDataInterval(self):
        """Interval in seconds at which twitch channel and stream data will be updated"""
        if self.__json != None and self.__json["updateDataInterval"] != None:
            return self.__json["updateDataInterval"]
        return 0
