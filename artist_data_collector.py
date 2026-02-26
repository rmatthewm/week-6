import os
from apputil import Genius
from dotenv import load_dotenv

# Get the access token from the environment variables
load_dotenv()
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')

def main():
    # Create a Genius object to get the data
    genius = Genius(ACCESS_TOKEN)

    # Load in the list of artists
    with open('artist_search_terms.txt', 'r') as file:
        artist_search_terms = file.read().strip().split('\n')

    # Get the artist data and save it to a csv file
    artist_data = genius.get_artists(artist_search_terms)
    artist_data.to_csv('artist_data.csv', index=False)


if __name__ == "__main__":
    main()