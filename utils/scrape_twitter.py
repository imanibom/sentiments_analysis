# utils/scrape_twitter.py
import os
import requests
from datetime import datetime, date, timedelta
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')

def create_headers():
    """
    Creates the necessary headers for Twitter API requests.
    Raises an error if the BEARER_TOKEN is not set.
    """
    if not BEARER_TOKEN:
        logging.error("TWITTER_BEARER_TOKEN environment variable not set.")
        raise ValueError("TWITTER_BEARER_TOKEN is not set. Please set it in your .env file.")
    return {
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }

def get_twitter_data(query="Umo Eno", max_results=10):
    """
    Fetches recent tweets from the Twitter API based on a query.
    Includes fallback dummy data if the real API call fails or token is missing.
    Ensures 'date' field is a datetime.date object.

    Args:
        query (str): The search query for tweets.
        max_results (int): The maximum number of tweets to retrieve (up to 100 for recent search).

    Returns:
        list: A list of dictionaries, where each dictionary represents a tweet
              with 'source', 'title', 'text', and 'date' fields.
    """
    if not (1 <= max_results <= 100):
        logging.warning(f"max_results should be between 1 and 100. Using default of 10 instead of {max_results}.")
        max_results = 10

    search_url = "https://api.twitter.com/2/tweets/search/recent"
    
    # --- Attempt to fetch real Twitter data ---
    try:
        headers = create_headers() # This will raise ValueError if token is missing
        
        params = {
            'query': query,
            'max_results': max_results,
            'tweet.fields': 'created_at,text',
            'expansions': 'author_id',
            'user.fields': 'username,name'
        }

        logging.info(f"Attempting to fetch Twitter data for query: '{query}'")
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        
        tweets_data = response.json()
        tweets = tweets_data.get("data", [])

        processed_tweets = []
        if tweets:
            for tweet in tweets:
                try:
                    # Ensure it's a date object
                    tweet_date = datetime.strptime(tweet['created_at'], "%Y-%m-%dT%H:%M:%S.000Z").date()
                    processed_tweets.append({
                        'source': 'Twitter',
                        'title': 'Tweet',
                        'text': tweet['text'],
                        'date': tweet_date
                    })
                except KeyError as e:
                    logging.error(f"Missing expected key in tweet data: {e} in tweet: {tweet}")
                except ValueError as e:
                    logging.error(f"Error parsing date for tweet: {tweet.get('created_at', 'N/A')}. Error: {e}")
            logging.info(f"Successfully fetched {len(processed_tweets)} tweets for '{query}'.")
            return processed_tweets # Return real data if successful
        else:
            logging.warning(f"No real tweets found for query '{query}'.")

    except (ValueError, requests.exceptions.RequestException, Exception) as e:
        logging.error(f"Failed to fetch real Twitter data for '{query}': {e}")
        # Continue to dummy data fallback

    # --- Fallback to dummy data if real fetch fails or token is missing ---
    logging.info(f"Falling back to dummy Twitter data for testing query '{query}'.")
    today = date.today()
    dummy_tweets = [
        {
            'source': 'Twitter',
            'title': 'Tweet',
            'text': f"Great work by Governor Umo Eno on the new road infrastructure in Akwa Ibom! #UmoEno #AkwaIbom",
            'date': today - timedelta(days=1) # Already a date object
        },
        {
            'source': 'Twitter',
            'title': 'Tweet',
            'text': f"Concerned about the recent increase in prices. Hope Governor Eno's policies address this. #Nigeria #Economy",
            'date': today - timedelta(days=3) # Already a date object
        },
        {
            'source': 'Twitter',
            'title': 'Tweet',
            'text': f"Attended a youth summit today where Governor Eno spoke. Very inspiring! #YouthEmpowerment #AkwaIbom",
            'date': today - timedelta(days=2) # Already a date object
        },
        {
            'source': 'Twitter',
            'title': 'Tweet',
            'text': f"Just flew into Uyo. The airport looks fantastic! Progress is visible thanks to government efforts. #Uyo #Development",
            'date': today - timedelta(days=5) # Already a date object
        },
        {
            'source': 'Twitter',
            'title': 'Tweet',
            'text': f"A balanced perspective needed on the current state of affairs in Akwa Ibom. Things are complex. #Politics #AkwaIbom",
            'date': today - timedelta(days=4) # Already a date object
        },
    ]
    return dummy_tweets

# Example usage (for testing, can be removed in production)
if __name__ == "__main__":
    print("Fetching tweets for 'Umo Eno' (testing real and dummy fallback)...")
    umo_eno_tweets = get_twitter_data(query="Umo Eno", max_results=5)
    for tweet in umo_eno_tweets:
        print(f"Date: {tweet['date']}, Text: {tweet['text'][:100]}...")
    
    print("\nFetching tweets for 'Akwa Ibom' with more results (testing real and dummy fallback)...")
    akwa_ibom_tweets = get_twitter_data(query="Akwa Ibom", max_results=20)
    for tweet in akwa_ibom_tweets:
        print(f"Date: {tweet['date']}, Text: {tweet['text'][:100]}...")

    print("\nAttempting to fetch with an invalid max_results (should default to 10 and use dummy if token missing)...")
    invalid_results_tweets = get_twitter_data(query="Nigeria", max_results=150)
    print(f"Number of tweets fetched: {len(invalid_results_tweets)}")
