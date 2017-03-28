from user import User
from database import Database
from twitter_utils import *


Database.initialize(user='postgres', password ='Mukhtar1', host='localhost', database='learning')

screen_name = input('Please enter your email:')

# returns true if user is found on the database with the provided email address, returns false otherwise
user = User.loadFromDbByScreenName(screen_name)

# if not found, takes the user to authorize and later puts necessary credentials into the database
if not user:
    request_token = getRequestToken()
    oauth_verifier = getOauthVerifier(request_token)
    access_token = getAccessToken(request_token, oauth_verifier)

    first_name = input("Your First name : ")
    last_name = input("And your Last name : ")
    user = User(screen_name, access_token['oauth_token'], access_token['oauth_token_secret'], None)
    user.SaveToDB()

# now, creating an authenticated token object so as to perform Twitter API calls.
authorized_token = oauth2.Token(user.oauth_token, user.oauth_token_secret)
authorized_client = oauth2.Client(consumer, authorized_token)
