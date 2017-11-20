import socket
import threading
import time
import datetime

class IRC:
    """IRC connection"""
    def __init__(self, chatToken, chatUsername, user, stream):
        self.killMe = False     # If this is set to True the listen thread will terminate and socket will close
        self.tryReconnect = False    # If this is set to True the listen thread will try to reconnect every 30 seconds
        self.chatToken = chatToken
        self.chatUsername = chatUsername
        self.user = user
        self.stream = stream
    
    def connect(self, url, port):
        print("IRC connecting to chat {} on port {}".format(url, port))
        self.url = url
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((url, port))
        self.tryReconnect = False
        self.JoinServer(self.chatToken, self.chatUsername)
        self.JoinChannel(self.user.name)
        # Start listener only once
        if hasattr(self, "listenThread") == False:
            self.startListener()
    
    def startListener(self):
        self.listenThread = threading.Thread(target=self.Listener)
        self.listenThread.start()

    def close(self):
        print("IRC closing connection...")
        self.killMe = True
        # Make sure that the socket is closed
        if self.socket._closed == False:
            self.socket.close
        print("IRC connection closed.")

    def sendData(self, command):
        data = str.encode(command + "\n")
        self.socket.send(data)
    
    def Listener(self):
        print("IRC chat listener thread started...")
        #self.SendChannelMessage("noiya00", "LUL Kappa Keepo")
        
        #self.killMe = True
        self.socket.setblocking(False)

        # Start listener
        while (1):
            # If killMe flag is set to True return
            if self.killMe:
                print("KILLING LISTENER")
                return

            buffer = None
            try:
                buffer = self.socket.recv(1024)
            except socket.error:
                """no data on socket yet"""
                #print("no data on socket yet...")
                
            if buffer != None:
                bufferStr = str(buffer)

                print("\t" + bufferStr)
                msg = str.split(bufferStr)

                if len(msg) > 1: 
                    command = msg[1]

                    # Respond for PING
                    if msg[0][:4] == b"PING":
                        print("PONG!")
                        self.socket.send("PONG")
                    elif len(msg) >= 3:
                        channel = msg[2]
                        # If channel starts with # remove it
                        if channel[0] == "#":
                            channel = channel[1:]
                        # Remove first : character in message and lat 4 characters which are \r\n
                        text = msg[3].strip()[1:-5]
                        print("message type {} in channel {} with text {}".format(command, channel, text))
                        if command == "PRIVMSG":
                            # Check if this is bot command
                            if text == "!uptime":
                                print("Command: !uptime")
                                if self.stream == None:
                                    self.SendChannelMessage(channel, "Offline FeelsBadMan")
                                else:
                                    streamTimeSeconds = self.stream.timedeltaSinceStart.seconds
                                    strStreamTime = "{:02}:{:02}:{:02}".format(streamTimeSeconds // 3600, streamTimeSeconds % 3600 // 60, streamTimeSeconds % 60)
                                    game = ""
                                    if self.stream.game != None:
                                        game = self.stream.game
                                    self.SendChannelMessage(channel, "{} is streaming {} for {} PogChamp".format(self.user.name, game, strStreamTime))
                            elif text == "!social":
                                print("Command: !social")
                                self.SendChannelMessage(channel, "Podążaj za noiya00 na twitter: https://twitter.com/noiya00 i facebook: https://www.facebook.com/noiya00 Kappa")
                else:
                    # Zero length string received - socket probably closed
                    print("reconnecting")
                    # Make sure that the socket is closed
                    if self.socket._closed == False:
                        self.socket.close()
                    # Open new socket to IRC
                    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.socket.connect((self.url, self.port))
                    self.tryReconnect = False
                    # Join server and chat
                    self.JoinServer(self.chatToken, self.chatUsername)
                    self.JoinChannel(self.user.name)
                    return
    
    def JoinServer(self, oauth, nick):
        print("IRC join server as " + nick + "...")
        self.sendData("PASS " + oauth)
        self.sendData("NICK " + nick)
        # Wait for response
        buffer = self.socket.recv(1024)
        msg = str.split(str(buffer))
        print("\t" + str(buffer))

    def JoinChannel(self, channel):
        print("IRC join channel " + channel + "...")
        self.sendData("JOIN #" + channel)
        # Wait for response
        buffer = self.socket.recv(1024)
        msg = str.split(str(buffer))
        print("\t" + str(buffer))
        # Second response
        buffer = self.socket.recv(1024)
        msg = str.split(str(buffer))
        print("\t" + str(buffer))

    def SendChannelMessage(self, channel, message):
        print("IRC sending message " + message + " to channel #" + channel + "...")
        self.sendData("PRIVMSG #" + channel + " :" + message)
