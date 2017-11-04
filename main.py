import http.client
import json

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

    if streamResponse.stream != None:
        print("Streaming {} with {} viewers for {} with average FPS of {}".format(
            streamResponse.stream.game,
            streamResponse.stream.viewers,
            streamResponse.stream.timedeltaSinceStart,
            streamResponse.stream.avgFPS
        ))
    else:
        print("Stream offline")

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


if __name__ == "__main__":
    main()