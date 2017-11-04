import json

class UsersResponse(object):
    """Top level response for /users endpoint"""
    def __init__(self, j):
        self.__json = json.loads(j)
        if self.__json != None and self.__json["data"] != None and len(self.__json["data"]) > 0:
                self.__user = User(self.__json["data"][0])
    
    @property
    def user(self):
        """User data"""
        try:
            self.__user
        except:
            return None
        return self.__user

class User(object):
    """Twitch user"""
    def __init__(self, data):
        self.__data = data

    @property
    def id(self):
        """User ID"""
        if self.__data != None and self.__data["id"] != None:
            return self.__data["id"]
        return ""

    @property
    def name(self):
        """Channel name"""
        if self.__data != None and self.__data["login"] != None:
            return self.__data["login"]
        return ""
    
    @property
    def displayName(self):
        """Channel display name"""
        if self.__data != None and self.__data["display_name"] != None:
            return self.__data["display_name"]
        return ""

    @property
    def viewCount(self):
        """View count of the channel"""
        if self.__data != None and self.__data["view_count"] != None:
            return self.__data["view_count"]
        return 0

    @property
    def type(self):
        """Channel type"""
        if self.__data != None and self.__data["type"] != None:
            return self.__data["type"]
        return ""

    @property
    def description(self):
        """Channel description"""
        if self.__data != None and self.__data["description"] != None:
            return self.__data["description"]
        return ""
