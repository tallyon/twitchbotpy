import http.client
import json
import sys
import time
import threading
import irc

# import models
import models.config
import models.twitch.user
import models.twitch.stream

def main():
    # Parse config file
    config = models.config.Config("config.json")
    # Validate config
    if config.validateSelf() == False:
        print("config invalid! exiting...")
        exit()
    else:
        print("config valid, continue...")

    print("Getting twitch channel " + config.channelName + " data...\n")

    # Get twitch user data
    response = GetTwitchUser(config.channelName, config.clientID)
    # print(str(response) + "\n\n")
    userResponse = models.twitch.user.UsersResponse(response)
    user = userResponse.user

    print("Twitch channel {} (login: {}, ID: {})\nView count: {}\nChannel type: {}\nDescription: {}".format(
        userResponse.user.displayName,
        userResponse.user.name,
        userResponse.user.id,
        userResponse.user.viewCount,
        userResponse.user.type,
        userResponse.user.description))

    # Get twitch user data from new api
    response = GetTwitchUserNew(userResponse.user.id, config.clientID)
    # print(str(response) + "\n\n")

    # Get twitch user stream data
    response = GetTwitchUserStream(userResponse.user.id, config.clientID)
    # print(str(response) + "\n\n")

    streamResponse = models.twitch.stream.StreamResponse(response)
    stream = streamResponse.stream

    if streamResponse.stream != None:
        print("Streaming {} with {} viewers for {} with average FPS of {}".format(
            streamResponse.stream.game,
            streamResponse.stream.viewers,
            streamResponse.stream.timedeltaSinceStart,
            streamResponse.stream.avgFPS
        ))
    else:
        print("Stream offline")

    print("\n\n=====================================\nFinished initial data fetching!\n=====================================\n\n")

    print("Starting autoupdater of user data for channel {} every {} seconds".format(config.channelName, config.updateDataInterval))
    autoupdateUserDataTimer = autoupdateUserData(config.updateDataInterval, config.clientID, config.channelName, user)

    print("Starting autoupdater of stream data for user {} every {} seconds".format(userResponse.user.displayName, config.updateDataInterval))
    autoUpdateStreamDataTimer =  autoupdateStreamData(config.updateDataInterval, config.clientID, userResponse.user.id, stream)

    print("\n\n=====================================\nFinished starting autoupdaters!\n=====================================\n\n")

    # Connect to twitch chat irc
    chat = irc.IRC(config.chatToken, config.chatUsername , user, stream)
    chat.connect("irc.chat.twitch.tv", 6667)
    
    stdinControl(chat)
    autoupdateUserDataTimer.cancel()
    autoUpdateStreamDataTimer.cancel()
    print("TwitchBotPrime dies.")
    sys.exit(0)

def getToString(host, path):
    conn = http.client.HTTPSConnection(host)
    conn.request("GET", path)
    response = conn.getresponse()
    readAll = response.read()
    conn.close()
    return readAll

def GetTwitchUser(name, clientID):
    conn = http.client.HTTPSConnection("api.twitch.tv")
    headers = {
        "Client-ID": clientID
    }
    conn.request("GET", "/helix/users?login=" + name, None, headers)
    response = conn.getresponse()
    readAll = response.read()
    conn.close()
    return readAll

def GetTwitchUserNew(userID, clientID):
    conn = http.client.HTTPSConnection("api.twitch.tv")
    headers = {
        "Client-ID": clientID,
        "Accept": "application/vnd.twitchtv.v5+json"
    }
    conn.request("GET", "/kraken/users/" + userID, None, headers)
    response = conn.getresponse()
    readAll = response.read()
    conn.close()
    return readAll

def GetTwitchUserStream(userID, clientID):
    conn = http.client.HTTPSConnection("api.twitch.tv")
    headers = {
        "Client-ID": clientID,
        "Accept": "application/vnd.twitchtv.v5+json"
    }
    conn.request("GET", "/kraken/streams/" + userID, None, headers)
    response = conn.getresponse()
    readAll = response.read()
    conn.close()
    return readAll

def stdinControl(chat):
    print("Type exit to quit")
    while True:
        laststdin = sys.stdin.readline().strip()
        if len(laststdin) < 1:
            continue
        elif laststdin == "exit":
            print("Exiting in 5 seconds...")
            chat.close()
            time.sleep(5)
            return
        else:
            print("Unknown command: {}".format(laststdin))

def autoupdateUserData(intervalSeconds, clientID, channelName, userDataObject):
    print(object.__repr__(userDataObject))
    # Get twitch user data
    response = GetTwitchUser(channelName, clientID)
    # print(str(response) + "\n\n")
    userResponse = models.twitch.user.UsersResponse(response)
    userDataObject = userResponse.user

    if userDataObject != None:
        print("Updated user data:\n\tTwitch channel {} (login: {}, ID: {})\nView count: {}\nChannel type: {}\nDescription: {}".format(
            userDataObject.displayName,
            userDataObject.name,
            userDataObject.id,
            userDataObject.viewCount,
            userDataObject.type,
            userDataObject.description))
    else:
        print("Could no fetch user data for channel {}".format(channelName))
    
    # repeat after provided interval
    timer = threading.Timer(intervalSeconds, autoupdateUserData, args=[intervalSeconds, clientID, channelName, userDataObject])
    timer.daemon = True
    timer.start()
    return timer

def autoupdateStreamData(intervalSeconds, clientID, userID, streamDataObject):
    response = GetTwitchUserStream(userID, clientID)
    streamResponse = models.twitch.stream.StreamResponse(response)
    streamDataObject = streamResponse.stream
    
    if streamDataObject != None:
        print("Updated stream data:\n\tStreaming {} with {} viewers for {} with average FPS of {}".format(
            streamDataObject.game,
            streamDataObject.viewers,
            streamDataObject.timedeltaSinceStart,
            streamDataObject.avgFPS
        ))
    else:
        print("Stream offline")

    # repeat after provided interval
    timer = threading.Timer(intervalSeconds, autoupdateStreamData, args=[intervalSeconds, clientID, userID, streamDataObject])
    timer.daemon = True
    timer.start()
    return timer

if __name__ == "__main__":
    main()