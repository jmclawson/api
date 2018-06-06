import requests, json, random

print("I can tell you what the cool weatherman are listening to anywhere in the world.")

# Start off by asking for input
city = input("What city are you looking for? ")
state = input("And the two-letter code, like for state or province? ")

# First, ready these input items for searching Yahoo's weather API
combined = 'select * from weather.forecast where woeid in (select woeid from geo.places(1) where text="' + city + ', ' + state + '")'

# Set them up as parameters for the query
params = {'q' : combined,
          'format' : 'json',
          'env' : 'store%3A%2F%2Fdatatables.org%2Falltableswithkeys'
     }

# Pass the GET request with the right parameters, then parse the results
weather = requests.get("https://query.yahooapis.com/v1/public/yql", params=params)
weather_parsed = json.loads(weather.text)
weather_condition = weather_parsed['query']['results']['channel']['item']['condition']['text']

# Now that that's done, search Genius for instances of the weather conditions found above 
# The access_token is acquired by registering with the site: https://docs.genius.com
# Enter the 64-character code in quotation marks below, in place of YOURTOKENHERE
params2 = {'q' : weather_condition, 
           'access_token' : YOURTOKENHERE
          }
song = requests.get("http://api.genius.com/search", params=params2)
song_parsed = json.loads(song.text)

# Get the list of songs
song_postparsed = song_parsed['response']['hits']

# Choose one of these songs at random, and then get its title
chosen_song = random.randint(0,(len(song_postparsed)-1))
song_title = song_postparsed[chosen_song]['result']['full_title']

# Return the results, both unhelpful and helpful
sentence = "They're playing " + song_title + " over in " + city + "!"
sentence2 = "(Because it's " + weather_condition + " there, obviously.)"

print(sentence)
print(sentence2)
