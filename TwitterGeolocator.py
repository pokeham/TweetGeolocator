from tkinter import Tk, Canvas, Frame, Button, Label, Entry, END, LEFT, BOTTOM, TOP, RIGHT, SUNKEN
import tkinter
import math
import ssl
from urllib.request import urlopen, urlretrieve
from urllib.parse import urlencode, quote_plus
import json
import webbrowser
import string
from twitteraccess import authTwitter
from twitteraccess import searchTwitter
from twitteraccess import printable
from twitteraccess import whoIsFollowedBy
from twitteraccess import getMyRecentTweets
import webbrowser

GOOGLEAPIKEY = "AIzaSyCZb8qnDG7h1GczokFCYwRTj3UNHoGo5X8"

class Globals:
   numTweets = None
   tweetURL = None
   currentTweetIndex = 0
   tweets_latlonlist = []
   rootWindow = None
   mapLabel = None
   locationEntry = None
   tweetEntry = None
   mapType = 'roadmap'
   defaultLocation = "Mt. Fuji, Japan"
   mapLocation = defaultLocation
   tweets = []
   tweetText = None
   tweetName = None
   tweetScreen_Name = None
   mapFileName = 'googlemap.gif'
   mapSize = 400
   zoomLevel = 9

def createMarkerString(currentTweetIndex, tweetLatLonList, mapCenterLatLon):
    tmp="&markers=color:red|";
    if len(tweetLatLonList) == 0:
       return
    if tweetLatLonList[currentTweetIndex]!=None:
        tmp+=str(tweetLatLonList[currentTweetIndex][0])+","+str(tweetLatLonList[currentTweetIndex][1]);
    else:
        tmp+=str(mapCenterLatLon[0])+","+str(mapCenterLatLon[1])
    tmp+="&markers=color:yellow|size:small";
    for i in tweetLatLonList:
        if i != None and i!=currentTweetIndex:
            tmp+="|"+str(i[0])+","+str(i[1])
    
    return tmp;

def geocodeAddress(addressString):
   urlbase = "https://maps.googleapis.com/maps/api/geocode/json?address="
   geoURL = urlbase + quote_plus(addressString)
   geoURL = geoURL + "&key=" + GOOGLEAPIKEY
   ctx = ssl.create_default_context()
   ctx.check_hostname = False
   ctx.verify_mode = ssl.CERT_NONE
   stringResultFromGoogle = urlopen(geoURL, context=ctx).read().decode('utf8')
   jsonResult = json.loads(stringResultFromGoogle)
   if (jsonResult['status'] != "OK"):
      print("Status returned from Google geocoder *not* OK: {}".format(jsonResult['status']))
      result = (0.0, 0.0) 
   else:
      loc = jsonResult['results'][0]['geometry']['location']
      result = (float(loc['lat']),float(loc['lng']))
   return result

def getMapUrl():
   lat, lng = geocodeAddress(Globals.mapLocation)
   urlbase = "http://maps.google.com/maps/api/staticmap?"
   args = "center={},{}&zoom={}&size={}x{}&maptype={}{}&sensor=false&format=gif".format(lat, lng, Globals.zoomLevel, Globals.mapSize,Globals.mapSize,Globals.mapType,createMarkerString(Globals.currentTweetIndex, Globals.tweets_latlonlist, [lat,lng]))
   args = args + "&key=" + GOOGLEAPIKEY
   mapURL = urlbase + args
   return mapURL

def retrieveMapFromGoogle():
   url = getMapUrl()
   urlretrieve(url, Globals.mapFileName)

def displayMap():
   retrieveMapFromGoogle()    
   mapImage = tkinter.PhotoImage(file=Globals.mapFileName)
   Globals.mapLabel.configure(image=mapImage)
   Globals.mapLabel.mapImage = mapImage
   
