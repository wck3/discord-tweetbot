import tweepy

API_key = '3PGceEwwxXvRoKWHFfsAc5lEW'
API_secret = 'zmHzO9paAx5eIn1CrHQfS5r7r4VbeFHIIBmoEEhzPcSp1KDUjL'
access_token = '1676998357468733441-2OLRoeZFYSPPifrceqnQE9BhPgo5MX'
access_token_secret = 'P0OX7WV1WmIUQZy8v50ncYmEpHcftUQRPNUbQBpFefv47'

auth = tweepy.OAuthHandler(API_key, API_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Success")
except:
    print("Error Validating Credentials")

