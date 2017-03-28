from flask import Flask, render_template, session, redirect, request, url_for, g
from twitter_utils import *
from user import User
from database import Database

Database.initialize(host='localhost', database='learning', user='postgres', password='Mukhtar1')
app = Flask(__name__)
app.secret_key = '1234'

@app.before_request
def get_user():
    if 'screen_name' in session:
        g.user = User.loadFromDbByScreenName(session['screen_name'])

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/login/twitter')
def twitter_login():
    if 'screen_name' in session:
        return redirect(url_for('profile'))
    request_token = getRequestToken()
    session['request_token'] = request_token

    return redirect(getOauthVerifierUrl(request_token))

@app.route('/logout')
def logout():
    session.clear()
    redirect(url_for(homepage))

@app.route('/auth/twitter')
def twitter_authentication():
    oauth_verifier = request.args.get('oauth_verifier')
    access_token = getAccessToken(session['request_token'], oauth_verifier)
    user = User.loadFromDbByScreenName(access_token['screen_name'])
    if not user:
        user = User(access_token['screen_name'], access_token['oauth_token'], access_token['oauth_token_secret'], None)
        user.SaveToDB()

    session['screen_name'] = user.screen_name

    return redirect(url_for('profile'))

@app.route('/profile')
def profile():
    return render_template('profile.html', user= g.user)

@app.route('/search')
def search():
    query_string = request.args.get('q')
    tweets = g.user.performTwitterRequest('https://api.twitter.com/1.1/search/tweets.json?q={}'.format(query_string))
    tweet_texts = [tweet['text'] for tweet in tweets['statuses']]
    return render_template('search.html', content=tweet_texts, user = g.user)

app.run(port=4995, debug=True)