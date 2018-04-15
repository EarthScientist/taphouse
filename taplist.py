# # # 
# parse taplist at lavelles taphouse in fairbanks, ak and even listen to their twitter feed for 
# beer updates! 
# this is just a fun little app that does very little at the moment, but is fun to mess around with.
# # # 

def parse_page( url, parser='html.parser' ):
    page = requests.get( url )
    return BeautifulSoup(page.text, parser)

def get_tap_info( tab ):
    tapNum = tab.find('div',class_='tapName').text
    idx, = [count for count,i in enumerate(tab.find_all('div', class_='producerName')) if i.text is not '' ]
    bevinfo = tab.find_all('div',class_='beverageInfo')[idx]
    tapDat = [ (i['class'][0],i.text) for i in bevinfo if i != '\n' ]
    tapDat.append( ('tapNum',tapNum) )
    return dict(tapDat)

def get_current_taplist( ):
    ## this was found by poking around on their lavellestaphouse.com website and found a way to
    # actually pull their resource for current taplist.  This will be MUCH easier to deal with 
    # than the whole Twitter thing.  
    url = 'http://fbpage.digitalpour.com/?companyID=5667586f5e002c0a5450d437&locationID=1'

    # use our parser function to parse the soup
    page = parse_page( url )

    # Try to sniff around for the tapinfo
    # --> the list elements on this page are the 36 taps XML data... its bulky xml.
    taps = page.find_all( 'li' )

    # get the current taplist...
    return pd.DataFrame([ get_tap_info(tap) for tap in taps ])

from tweepy import StreamListener
class StdOutListener( StreamListener ):

    def on_data(self, data):
        # process stream data here
        print( data )
        print( '---' )
        print( self.format_tweet_info( data ) )
        # make a table with the new data and the current taplist. and show what is new.
        # or maybe get and store the taplists for a month
        

    def on_error(self, status):
        print('error: {}'.format(status))
        # print(status)

    @staticmethod
    def format_tweet_info( t ):
        out = list(zip(['on','off'],t.text.split( '  is on, replacing ' )))
        out.append( ('time',datetime.date.fromtimestamp(t.created_at_in_seconds)))
        return dict(out)

def listen_to_lavellestaps():
    ''' 
    listen to @lavellestaps twitter feed for any new tweets

    the class above will do much of the handling work. 

    see: https://stackoverflow.com/questions/28709826/tweepy-streaming-api-filtering-on-user
    '''
    CONSUMER_KEY = 'lkemsVN12R0aJDELs6csmA'
    CONSUMER_SECRET = 'vEFFtvXYCC0mOHVikmcun4QHKeeKJ8akFgywINebNI'
    ACCESS_KEY = '981753320-t3T6oLmKKjyTYUzv40ddcSI5stw4kKHnI0ebPfE5'
    ACCESS_SECRET = 'MeBdGth7LFs6GmSOPWOGgKgYl0JDGsNqI4mfuVSlZU'

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)

    # listen
    listener = StdOutListener()
    twitterStream = Stream(auth, listener)
    twitterStream.filter(follow=['2445679704']) # this is @lavellestaps user_id

if __name__ == '__main__':
    import requests
    from bs4 import BeautifulSoup
    from tweepy import Stream
    import tweepy
    import pandas as pd
    import numpy as np

    # get the taplist
    current_taplist = get_current_taplist()

    # listen for changes on twitter
    listen_to_lavellestaps()