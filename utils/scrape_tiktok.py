# utils/scrape_tiktok.py
import os
import requests
from datetime import datetime, date, timedelta
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- IMPORTANT NOTE ON TIKTOK SCRAPING ---
# This implementation is a PLACEHOLDER demonstrating structure and WILL ALWAYS
# RETURN DUMMY DATA for demonstration purposes due to the difficulty of real access.
# -------------------------------------------

TIKTOK_ACCESS_TOKEN = os.getenv('TIKTOK_ACCESS_TOKEN')

def create_headers():
    if not TIKTOK_ACCESS_TOKEN:
        logging.warning("TIKTOK_ACCESS_TOKEN environment variable not set. Using dummy data for TikTok.")
    return {
        "Authorization": f"Bearer {TIKTOK_ACCESS_TOKEN if TIKTOK_ACCESS_TOKEN else 'DUMMY_TOKEN'}",
        "Content-Type": "application/json"
    }

def get_tiktok_data(query="Akwa Ibom", max_results=5):
    """
    Simulates fetching data from TikTok, always returning dummy data for demonstration.
    Ensures 'date' field is a datetime.date object.

    Args:
        query (str): A simulated search query.
        max_results (int): Simulated maximum number of results.

    Returns:
        list: A list of dictionaries, where each dictionary represents a TikTok video.
    """
    logging.info("Returning DUMMY TikTok data for demonstration.")

    today = date.today()
    dummy_videos = []
    base_descriptions = [
        f"Umo Eno’s road projects are trending on TikTok in {query}! #Infrastructure",
        f"See how Akwa Ibom is transforming! Amazing progress!",
        f"Join the conversation: What do you think about the latest state initiatives?",
        f"Fun facts about {query} and its vibrant culture! #TravelNigeria"
    ]
    for i in range(max_results):
        video_date = today - timedelta(days=i) # Already a date object
        description = base_descriptions[i % len(base_descriptions)]
        
        # FIX: Convert datetime.date to datetime.datetime before calling timestamp()
        timestamp_for_tiktok = int(datetime.combine(video_date, datetime.min.time()).timestamp())

        dummy_videos.append({
            'id': f'tt_video_{i+1}',
            'description': f"TikTok Clip {i+1}: {description}",
            'create_time': timestamp_for_tiktok,
            'share_url': 'https://www.tiktok.com/@dummy/video/12345',
            'region_code': 'NG'
        })

    processed_data = []
    for video in dummy_videos:
        try:
            # Convert Unix timestamp to datetime object, then get date object
            video_date = datetime.fromtimestamp(video['create_time']).date()

            processed_data.append({
                'source': 'TikTok',
                'title': 'TikTok Video',
                'text': video.get('description', 'No description available'),
                'date': video_date # This will be a datetime.date object
            })
        except Exception as e:
            logging.error(f"Error processing dummy TikTok video data: {e} in video: {video}")

    return processed_data

# Example usage (for testing)
if __name__ == "__main__":
    print("Fetching dummy TikTok data for 'Akwa Ibom'...")
    tiktok_data = get_tiktok_data(query="Akwa Ibom", max_results=3)
    for item in tiktok_data:
        print(f"Source: {item['source']}, Date: {item['date']}, Text: {item['text'][:80]}...")

    print("\nFetching more dummy TikTok data for 'Nigerian food'...")
    tiktok_data_2 = get_tiktok_data(query="Nigerian food", max_results=7)
    for item in tiktok_data_2:
        print(f"Source: {item['source']}, Date: {item['date']}, Text: {item['text'][:80]}...")
