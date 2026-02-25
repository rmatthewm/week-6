import os
from dotenv import load_dotenv
import requests

load_dotenv()
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')


# Exercise 1
class Genius:
    def __init__(self, access_token):
        # store the token so other methods can use it
        self.access_token = access_token

    # Exercise 2
    def get_artist(self, search_term):
