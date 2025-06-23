# utils/visualize.py
import streamlit as st
import pandas as pd
import altair as alt
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def show_charts(data):
    """
    Displays various charts in a Streamlit application based on sentiment analysis data.

    Args:
        data (list): A list of dictionaries, where each dictionary is expected to have
                     'date', 'sentiment', and optionally 'score' and 'source' keys.
                     Example: [{'date': date_obj, 'sentiment': 'Positive', 'score': 0.9, 'text': '...'}]
    """
    if not isinstance(data, list):
        logging.error("Input 'data' must be a list. Received type: %s", type(data))
        st.error("Error: Invalid data format for visualization. Please provide a list.")
        return

    # Convert list of dictionaries to DataFrame
    df = pd.DataFrame(data)

    # Basic data validation after DataFrame creation
    if df.empty:
        st.warning("No data available to display charts. Please ensure data is loaded.")
        return

    # Ensure required columns exist
    required_columns = ['date', 'sentiment']
    if not all(col in df.columns for col in required_columns):
        missing_cols = [col for col in required_columns if col not in df.columns]
        logging.error("Missing required columns in DataFrame: %s. Available columns: %s", missing_cols, df.columns.tolist())
        st.error(f"Error: Data is missing required columns for visualization ({', '.join(missing_cols)}).")
        return

    # --- Data Preprocessing for Visualization ---
    # Ensure 'date' column is in datetime format for proper charting
    if pd.api.types.is_object_dtype(df['date']): # Check if it's not already a datetime object
        try:
            # Attempt to convert to datetime, handling potential errors
            df['date'] = pd.to_datetime(df['date'])
        except Exception as e:
            logging.error(f"Could not convert 'date' column to datetime: {e}")
            st.error("Error: 'date' column could not be parsed. Please ensure dates are in a valid format.")
            return

    # Ensure 'sentiment' is categorical for consistent plotting
    if 'sentiment' in df.columns:
        df['sentiment'] = df['sentiment'].astype('category')

    # Add a title to the visualization section
    st.title("Sentiment Analysis Dashboard")

    # --- 1. Sentiment Over Time (Original Chart, improved) ---
    st.subheader("Sentiment Distribution Over Time")

    # Aggregate sentiment counts by date
    sentiment_count = df.groupby(['date', 'sentiment']).size().reset_index(name='count')

    # Create the Altair chart
    # Use 'utcoffset=False' for date axis to prevent unexpected UTC conversions
    chart_sentiment_time = alt.Chart(sentiment_count).mark_bar().encode(
        x=alt.X('date:T', title='Date', axis=alt.Axis(format='%Y-%m-%d')),
        y=alt.Y('count:Q', title='Number of Items'),
        color=alt.Color('sentiment:N', title='Sentiment',
                        scale=alt.Scale(domain=['Positive', 'Negative', 'Neutral'],
                                        range=['#2ca02c', '#d62728', '#1f77b4'])), # Custom colors
        tooltip=['date:T', 'sentiment:N', 'count:Q'] # Add tooltips for interactivity
    ).properties(
        title='Sentiment Distribution Over Time'
    ).interactive() # Enable zooming and panning

    st.altair_chart(chart_sentiment_time, use_container_width=True)


    # --- 2. Overall Sentiment Breakdown (Pie Chart/Donut Chart) ---
    st.subheader("Overall Sentiment Breakdown")

    # Count overall sentiment occurrences
    overall_sentiment_counts = df['sentiment'].value_counts().reset_index()
    overall_sentiment_counts.columns = ['sentiment', 'count']

    # Create a pie/donut chart
    chart_overall_sentiment = alt.Chart(overall_sentiment_counts).mark_arc(outerRadius=120).encode(
        theta=alt.Theta("count:Q", stack=True),
        color=alt.Color("sentiment:N", title='Sentiment',
                        scale=alt.Scale(domain=['Positive', 'Negative', 'Neutral'],
                                        range=['#2ca02c', '#d62728', '#1f77b4'])),
        order=alt.Order("count:Q", sort="descending"),
        tooltip=["sentiment", "count", alt.Tooltip("count", format=".0f")]
    ).properties(
        title="Overall Sentiment Distribution"
    )

    text_overall_sentiment = chart_overall_sentiment.mark_text(radius=140).encode(
        text=alt.Text("count:Q"),
        order=alt.Order("count:Q", sort="descending"),
        color=alt.value("black") # Set text color to black for better contrast
    )

    st.altair_chart(chart_overall_sentiment + text_overall_sentiment, use_container_width=True)


    # --- 3. Sentiment Score Distribution (if 'score' column exists) ---
    if 'score' in df.columns:
        st.subheader("Sentiment Score Distribution")
        
        # Create a histogram for sentiment scores
        chart_score_distribution = alt.Chart(df).mark_bar().encode(
            x=alt.X('score:Q', bin=alt.Bin(maxbins=20), title='Confidence Score'),
            y=alt.Y('count()', title='Number of Items'),
            color=alt.Color('sentiment:N', title='Sentiment',
                            scale=alt.Scale(domain=['Positive', 'Negative', 'Neutral'],
                                            range=['#2ca02c', '#d62728', '#1f77b4'])),
            tooltip=['score:Q', 'count()']
        ).properties(
            title="Distribution of Sentiment Confidence Scores"
        ).interactive()

        st.altair_chart(chart_score_distribution, use_container_width=True)

    # --- 4. Data Table (for inspection) ---
    st.subheader("Raw Data Table")
    # Display the DataFrame with a maximum height for scrollability
    st.dataframe(df, height=300)

