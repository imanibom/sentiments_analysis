# utils/fetch_rss.py
import feedparser
from datetime import datetime, date, timedelta
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_rss_articles(rss_feed_url="https://punchng.com/feed/"):
    """
    Fetches articles from an RSS feed and formats them.
    Includes robust fallback dummy data if the real fetch fails.
    Ensures 'date' field is a datetime.date object.

    Args:
        rss_feed_url (str): The URL of the RSS feed to parse.

    Returns:
        list: A list of dictionaries, where each dictionary represents an RSS article
              with 'source', 'title', 'text', and 'date' fields.
    """
    articles = []
    
    # --- Attempt to fetch real RSS data ---
    try:
        logging.info(f"Attempting to fetch RSS articles from: {rss_feed_url}")
        feed = feedparser.parse(rss_feed_url)
        if feed.bozo:
            logging.warning(f"Bozo bit set for RSS feed {rss_feed_url}: {feed.bozo_exception}")

        if feed.entries:
            for entry in feed.entries:
                try:
                    published_date = None
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        # Ensure it's a date object
                        published_date = datetime(*entry.published_parsed[:6]).date()
                    else:
                        published_date = date.today() - timedelta(days=5) # Default to a recent past date
                        logging.warning(f"No publish date found for RSS entry: {entry.title}. Using a default past date.")

                    articles.append({
                        'source': 'RSS',
                        'title': entry.title,
                        'text': entry.summary if hasattr(entry, 'summary') else entry.title,
                        'date': published_date
                    })
                except Exception as e:
                    logging.error(f"Error processing RSS entry '{entry.title if hasattr(entry, 'title') else 'N/A'}': {e}")
                    continue
            if articles: # Only return if actual articles were fetched
                logging.info(f"Successfully fetched {len(articles)} articles from RSS.")
                return articles
            else:
                logging.warning("No valid entries found in the fetched RSS feed, falling back to dummy.")

    except Exception as e:
        logging.error(f"Failed to fetch or parse RSS feed from {rss_feed_url}: {e}. Falling back to dummy data.")

    # --- Fallback to richer dummy data if real fetch fails or yields no entries ---
    logging.info("Falling back to richer dummy RSS data for testing.")
    today = date.today()
    dummy_articles = [
        {
            'source': 'RSS',
            'title': 'Governor Umo Eno Flags Off Ibom Air Maintenance Hangar',
            'text': 'Governor Umo Eno of Akwa Ibom State today commissioned the new Ibom Air Maintenance Hangar, a landmark achievement set to boost aviation in the region. This is a very positive development for the state.',
            'date': today - timedelta(days=1)
        },
        {
            'source': 'RSS',
            'title': 'Akwa Ibom Residents Express Concerns Over Road Construction Delays',
            'text': 'Some residents in Akwa Ibom have voiced dissatisfaction regarding the slow pace of certain road construction projects. They urge Governor Umo Eno\'s administration to expedite work.',
            'date': today - timedelta(days=3)
        },
        {
            'source': 'RSS',
            'title': 'Education Sector Reforms in Akwa Ibom Yielding Mixed Results',
            'text': 'The recently introduced education reforms by the Akwa Ibom State government under Governor Eno are showing varied outcomes, with some improvements noted but also areas requiring more attention.',
            'date': today - timedelta(days=5)
        },
        {
            'source': 'RSS',
            'title': 'Governor Umo Eno Commends Youth Engagement in Agriculture',
            'text': 'Governor Umo Eno praised the rising interest of Akwa Ibom youth in agricultural initiatives, highlighting the state\'s commitment to food security and youth empowerment.',
            'date': today - timedelta(days=2)
        },
        {
            'source': 'RSS',
            'title': 'Analysis: Akwa Ibom State Budget Implementation for Q2',
            'text': 'A detailed analysis of Akwa Ibom State\'s Q2 budget implementation indicates a neutral trajectory with expenditures aligned with planned targets, though some sectors saw minor deviations.',
            'date': today - timedelta(days=7)
        },
        {
            'source': 'RSS',
            'title': 'Stakeholders React to Governor Eno\'s Infrastructure Plans',
            'text': 'Industry stakeholders in Akwa Ibom have offered diverse reactions to Governor Umo Eno\'s ambitious infrastructure development plans, with some expressing optimism and others caution.',
            'date': today - timedelta(days=9)
        },
        {
            'source': 'RSS',
            'title': 'New Healthcare Policy Announced for Akwa Ibom Rural Areas',
            'text': 'The Akwa Ibom State government under Governor Umo Eno has announced a new healthcare policy aimed at improving access to medical services in underserved rural communities.',
            'date': today - timedelta(days=4)
        },
        {
            'source': 'RSS',
            'title': 'Controversy Arises Over Land Acquisition in Akwa Ibom',
            'text': 'A recent land acquisition by the state government in Akwa Ibom has sparked controversy, leading to protests by affected families. This is a negative development for local relations.',
            'date': today - timedelta(days=10)
        },
        {
            'source': 'RSS',
            'title': 'Akwa Ibom Delegation Attends National Investment Forum',
            'text': 'A high-level delegation from Akwa Ibom State, led by officials from Governor Eno\'s office, participated in a national investment forum, showcasing the state\'s potentials.',
            'date': today - timedelta(days=6)
        },
        {
            'source': 'RSS',
            'title': 'Governor Umo Eno Reaffirms Commitment to Industrialization',
            'text': 'During a recent forum, Governor Umo Eno reiterated his administration\'s unwavering commitment to accelerating industrial growth in Akwa Ibom State.',
            'date': today - timedelta(days=12)
        }
    ]
    return dummy_articles

# Example usage (for testing, can be removed in production)
if __name__ == "__main__":
    print("Fetching sample RSS articles (testing real and dummy fallback)...")
    sample_articles = get_rss_articles()
    for article in sample_articles[:10]: # Print first 10 for brevity
        print(f"Source: {article['source']}, Date: {article['date']}, Title: {article['title'][:70]}...")
