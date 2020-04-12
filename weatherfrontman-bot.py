import tweepy
import codecs
import my_keys
import requests
import json
import random

def getresponse(locale):
    combined = locale

    # Set them up as parameters for the query
    params = {'q' : combined,
          'appid' : my_keys.WEATHER
      }

    # Pass the GET request with the right parameters, then parse the results
    weather = requests.get("https://api.openweathermap.org/data/2.5/weather", params=params)
    weather_parsed = json.loads(weather.text)
    weather_condition = weather_parsed['weather'][0]['main']

    # Now that's done, search Genius for the weather conditions found above. (The access_token is from the OAuth registered with the site.)
    params2 = {'q' : weather_condition,
           'access_token' : my_keys.GENIUS
          }
    song = requests.get("http://api.genius.com/search", params=params2)
    song_parsed = json.loads(song.text)

    # Get the list of songs
    song_postparsed = song_parsed['response']['hits']

    # Choose one of these songs at random and get its title
    chosen_song = random.randint(0,(len(song_postparsed)-1))
    song_title = song_postparsed[chosen_song]['result']['full_title']

    # Return the results, both unhelpful and helpful
    # The .split method divides the string at the comma and returns everything before it
    sentence = "They're playing " + song_title + " over in " + locale.split(', ', 1)[0] + "! (Because it's " + weather_condition + " there, obviously.)"
    return sentence

# Get the authentication keys from my_keys.py
CONSUMER_KEY = my_keys.CONSUMER_KEY
CONSUMER_SECRET = my_keys.CONSUMER_SECRET
ACCESS_KEY = my_keys.ACCESS_KEY
ACCESS_SECRET = my_keys.ACCESS_SECRET

# Authenticate to Twitter with our keys
auth1 = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth1.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth1)

class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        tweet = status.text
        userid = status.author.screen_name
        tweetid = status.id
        
        # The .split method divides the string at the first space and returns everything after it
        weathertweet = getresponse(tweet.split(' ', 1)[1])
        
        if not ('RT @' in tweet) :  
            print("\"%s\",\"%s\",\"%s\"" % (weathertweet,userid,tweetid))
            api.update_status(status="@" + userid + " " + weathertweet + " #dhsiapi #dhsi18", in_reply_to_status_id=status.id)

# Connect to the streaming API and print tweets matching our keywords
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

# Now define the string to listen for in Twitter
print(myStream.filter(track=['@weatherfrontman']))
