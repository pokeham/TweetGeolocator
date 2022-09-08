
import sys
sys.path.insert(0,'./modulesForOAuth')
import requests
from requests_oauthlib import OAuth1
import json
from urllib.parse import quote_plus

API_KEY = "9vY0KOmjJ3TgL7pC9q3ZWjQK4"
API_SECRET = "1l5tKK5h7uZFhlAQDUOv2IpAJjCO3kOocOkP8EqD0TVkAnMtWP"
ACCESS_TOKEN = "1470173353524834310-XrV2d5oap5jFNZFGjDO0FSAnIAciKw"
ACCESS_TOKEN_SECRET = "lOAtuX8oz74yLEyUDG0wsG70hxoTFMVcIquy5trrIzcwH"

def authTwitter():
    global client
    client = OAuth1(API_KEY, API_SECRET,
                    ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

def searchTwitter(searchString, count = 20, radius = 2, latlngcenter = None):    
    query = "https://api.twitter.com/1.1/search/tweets.json?q=" + quote_plus(searchString) + "&count=" + str(count)

    if latlngcenter != None:
        query = query + "&geocode=" + str(latlngcenter[0]) + "," + str(latlngcenter[1]) + "," + str(radius) + "km"
    global response
    response = requests.get(query, auth=client)
    resultDict = json.loads(response.text)
       tweets = resultDict['statuses']
    tweetsWithGeoCount = 0 
    for tweetIndex in range(len(tweets)):
        tweet = tweets[tweetIndex]
        if tweet['coordinates'] != None:
            tweetsWithGeoCount += 1
            print("Tweet {} has geo coordinates.".format(tweetIndex))           
    return tweets

def printable(s):
    result = ''
    for c in s:
        result = result + (c if c <= '\uffff' else '?')
    return result

def whoIsFollowedBy(screenName):
    global response
    global resultDict
    
    query = "https://api.twitter.com/1.1/friends/list.json?&count=50"
    query = query + "&screen_name={}".format(screenName)
    response = requests.get(query, auth=client)
    resultDict = json.loads(response.text)
    for person in resultDict['users']:
        print(person['screen_name'])
    
def getMyRecentTweets():
    global response
    global data
    global statusList 
    query = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    response = requests.get(query,auth=client)
    statusList = json.loads(response.text)
    for tweet in statusList:
        print(printable(tweet['text']))
        print()

