import pandas as pd
from datetime import date, timedelta
import random

def generate_random_sentiment_data(num_records=10):
    """
    Generates a list of dictionaries simulating social media posts and RSS articles
    about Akwa Ibom State and its Governor, with varied sentiments and keywords.

    Args:
        num_records (int): The number of records to generate.

    Returns:
        list: A list of dictionaries, each representing an article/post.
    """
    data = []
    sources = ["RSS", "Twitter", "Facebook", "Instagram", "TikTok"]
    
    # Common keywords and sentiment indicators
    positive_phrases = [
        "fantastic progress", "great initiative", "improving lives", "commendable effort",
        "visionary leadership", "huge success", "transformative impact", "excellent work"
    ]
    negative_phrases = [
        "serious concerns", "disappointing outcome", "needs urgent attention", "facing challenges",
        "insufficient progress", "poor implementation", "frustrating delays", "unacceptable conditions"
    ]
    neutral_phrases = [
        "under review", "ongoing discussions", "updates provided", "current status",
        "awaiting further details", "being monitored", "analysis in progress", "reports indicate"
    ]

    # Combine phrases with keywords for realistic text generation
    templates = [
        # Positive
        "Governor Umo Eno announced {positive_phrase} in {keyword_type} projects.",
        "The recent {keyword_type} {positive_phrase} shows significant {keyword_dev} under Governor Eno.",
        "Excited to see the state continue to {keyword_build} and achieve {positive_phrase} in {keyword_dev}.",
        "The new {keyword_type} {positive_phrase} reflects careful {keyword_budget} planning.",
        "Our state is experiencing {positive_phrase} on the {keyword_road} network.",
        # Negative
        "Residents express {negative_phrase} regarding {keyword_type} maintenance. Needs urgent {keyword_dev}.",
        "Concerns raised about {negative_phrase} in {keyword_dev} due to current {keyword_budget} limitations.",
        "The pace to {keyword_build} new {keyword_type} is {negative_phrase}.",
        "Questions arise over the allocation of {keyword_budget} with {negative_phrase} results.",
        "The {keyword_road} infrastructure is facing {negative_phrase}.",
        # Neutral
        "Discussions on the next phase of {keyword_dev} projects are {neutral_phrase}.",
        "The {keyword_budget} review for {keyword_type} infrastructure is {neutral_phrase}.",
        "Updates on the state's plan to {keyword_build} are {neutral_phrase}.",
        "Report on {keyword_type} network {keyword_dev} indicates {neutral_phrase}.",
        "Status of the {keyword_road} construction remains {neutral_phrase}."
    ]

    keywords = {
        "build": ["build", "construct", "erect"],
        "road": ["road", "highway", "avenue", "street"],
        "development": ["development", "progress", "growth", "advancement"],
        "budget": ["budget", "funds", "allocation", "spending"]
    }

    # Assign specific sentiment to phrases for better control
    sentiment_phrases = {
        "Positive": positive_phrases,
        "Negative": negative_phrases,
        "Neutral": neutral_phrases
    }

    # Ensure a mix of sentiments and keywords
    for i in range(num_records):
        source = random.choice(sources)
        current_date = date.today() - timedelta(days=random.randint(0, 15)) # Data from today to 15 days ago

        sentiment_type = random.choice(list(sentiment_phrases.keys()))
        phrase = random.choice(sentiment_phrases[sentiment_type])
        
        keyword_types = list(keywords.keys())
        keyword_type_chosen_1 = random.choice(keyword_types)
        keyword_chosen_1 = random.choice(keywords[keyword_type_chosen_1])

        # Ensure a second keyword is different from the first, if possible
        available_second_keywords = [k for k in keyword_types if k != keyword_type_chosen_1]
        keyword_type_chosen_2 = random.choice(available_second_keywords) if available_second_keywords else keyword_type_chosen_1
        keyword_chosen_2 = random.choice(keywords[keyword_type_chosen_2])

        text_template = random.choice(templates)
        
        # Replace placeholders with chosen words
        text = text_template.replace("{positive_phrase}", phrase)\
                            .replace("{negative_phrase}", phrase)\
                            .replace("{neutral_phrase}", phrase)\
                            .replace("{keyword_type}", keyword_chosen_1)\
                            .replace("{keyword_dev}", keyword_chosen_2)\
                            .replace("{keyword_build}", random.choice(keywords["build"])) \
                            .replace("{keyword_road}", random.choice(keywords["road"])) \
                            .replace("{keyword_budget}", random.choice(keywords["budget"]))

        # Ensure "Umo Eno" or "Governor Eno" is present in roughly half the articles
        if random.random() < 0.6:
            gov_name = "Governor Umo Eno" if random.random() < 0.5 else "Governor Eno"
            text = f"{gov_name} {text[0].lower()}{text[1:]}" if text.startswith(text[0].upper()) else f"{gov_name}'s administration {text}"

        title_prefix = {
            "RSS": "News Update:",
            "Twitter": "Tweet by @AkwaIbom",
            "Facebook": "Facebook Post:",
            "Instagram": "IG Update:",
            "TikTok": "Trending Clip:"
        }
        title = f"{title_prefix[source]} {text[:60]}..."

        data.append({
            'source': source,
            'title': title,
            'text': text,
            'date': current_date
        })
    return data

if __name__ == "__main__":
    generated_data = generate_random_sentiment_data(num_records=20) # Generate more records for better variety
    df = pd.DataFrame(generated_data)
    
    # FIX: Convert the 'date' column which contains datetime.date objects to strings
    # astype(str) will correctly format datetime.date objects to 'YYYY-MM-DD' strings by default.
    df['date'] = df['date'].astype(str)

    output_file = "sample_sentiment_data.csv"
    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"Generated {len(generated_data)} records and saved to {output_file}")
    print("\nSample of generated data:")
    print(df.head())
    print("\nData generation complete.")