import oauth2
import constants
import constants
import urllib.parse as urlparse
# creating a consumer using CONSUMER_KEY and CONSUMER_SECRET to recognize our application.
consumer = oauth2.Consumer(constants.CONSUMER_KEY, constants.CONSUMER_SECRET)


def getRequestToken():
    client = oauth2.Client(consumer)
    # using a client to perform for a request token.
    response, content = client.request(constants.REQUEST_TOKEN_URL, 'POST')
    # check if there's any error getting the request token.
    if response.status != 200:
        print("An error occurred getting request token from Twitter!!!")
    return dict(urlparse.parse_qsl(content.decode('utf-8')))

def getOauthVerifier(request_token):
    # asking the user to authorize our app and provide the pin code.
    print("PLease go to the following website in your browser: ")
    print(getOauthVerifierUrl(request_token))
    return input("Please enter the pin: ")

def getOauthVerifierUrl(request_token):
    return "{}?oauth_token={}".format(constants.AUTHORIZATION_URL, request_token['oauth_token'])

def getAccessToken(request_token, oauth_verifier):
    # creating a token object that consists of request token and the oauth_code
    token = oauth2.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
    token.set_verifier(oauth_verifier)
    # creating a client with our consumer (our app) and the newly created (and verified) token
    client = oauth2.Client(consumer, token)
    # asking Twitter for an access token, we alredy verified the request token
    response, content = client.request(constants.ACCESS_TOKEN_URL, 'POST')
    return dict(urlparse.parse_qsl(content.decode('utf-8')))