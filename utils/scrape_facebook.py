# utils/scrape_facebook.py
import os
import requests
from datetime import datetime, date, timedelta
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- IMPORTANT NOTE ON FACEBOOK SCRAPING ---
# This implementation is a PLACEHOLDER demonstrating structure and WILL ALWAYS
# RETURN DUMMY DATA for demonstration purposes due to the difficulty of real access.
# -------------------------------------------

FACEBOOK_ACCESS_TOKEN = os.getenv('FACEBOOK_ACCESS_TOKEN')

def create_headers():
    if not FACEBOOK_ACCESS_TOKEN:
        logging.warning("FACEBOOK_ACCESS_TOKEN environment variable not set. Using dummy data for Facebook.")
    return {
        "Authorization": f"Bearer {FACEBOOK_ACCESS_TOKEN if FACEBOOK_ACCESS_TOKEN else 'DUMMY_TOKEN'}",
        "Content-Type": "application/json"
    }

def get_facebook_data(query="Akwa Ibom State", max_results=5):
    """
    Simulates fetching data from Facebook, always returning dummy data for demonstration.
    Ensures 'date' field is a datetime.date object.

    Args:
        query (str): A simulated search query.
        max_results (int): Simulated maximum number of results.

    Returns:
        list: A list of dictionaries, where each dictionary represents a Facebook post.
    """
    logging.info("Returning DUMMY Facebook data for demonstration.")

    today = date.today()
    dummy_posts = []
    base_messages = [
        f"Governor Umo Eno’s speech at the townhall in {query} was inspiring!",
        f"Akwa Ibom State is seeing rapid development under the current administration.",
        f"Community efforts are key to sustainable growth in {query}."
    ]
    for i in range(max_results):
        post_date = today - timedelta(days=i) # Already a date object
        message = base_messages[i % len(base_messages)]
        dummy_posts.append({
            'id': f'fb_post_{i+1}',
            'message': f"FB Post {i+1}: {message}",
            'created_time': post_date.isoformat(), # Store as ISO format string
        })

    processed_data = []
    for post in dummy_posts:
        try:
            # Parse back to date object to ensure consistency, even though it started as one
            post_date = datetime.fromisoformat(post['created_time']).date()
            processed_data.append({
                'source': 'Facebook',
                'title': 'Facebook Post',
                'text': post.get('message', 'No message available'),
                'date': post_date # This will be a datetime.date object
            })
        except Exception as e:
            logging.error(f"Error processing dummy Facebook post data: {e} in post: {post}")

    return processed_data

# Example usage (for testing)
if __name__ == "__main__":
    print("Fetching dummy Facebook data for 'Akwa Ibom State'...")
    fb_data = get_facebook_data(query="Akwa Ibom State", max_results=3)
    for item in fb_data:
        print(f"Source: {item['source']}, Date: {item['date']}, Text: {item['text'][:80]}...")

    print("\nFetching more dummy Facebook data for 'Nigeria'...")
    fb_data_2 = get_facebook_data(query="Nigeria", max_results=7)
    for item in fb_data_2:
        print(f"Source: {item['source']}, Date: {item['date']}, Text: {item['text'][:80]}...")
