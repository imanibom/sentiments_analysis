# utils/scrape_instagram.py
import os
import requests
from datetime import datetime, date, timedelta
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- IMPORTANT NOTE ON INSTAGRAM SCRAPING ---
# This implementation is a PLACEHOLDER demonstrating structure and WILL ALWAYS
# RETURN DUMMY DATA for demonstration purposes due to the difficulty of real access.
# -------------------------------------------

INSTAGRAM_ACCESS_TOKEN = os.getenv('INSTAGRAM_ACCESS_TOKEN')

def create_headers():
    if not INSTAGRAM_ACCESS_TOKEN:
        logging.warning("INSTAGRAM_ACCESS_TOKEN environment variable not set. Using dummy data for Instagram.")
    return {
        "Authorization": f"Bearer {INSTAGRAM_ACCESS_TOKEN if INSTAGRAM_ACCESS_TOKEN else 'DUMMY_TOKEN'}",
        "Content-Type": "application/json"
    }

def get_instagram_data(query="Umo Eno", max_results=5):
    """
    Simulates fetching data from Instagram, always returning dummy data for demonstration.
    Ensures 'date' field is a datetime.date object.

    Args:
        query (str): A simulated search query.
        max_results (int): Simulated maximum number of results.

    Returns:
        list: A list of dictionaries, where each dictionary represents an Instagram media item.
    """
    logging.info("Returning DUMMY Instagram data for demonstration.")

    today = date.today()
    dummy_media = []
    base_captions = [
        f"People in Akwa Ibom love Umo Eno’s grassroots development efforts! #CommunityImpact #AkwaIbom",
        f"Highlights from the recent youth engagement in Uyo. Inspiring future leaders!",
        f"Exploring the beauty of Akwa Ibom State. So much potential here!",
        f"Supporting local businesses, a key part of our economic agenda."
    ]
    for i in range(max_results):
        media_date = today - timedelta(days=i) # Already a date object
        caption = base_captions[i % len(base_captions)]
        dummy_media.append({
            'id': f'ig_media_{i+1}',
            'caption': f"IG Post {i+1}: {caption}",
            'timestamp': media_date.isoformat(), # Store as ISO format string
            'media_type': 'IMAGE',
            'media_url': 'https://placehold.co/150x150/000000/FFFFFF?text=IG+Media'
        })

    processed_data = []
    for media_item in dummy_media:
        try:
            # Parse back to date object to ensure consistency
            media_date = datetime.fromisoformat(media_item['timestamp']).date()

            processed_data.append({
                'source': 'Instagram',
                'title': f"IG {media_item.get('media_type', 'Media')}",
                'text': media_item.get('caption', 'No caption available'),
                'date': media_date # This will be a datetime.date object
            })
        except Exception as e:
            logging.error(f"Error processing dummy Instagram media data: {e} in media: {media_item}")

    return processed_data

# Example usage (for testing)
if __name__ == "__main__":
    print("Fetching dummy Instagram data for 'Umo Eno'...")
    ig_data = get_instagram_data(query="Umo Eno", max_results=3)
    for item in ig_data:
        print(f"Source: {item['source']}, Date: {item['date']}, Text: {item['text'][:80]}...")

    print("\nFetching more dummy Instagram data for 'Nigeria tourism'...")
    ig_data_2 = get_instagram_data(query="Nigeria tourism", max_results=7)
    for item in ig_data_2:
        print(f"Source: {item['source']}, Date: {item['date']}, Text: {item['text'][:80]}...")
