Uses both v5 and new Twitch API to provide Twitch channel summary and statistics.

## Running

**Python 3 required**. Written and tested on 3.6

To run use
```python main.py```

## Config

Make sure there is a file config.json in root directory (where main.py is located). There is a template named config.template.json that you can use after setting config values there.

**config.channelName** is a string - name of the Twitch channel that you want to get stats for  
**config.clientID** is your Twitch dev app ID  
**config.chatUsername** is your twitch chat username that will be used to connect to twitch irc  
**config.chatToken** is your user twitch chat token beggining with oauth:  
**config.updateDataInterval** is time in seconds that will be update interval for channel and stream data

## Twitch chat commands

**!uptime** sends "Offline FeelsBadMan" if stream is offline or uptime in format HH:MM:SS  
**!social** sends custom string defined in IRC class "Podążaj za noiya00 na twitter: https://twitter.com/noiya00 i facebook: https://www.facebook.com/noiya00 Kappa"
