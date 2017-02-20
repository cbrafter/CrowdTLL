# -*- coding: utf-8 -*-
"""
@file    CrowdTLL.py
@author  Craig Rafter
@date    01/02/17

Code to run and display results from the twitter feed
"""
import twitAuth
import updateResults
import time

api = twitAuth.getAPI()

# Generate default leaderboard and open webpage
updateResults.parseTweets(api)
updateResults.openHTML_Browser('./data/results.html')

while True:
    updateResults.parseTweets(api)
    time.sleep(30)
