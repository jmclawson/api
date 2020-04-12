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
    weather_description = weather_parsed['weather'][0]['description']
    weather_icon = weather_parsed['weather'][0]['icon']
    weather_id = weather_parsed['weather'][0]['id']
    
    #weather_dictionary = {"01d":"u'\U00001F31E'", 
    #                     "01n":"u'\U00001F31D'", 
    #                     "04d":"u'\U00002601'"}
    #for key in weather_dictionary.keys():
    #    weather_icon = weather_icon.replace(key, weather_dictionary[key])
    
    weather_emoji = ""  
    if weather_icon == "01n":# clear-night
        weather_emoji = random.choice([u'\U0001F31D', u'\U0001F303', u'\U0001F30C'])

    if weather_icon == "01d":# clear-day
        weather_emoji = random.choice([u'\U0001F31E', u'\U00002600'])
        
    if weather_id in range (200, 232):# thunderstorms
        weather_emoji = u'\U000026C8'
        
    if weather_id in range (300, 399):# drizzles
        weather_emoji = u'\U00002614'
        
    if weather_id in range (500, 599):# rain
        weather_emoji = u'\U0001F327'
        
    if weather_id in range (600, 699):# snow
        weather_emoji = u'\U00002603'
        
    if weather_id in range (700, 761):# haze
        weather_emoji = u'\U0001F32B'
        
    if weather_id == 762:# ash
        weather_emoji = u'\U0001F30B'
        
    if weather_id == 771:# squall
        weather_emoji = u'\U0001F32C'
        
    if weather_id == 741:# foggy special
        weather_emoji = u'\U0001F301'
        
    if weather_id == 781:# tornado
        weather_emoji = u'\U0001F32A'
        
    if weather_id == 511:# freezing rain
        weather_emoji = u'\U00002744'
        
    if weather_id == 801:# clouds1
        weather_emoji = u'\U0001F324'
        
    if weather_id == 802:# clouds2
        weather_emoji = u'\U000026C5'
        
    if weather_id == 803:# clouds3
        weather_emoji = u'\U0001F325'
        
    if weather_id == 804:# clouds4
        weather_emoji = u'\U00002601'

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
    
    # Randomize some results
    my_verb = random.choice(["jamming to ", "playing ", "rockin' out to ", "blasting ", "singing along with "])
    my_prep = random.choice([" in ", " over in ", " down in ", " up in ", " all over ", " all around "])
    my_explain = random.choice(["(They've obviously got ", "(They must have ", "(It seems they have ", "(They have ", "(It's because of the ", "(It's all because of the "])
    my_end = random.choice([" there.)", ".)" , ". "+ u'\U0001F3B8' +")"])
    
    alt1_begin = random.choice(["If I had so much ", "If I had their "])
    alt1_end = random.choice([", I'd do the same!", ", that's all I'd want to hear, too!"])
    
    alt2_begin = random.choice (["With all that ", "With so much "])
    alt2_end = random.choice([", who could blame them?!", ", you'd do the same!"])
    
    # add an emoji
    weather_description += " "
    weather_description += weather_emoji
    
    # Return the results, both unhelpful and helpful
    # The .split method divides the string at the comma and returns everything before it
    sentence_one = "They're " + my_verb + song_title + my_prep + locale.split(', ', 1)[0] + "!"
    sentence_2one = my_explain + weather_description + my_end
    sentence_2two = alt1_begin + weather_description + alt1_end + weather_emoji + u'\U0001F468\U0000200D\U0001F3A4'
    sentence_2three = alt2_begin + weather_description + weather_emoji + weather_emoji + alt2_end + u'\U0001F3B8'
    sentence_two = random.choice([sentence_2one, sentence_2two, sentence_2three])

    sentence = sentence_one + " " + sentence_two
    sentence_alt = weather_emoji
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

weathertweet = getresponse("Shreveport, Louisiana")
api.update_status(status=weathertweet)
