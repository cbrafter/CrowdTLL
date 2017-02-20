import twitter


def getAPI():
	api = twitter.Api(
        consumer_key        = '',
        consumer_secret     = '',
        access_token_key    = '',
        access_token_secret = ''
        )
	return api
