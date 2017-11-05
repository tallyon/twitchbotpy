import socket
import threading
import time

class IRC:
    """IRC connection"""
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.killMe = False     # If this is set to True the listen thread will terminate and socket will close
    
    def connect(self, url, port):
        print("IRC connecting to chat {} on port {}".format(url, port))
        self.socket.connect((url, port))
        self.listenThread = threading.Thread(target=self.Listener)
        self.listenThread.start()
        # self.Listener()
    
    def close(self):
        print("IRC closing connection...")
        self.killMe = True
        # self.listenThread.join(timeout=5)
        # self.socket.close()
        print("IRC connection closed.")

    def sendData(self, command):
        data = str.encode(command + "\n")
        self.socket.send(data)
    
    def Listener(self):
        print("IRC chat listener thread started...")
        self.JoinServer("oauth:yhgkal2xb81cfrkwa2nw7u25wjk1ar", "thallyon")
        self.JoinChannel("noiya00")
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
                msg = str.split(str(buffer))
                command = msg[1]
                channel = msg[2]
                # If channel starts with # remove it
                if channel[0] == "#":
                    channel = channel[1:]
                # Remove first : character in message and lat 4 characters which are \r\n
                text = msg[3].strip()[1:-5]
                print("\t" + str(buffer))
                print("message type {} in channel {} with text {}".format(command, channel, text))
                if command == "PING":
                    print("Pinged!")
                    self.socket.send("PONG %s" % text + "\n")
                elif command == "PRIVMSG":
                    # Check if this is bot command
                    if text == "!uptime":
                        self.SendChannelMessage(channel, "UPTIME HERE")
    
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
