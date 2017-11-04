import json
import dateutil.parser
import datetime

class StreamResponse(object):
    """Top level response from /kraken/streams endpoint"""
    def __init__(self, j):
        self.__json = json.loads(j)
        if self.__json["stream"] != None:
            self.__stream = Stream(self.__json["stream"])

    @property
    def stream(self):
        """Stream data"""
        if hasattr(self, "__stream"):
            return self.__stream
        return None

class Stream(object):
    """Twitch stream"""
    def __init__(self, data):
        self.__data = data

    @property
    def game(self):
        """Current game name"""
        if self.__data != None and self.__data["game"] != None:
            return self.__data["game"]
        return ""
    
    @property
    def viewers(self):
        """Current stream viewers number"""
        if self.__data != None and self.__data["viewers"] != None:
            return self.__data["viewers"]
        return -1

    @property
    def createdTimestamp(self):
        """Timestamp (second based) when stream was created"""
        if self.__data != None and self.__data["created_at"] != None:
            return self.createdDatetime.timestamp()
        return -1

    @property
    def createdDatetime(self):
        """Datetime when stream was created"""
        if self.__data != None and self.__data["created_at"] != None:
            return dateutil.parser.parse(self.__data["created_at"], None, ignoretz=True)

    @property
    def timedeltaSinceStart(self):
        """Time delta object since stream has started until now"""
        return datetime.datetime.utcnow() - self.createdDatetime

    @property
    def avgFPS(self):
        """Average FPS of the stream"""
        if self.__data != None and self.__data["average_fps"] != None:
            return self.__data["average_fps"]
        return -1