def readEntryAndDisplayMap():
   locationString = Globals.locationEntry.get()
   tweetstring = Globals.tweetEntry.get()
   latlng = []
   Globals.mapLocation = locationString
   latlng =(geocodeAddress(Globals.mapLocation))
   tweets = searchTwitter(tweetstring,latlngcenter =[latlng[0],latlng[1]],radius = 1)
   print(len(tweets))
   extractTwitter(tweets)
   displayTweet(Globals.currentTweetIndex)
   displayMap()

def extractTwitter(tweetInfo):
   Globals.currentTweetIndex = 0
   tweet_size = len(tweetInfo)
   Globals.tweets = []
   Globals.tweets_latlonlist = []
   for x in range(tweet_size):
      (Globals.tweets_latlonlist).append([(tweetInfo[x]['geo']['coordinates'][0]),(tweetInfo[x]['geo']['coordinates'][1])])
      (Globals.tweets).append([(tweetInfo[x]['user']['name']),(tweetInfo[x]['user']['screen_name']),(tweetInfo[x]['text']),(tweetInfo[x]['geo']['coordinates']),(tweetInfo[x]['entities']['urls'][0]['url'])])
   
def displayTweet(currentTweetIndex):
   if(len(Globals.tweets) == 0):
      return
      
   Globals.tweetText.configure(state='normal')
   Globals.tweetText.delete(1.0,'end')
   (Globals.tweetText).insert(1.0,(Globals.tweets)[Globals.currentTweetIndex][2])
   Globals.tweetText.configure(state='disabled')
   (Globals.tweetText).pack()

   (Globals.tweetName).configure(text = "")
   (Globals.tweetName).configure(text =( Globals.tweets)[Globals.currentTweetIndex][0])
   Globals.tweetName.pack()


   (Globals.tweetScreen_Name).configure(text = "")
   (Globals.tweetScreen_Name).configure(text =( Globals.tweets)[Globals.currentTweetIndex][1])
   Globals.tweetScreen_Name.pack()

   (Globals.tweetURL).configure(text =(Globals.tweets)[Globals.currentTweetIndex][4])
   Globals.tweetURL.pack()

   Globals.numTweets.configure(text = str(len(Globals.tweets)))
   Globals.numTweets.pack()
   
   
          
def ZoomIn():
   Globals.zoomLevel += 1
   displayMap()
   
def ZoomOut():
    Globals.zoomLevel -= 1
    displayMap()
    
def radioButtonChosen():
    global selectedButtonText
    global choiceVar
    global label

    if choiceVar.get() == 1:
        selectedButtonText = "roadmap"
        Globals.mapType = "roadmap"
    elif choiceVar.get() == 2:
        selectedButtonText = "satellite"
        Globals.mapType = "satellite"
    elif choiceVar.get() == 3:
        selectedButtonText = "terrain"
        Globals.mapType = "terrain"
    else:
        selectedButtonText = "hybrid"
        Globals.mapType = "hybrid"
    displayMap()
    label.configure(text="Radio button choice is: {}".format(selectedButtonText))
def PrevTweet():
   if Globals.currentTweetIndex == 0:
      Globals.currentTweetIndex = len(Globals.tweets)-1
      displayTweet(Globals.currentTweetIndex)
      displayMap()
   else:
      Globals.currentTweetIndex = Globals.currentTweetIndex -1
      displayTweet(Globals.currentTweetIndex)
      displayMap()
      
def NextTweet():
   if Globals.currentTweetIndex == len(Globals.tweets)-1:
      Globals.currentTweetIndex = 0
      displayTweet(Globals.currentTweetIndex)
      displayMap()
   else:
      Globals.currentTweetIndex = Globals.currentTweetIndex +1
      displayTweet(Globals.currentTweetIndex)
      displayMap()
def OpenURL():
   if(len(Globals.tweets) == 0):
      return
   else:
      webbrowser.open((Globals.tweets)[Globals.currentTweetIndex][4])
      

     
