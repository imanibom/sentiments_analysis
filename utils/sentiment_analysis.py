# utils/sentiment_analysis.py
import logging
from transformers import pipeline

# Configure logging for better error/info messages
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Model Loading (Optimized and Robust) ---
SENTIMENT_MODEL_NAME = "finiteautomata/bertweet-base-sentiment-analysis"
sentiment_pipeline = None

# Define the label mapping
SENTIMENT_LABEL_MAP = {
    'POS': 'Positive',
    'NEG': 'Negative',
    'NEU': 'Neutral'
}

def _load_sentiment_pipeline():
    """
    Loads the sentiment analysis pipeline. This function ensures the model
    is loaded only once and handles potential errors during loading.
    """
    global sentiment_pipeline
    if sentiment_pipeline is None:
        logging.info(f"Attempting to load sentiment analysis model: {SENTIMENT_MODEL_NAME}...")
        try:
            sentiment_pipeline = pipeline("sentiment-analysis", model=SENTIMENT_MODEL_NAME)
            logging.info("Sentiment analysis model loaded successfully.")
        except Exception as e:
            logging.error(f"FATAL ERROR: Failed to load sentiment analysis model {SENTIMENT_MODEL_NAME}: {e}")
            logging.error("Please ensure you have an active internet connection and that the model name is correct.")
            logging.error("You may also need to reinstall transformers and torch/tensorflow if files are corrupted.")
            raise RuntimeError(f"Could not load sentiment analysis model: {e}")

def analyze_sentiment(data):
    """
    Performs sentiment analysis on a list of dictionaries containing 'text' fields.
    Adds 'sentiment' (label) and 'score' to each dictionary, mapping labels
    to 'Positive', 'Negative', 'Neutral'.

    Args:
        data (list): A list of dictionaries, where each dictionary
                     is expected to have a 'text' key.

    Returns:
        list: The input list of dictionaries, with 'sentiment' and 'score'
              keys added to each item. Returns an empty list if input is not valid
              or if the pipeline fails to load or process.
    """
    logging.info(f"analyze_sentiment: Received {len(data)} items for analysis.")

    if not isinstance(data, list):
        logging.error("analyze_sentiment: Input 'data' must be a list.")
        return []

    if not data:
        logging.info("analyze_sentiment: Input 'data' is empty. No sentiment analysis to perform.")
        return []

    # Ensure the pipeline is loaded before processing
    try:
        if sentiment_pipeline is None:
            _load_sentiment_pipeline()
            logging.info("analyze_sentiment: Sentiment pipeline initialized.")
        else:
            logging.info("analyze_sentiment: Sentiment pipeline already loaded.")
    except RuntimeError as e:
        logging.error(f"analyze_sentiment: Sentiment analysis aborted due to model loading error: {e}")
        return []

    texts_to_analyze = []
    original_item_references = [] # Store references to original items to update them directly

    # Prepare texts for batch processing and keep references to original items
    for i, item in enumerate(data):
        if not isinstance(item, dict):
            logging.warning(f"analyze_sentiment: Skipping non-dictionary item at index {i}: {item}")
            continue
            
        if 'text' not in item or not isinstance(item['text'], str):
            logging.warning(f"analyze_sentiment: Skipping item at index {i} due to missing or invalid 'text' key: {item}")
            continue
        
        texts_to_analyze.append(item['text'])
        original_item_references.append(item) # Reference the actual item to modify it in place

    if not texts_to_analyze:
        logging.info("analyze_sentiment: No valid texts extracted for analysis.")
        return [] # Return empty if no valid texts to analyze

    logging.info(f"analyze_sentiment: Extracted {len(texts_to_analyze)} valid texts for batch analysis.")

    try:
        # Process texts in a batch
        results = sentiment_pipeline(texts_to_analyze)
        
        # Ensure results is an iterable (list) before attempting to iterate
        if not isinstance(results, list):
            logging.error(f"analyze_sentiment: Pipeline returned unexpected type: {type(results)}. Expected a list.")
            return [] # Return empty if result is not a list

        logging.info(f"analyze_sentiment: Pipeline returned {len(results)} results.")
        # Logging first few results for inspection
        for k in range(min(3, len(results))):
            logging.info(f"  Sample Result {k}: {results[k]}")

        processed_count = 0
        for j, result in enumerate(results):
            if j >= len(original_item_references):
                logging.warning(f"analyze_sentiment: Mismatch in results and original items count. Skipping result {j}.")
                continue

            original_item = original_item_references[j] # Get the reference to the original item

            if isinstance(result, dict) and 'label' in result and 'score' in result:
                mapped_label = SENTIMENT_LABEL_MAP.get(result['label'], result['label'])
                original_item['sentiment'] = mapped_label
                original_item['score'] = result['score']
                processed_count += 1
            else:
                logging.warning(f"analyze_sentiment: Invalid result format for item {j}: {result}. Skipping sentiment update.")
                original_item['sentiment'] = 'unknown' # Mark as unknown if result is malformed
                original_item['score'] = 0.0

        logging.info(f"analyze_sentiment: Successfully processed {processed_count} items with sentiment.")
        return data # Return the input list, now enriched with sentiment data

    except Exception as e:
        logging.error(f"analyze_sentiment: CRITICAL ERROR during batch sentiment analysis: {e}")
        logging.error("This could be due to memory issues, corrupted model files, or a bug in the pipeline execution.")
        # Attempt to also print traceback for more details
        logging.exception("Full traceback for critical error in analyze_sentiment:")
        return [] # Return empty on critical failure

# Example Usage (for testing purposes - runs when sentiment_analysis.py is executed directly)
if __name__ == "__main__":
    print("\n--- Running direct test of analyze_sentiment ---")
    
    # Test with valid data
    sample_data = [
        {'id': 1, 'text': 'Umo Eno is doing a great job in Akwa Ibom State!'},
        {'id': 2, 'text': 'The current economic situation is challenging.'},
        {'id': 3, 'text': 'I love the new policy initiatives.'},
        {'id': 4, 'text': 'This news is absolutely terrible.'},
        {'id': 5, 'text': 'Neutral statement here.'},
        {'id': 6, 'text': 'Another fantastic day in Akwa Ibom!'}
    ]

    print("\nAnalyzing sample data:")
    analyzed_sample_data = analyze_sentiment(sample_data)
    for item in analyzed_sample_data:
        print(f"ID: {item.get('id')}, Text: '{item['text'][:60]}...', Sentiment: {item.get('sentiment', 'N/A')}, Score: {item.get('score', 'N/A'):.4f}")

    print("\nAnalyzing empty data:")
    empty_data = []
    analyzed_empty_data = analyze_sentiment(empty_data)
    print(f"Result for empty data: {analyzed_empty_data}")

    print("\nAnalyzing invalid data format (should show warnings):")
    invalid_data = [
        {'id': 10, 'content': 'This should be skipped.'}, # Missing 'text'
        {'id': 11, 'text': 123}, # 'text' is not a string
        'not a dict', # Not a dictionary
        {'id': 12, 'text': 'Another valid text.'}
    ]
    analyzed_invalid_data = analyze_sentiment(invalid_data)
    for item in analyzed_invalid_data:
        print(f"Item: {item.get('id')}, Text: {item.get('text', 'N/A')}, Sentiment: {item.get('sentiment', 'N/A')}")
