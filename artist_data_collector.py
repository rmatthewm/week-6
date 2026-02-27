import os
from dotenv import load_dotenv
from joblib import Parallel, delayed
from apputil import Genius

# Get the access token from the environment variables
load_dotenv()
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')

def main():
    # Create a Genius object to get the data
    genius = Genius(ACCESS_TOKEN)

    # Load in the list of artists
    with open('artist_search_terms.txt', 'r') as file:
        artist_search_terms = file.read().strip().split('\n')

    # Find how many available CPU threads we have
    thread_count = os.cpu_count()

    # Since we will almost certainly have fewer cores than artists, we will
    # assign a batch of artists to each thread
    batch_size = len(artist_search_terms) // thread_count

    # Get the data for each artist in parallel
    # artist_data_para = Parallel(n_jobs=thread_count)(
    #     # For the last thread, include all that's left to avoid missing
    #     # artists or exceeding the list length
    #     delayed(genius.get_artists)(artist_search_terms[batch_size*i:]) 
    #         if i == thread_count - 1 else delayed(genius.get_artists)
    #         (artist_search_terms[i*batch_size:(i+1)*batch_size])
    #         for i in range(thread_count)
    # )

    artist_data_para = genius.get_artists(artist_search_terms[0:10])

    print(artist_data_para)

    #artist_data.to_csv('artist_data.csv', index=False)


if __name__ == "__main__":
    main()