def initializeGUIetc():

   global selectedButtonText
   global choiceVar
   global label

   Globals.rootWindow = tkinter.Tk()
   Globals.rootWindow.title("HW11")

   locationLabelFrame = tkinter.Frame(Globals.rootWindow)
   locationLabel = Label(locationLabelFrame, text="Enter the location and Search Term:")
   locationLabelFrame.pack()
   locationLabel.pack()

   

   Globals.locationEntry = tkinter.Entry()
   Globals.locationEntry.pack()

   Globals.tweetEntry = tkinter.Entry()
   Globals.tweetEntry.pack()

   mainFrame = tkinter.Frame(Globals.rootWindow)
   mainFrame.pack()

   readEntryAndDisplayMapButton = tkinter.Button(mainFrame, text="Search Twitter and Display map", command=readEntryAndDisplayMap)
   readEntryAndDisplayMapButton.pack()

   
   
   selectedButtonText = ""

   label = tkinter.Label(mainFrame, text="Map Type is: {}".format(selectedButtonText))
   label.pack()
   
   choiceVar = tkinter.IntVar()
   choiceVar.set(1)
   choice1 = tkinter.Radiobutton(mainFrame, text="road Map", variable=choiceVar, value=1,command=radioButtonChosen)
   choice1.pack()
   choice2 = tkinter.Radiobutton(mainFrame, text="satellite Map", variable=choiceVar, value=2, command=radioButtonChosen)
   choice2.pack()
   choice3 = tkinter.Radiobutton(mainFrame,text="terrain Map", variable=choiceVar,value=3,command=radioButtonChosen)
   choice3.pack()
   choice4 = tkinter.Radiobutton(mainFrame,text="hybrid Map", variable=choiceVar,value=4,command=radioButtonChosen)
   choice4.pack()

   labelZoom = tkinter.Label(mainFrame,text = "Zoom In or Out!")
   labelZoom.pack()
   

   ZoomInButton = tkinter.Button(mainFrame,text="+", command=ZoomIn)
   
   ZoomInButton.pack()

   ZoomOutButton = tkinter.Button(mainFrame,text="-",command=ZoomOut)
   ZoomOutButton.pack()


   tweetNameHeader = tkinter.Label(mainFrame,text = "Name:")
   tweetNameHeader.pack()
   Globals.tweetName = tkinter.Label(mainFrame,text = "NA")
   Globals.tweetName.pack()

   tweetScreen_NameHeader = tkinter.Label(mainFrame,text = "Screen_Name:")
   tweetScreen_NameHeader.pack()
   Globals.tweetScreen_Name = tkinter.Label(mainFrame,text = "NA")
   Globals.tweetScreen_Name.pack()
   
                                   
   tweetTextHeader = tkinter.Label(mainFrame,text = "Tweet Text:")
   tweetTextHeader.pack()
   Globals.tweetText = tkinter.Text(mainFrame,width = 70,height = 4)
   Globals.tweetText.configure(state='disabled')
   Globals.tweetText.pack()
   
   tweetURLHeader = tkinter.Label(mainFrame,text = "Tweet URL:")
   tweetURLHeader.pack()
   Globals.tweetURL = tkinter.Label(mainFrame,text = "NA")
   Globals.tweetURL.pack()
   tweetURLbutton = tkinter.Button(mainFrame,text = "Open URL!", command=OpenURL)
   tweetURLbutton.pack()
   numTweetsHeader = tkinter.Label(mainFrame,text = "Number of Tweets:")
   numTweetsHeader.pack()
   Globals.numTweets = tkinter.Label(mainFrame, text = "")
   Globals.numTweets.pack()
   
   NextTweetButton = tkinter.Button(mainFrame,text="Next Tweet", command=NextTweet)
   NextTweetButton.pack(side = 'right',fill='y')
   PrevTweetButton = tkinter.Button(mainFrame,text="Previous Tweet", command=PrevTweet)
   PrevTweetButton.pack(side = 'left',fill='y')
   
   Globals.mapLabel = tkinter.Label(mainFrame, width=Globals.mapSize, bd=2, relief=tkinter.FLAT)
   Globals.mapLabel.pack()

def Main():
   authTwitter()
   initializeGUIetc()
   displayMap()
   Globals.rootWindow.mainloop()