# Example Usage (for testing)
if __name__ == "__main__":
    # Sample data with dates, sentiments, and scores
    from datetime import date, timedelta
    today = date.today()
    sample_data = [
        {'date': today - timedelta(days=2), 'sentiment': 'Positive', 'score': 0.95, 'text': 'Great news today!'},
        {'date': today - timedelta(days=2), 'sentiment': 'Negative', 'score': 0.88, 'text': 'Bad things happened.'},
        {'date': today - timedelta(days=1), 'sentiment': 'Positive', 'score': 0.72, 'text': 'Feeling good.'},
        {'date': today - timedelta(days=1), 'sentiment': 'Positive', 'score': 0.81, 'text': 'Another positive note.'},
        {'date': today - timedelta(days=1), 'sentiment': 'Neutral', 'score': 0.65, 'text': 'Just a fact.'},
        {'date': today, 'sentiment': 'Negative', 'score': 0.91, 'text': 'Very upsetting.'},
        {'date': today, 'sentiment': 'Positive', 'score': 0.78, 'text': 'Good vibes here.'},
        {'date': today, 'sentiment': 'Neutral', 'score': 0.55, 'text': 'It is what it is.'},
        {'date': today, 'sentiment': 'Negative', 'score': 0.60, 'text': 'Not happy.'},
        # Add some data without score for testing robustness
        {'date': today - timedelta(days=3), 'sentiment': 'Positive', 'text': 'No score here'},
        # Add some malformed data for robust testing
        {'date': today, 'sentiment': 'Positive', 'score': 0.99, 'text': 'Yet another good one'},
        {'date': 'invalid-date', 'sentiment': 'Positive', 'score': 0.8, 'text': 'This date will fail conversion'},
        {'date': today, 'not_sentiment': 'Positive', 'score': 0.8, 'text': 'Missing sentiment key'},
        {'date': today, 'sentiment': 'Positive', 'score': 'not_a_number', 'text': 'Score not a number'},
    ]

    print("--- Displaying Sample Charts ---")
    show_charts(sample_data)

    print("\n--- Displaying Charts with Empty Data ---")
    st.header("Test with Empty Data")
    show_charts([])

    print("\n--- Displaying Charts with Missing Columns ---")
    st.header("Test with Missing Columns")
    show_charts([{'date': today, 'text': 'Only text'}]) # Missing sentiment