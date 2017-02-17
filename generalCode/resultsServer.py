import twitAuth
import updateResults
import time

api = twitAuth.getAPI()

# Generate default leaderboard and open webpage
updateResults.parseTweets(api)
updateResults.openHTML_Browser('results.html')

while True:
    updateResults.parseTweets(api)
    time.sleep(30)
