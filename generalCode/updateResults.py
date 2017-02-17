import pandas as pd
import os
from shutil import copyfile
from htmlTable import htmlTable
import time
import profanity.profanity as profanity
import webbrowser
with open('badWordsShort.txt', 'r') as f:
    badWords = [x.strip() for x in f.readlines()]
    # profanity.load_words(badWords)


def openHTML_Browser(filename):
    path = os.path.abspath(filename)
    url = 'file://' + path
    webbrowser.open(url)


def updateResults(filename, initial, timeScore):
    hdfFile = './data/'+filename+'.hdf'
    if not os.path.exists(hdfFile):
        copyfile('./data/default.hdf', hdfFile)
    data = pd.read_hdf(hdfFile)
    # add new entry to data frame
    data.loc[len(data)] = [initial, timeScore]
    # rank user scores
    sortData = data.groupby(['INITIALS']).min()
    # save new data
    sortData.to_hdf(hdfFile, 'test', mode='w')

    htmlTable(sortData, filename+'.html')


def tweetInfo(api, initial, timeScore):
    status = '{} cleared the junction in {}s!'
    if len(initial) == 0:
        name = 'NONE'
        api.PostUpdate(status.format(name, timeScore))

    # limit iniital to 4 chars and remove symbols
    name = initial[:4].lower()  # Use only 4 letter max words
    name = ''.join([c for c in name if c.isalnum()])

    # All chars were symbols
    if len(name) == 0:
        initial = 'NONE'
        api.PostUpdate(status.format(name, timeScore))

    findMap = ['1', '3', '4', '7', '8', '9', '5', '0', '2']
    replMap = ['i', 'e', 'a', 'l', 'b', 'g', 's', 'o', 'r']
    for i, j in zip(findMap, replMap):
        name.replace(i, j)

    # profanity filter
    if profanity.contains_profanity(name):
        name = initial[:4].upper()
        name = name[0] + '***'
    else:
        name = initial[:4].upper()

    # Post result to twitter
    api.PostUpdate(status.format(name, timeScore))


def secondsSinceTweet(tweet):
    return time.time() - tweet.created_at_in_seconds


def parseTweets(api):
    userName = api.VerifyCredentials().screen_name
    timeline = api.GetUserTimeline(screen_name=userName, count=110)
    results = {'UID': ['COMP', 'JIM', 'UOS'], 'TIME': [175.12, 250.0, 300.0]}
    oneHourInSeconds = 3600
    validTweets = []

    # Get only tweets from the last hour or if the number of tweets is over 100
    for tweet in timeline:
        if (secondsSinceTweet(tweet) < oneHourInSeconds and
           len(validTweets) < 100):
            # Get only tweets from own account and if the message matches the
            # result string format
            if (tweet.user.screen_name == userName and
               'cleared the junction in' in tweet.text):
                validTweets.append(tweet)
        else:
            break

    # Parse the name and time from tweets
    for tweet in validTweets:
        splitMsg = tweet.text.split()
        clearIndex = splitMsg.index('cleared')
        # clearIndex = max(1, clearIndex) # if user puts name as cleared
        name = str(''.join(splitMsg[0:clearIndex]))
        timeScore = float(splitMsg[clearIndex+4][:-2])
        results['UID'].append(name)
        results['TIME'].append(timeScore)

    # Pandas Stuff
    df = pd.from_dict(results)
    dfSort = df.groupby(['INITIALS']).min()
    htmlTable(dfSort, 'results.html')
