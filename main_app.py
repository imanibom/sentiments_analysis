import streamlit as st
import pandas as pd
from datetime import date, timedelta, datetime
import logging
import os # Import os to check for file existence

# Configure logging for the main app
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Streamlit Page Configuration (MUST BE THE ABSOLUTE FIRST Streamlit command) ---
st.set_page_config(
    page_title="Akwa Ibom Governor Sentiment Tracker",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.example.com/help',
        'Report a bug': "https://www.example.com/bug",
        'About': "# This is a sentiment analysis dashboard for Akwa Ibom State Governor's mentions."
    }
)

# --- Custom CSS for Styling (ONLY ONCE, right after set_page_config) ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    html, body, [class*="st-emotion"] {
        font-family: 'Inter', sans-serif;
        color: #333;
    }

    /* General background and primary colors */
    .stApp {
        background-color: #f0f2f6; /* Light gray background for the whole app */
    }

    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #1f77b4; /* A deep blue, can be changed to a darker green or orange if preferred for titles */
        font-weight: 600;
    }

    /* Main title bar */
    .st-emotion-cache-18ni7ap { /* Class for the main header container */
        background-color: #f8f8f8; /* Off-white for header */
        padding: 1rem 2rem;
        border-bottom: 1px solid #eee;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    /* Sidebar styling */
    .st-emotion-cache-vk3305 { /* Sidebar container */
        background-color: #ffffff; /* White sidebar background */
        border-right: 1px solid #eee;
        padding: 20px;
        box-shadow: 2px 0 5px rgba(0,0,0,0.05);
    }

    /* Sidebar Header */
    .st-emotion-cache-10sv2r9 { /* Sidebar header element */
        color: #0c6a38; /* Green for sidebar header */
        font-weight: 700;
        border-bottom: 2px solid #ff8c00; /* Orange underline */
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #0c6a38; /* Green button */
        color: white;
        border-radius: 8px;
        padding: 0.75rem 1.25rem;
        font-weight: 600;
        transition: background-color 0.3s ease, transform 0.2s ease;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton > button:hover {
        background-color: #094d29; /* Darker green on hover */
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0,0,0,0.15);
    }
    .stButton > button:active {
        transform: translateY(0);
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    /* Multiselect and text input styling */
    .stMultiSelect, .stTextInput, .stDateInput {
        margin-bottom: 15px;
    }
    .stMultiSelect > div > div, .stTextInput > div > div > input, .stDateInput > div > div > input {
        border-radius: 8px;
        border: 1px solid #ccc;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.05);
        padding: 0.5rem 1rem;
        background-color: #fdfdfd;
    }

    /* Info/Warning/Success messages */
    .stAlert {
        border-radius: 8px;
        font-weight: 500;
    }
    .stAlert.info {
        background-color: #e0f2f7;
        color: #2980b9;
        border-left: 5px solid #2980b9;
    }
    .stAlert.warning {
        background-color: #fff3e0;
        color: #ff8c00; /* Orange for warning */
        border-left: 5px solid #ff8c00;
    }
    .stAlert.success {
        background-color: #e6ffe6;
        color: #0c6a38; /* Green for success */
        border-left: 5px solid #0c6a38;
    }

    .st-emotion-cache-16idsms p { /* For the text above charts */
        font-size: 1.1em;
        line-height: 1.6;
    }

    div[data-testid="stMetric"] {
        background-color: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        text-align: center;
        transition: transform 0.3s ease;
        height: 100%; /* Ensure uniform height in columns */
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
    }
    div[data-testid="stMetricLabel"] {
        font-size: 1.1em;
        color: #555;
        font-weight: 500;
    }
    div[data-testid="stMetricValue"] {
        font-size: 2em;
        font-weight: 700;
        color: #0c6a38; /* Green for values */
    }

    /* Specific colors for sentiment values in metrics */
    div[data-testid="stMetricValue"].positive {
        color: #2ca02c; /* Strong green */
    }
    div[data-testid="stMetricValue"].negative {
        color: #d62728; /* Red */
    }
    div[data-testid="stMetricValue"].neutral {
        color: #1f77b4; /* Blue */
    }


    /* Chart Container Styling */
    .element-container {
        background-color: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Import necessary utility functions
# Only sentiment_analysis and visualize are strictly needed for the CSV loading path
from utils.sentiment_analysis import analyze_sentiment
from utils.visualize import show_charts

# --- Header Section ---
st.markdown("<h1 style='text-align: center; color: #0c6a38;'>📊 Akwa Ibom Governor Sentiment Tracker 📊</h1>", unsafe_allow_html=True)
st.markdown(
    """
    <p style='text-align: center; font-size: 1.1em; color: #555;'>
        Analyze public sentiment regarding Governor Umo Eno from various online sources.
        Gain insights into trends, overall sentiment breakdown, and confidence scores.
    </p>
    """, unsafe_allow_html=True
)


# --- Sidebar Filters ---
st.sidebar.header("Analysis Options")
source_option = st.sidebar.multiselect(
    "Select Source(s)",
    ["RSS", "Twitter", "Facebook", "Instagram", "TikTok"],
    default=["RSS", "Twitter"], # Default values
    help="Choose the social media and news sources to include in the analysis."
)

# Default to last 7 days for date range
today = date.today()
last_7_days = [today - timedelta(days=7), today]

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=last_7_days, # Set default value
    key="date_input_range",
    help="Filter data by creation date. Leave empty for all dates."
)

keyword_filter = st.sidebar.text_input(
    "Filter by Keyword (case-insensitive)",
    placeholder="e.g., road, development, budget",
    key="keyword_input",
    help="Only show items containing this keyword in their text/description."
)

sentiment_filter = st.sidebar.multiselect(
    "Filter by Sentiment",
    ["Positive", "Neutral", "Negative"],
    default=["Positive", "Neutral", "Negative"],
    key="sentiment_multiselect",
    help="Include or exclude specific sentiment categories."
)

# --- Initial Data Load & Sentiment Analysis (Always run on first load and reruns) ---
# Initialize session state for data storage unconditionally at the top level
if 'analyzed_data_raw' not in st.session_state:
    st.session_state.analyzed_data_raw = [] # Will hold raw hardcoded data initially
if 'analyzed_data' not in st.session_state:
    st.session_state.analyzed_data = [] # Will hold sentiment-analyzed data

# Path to the generated CSV file
DATA_CSV_FILE = "sample_sentiment_data.csv"

# Load data from CSV if available, otherwise prompt to generate
if not st.session_state.analyzed_data or not os.path.exists(DATA_CSV_FILE):
    st.info(f"Loading data from '{DATA_CSV_FILE}'...")
    if os.path.exists(DATA_CSV_FILE):
        try:
            # Read CSV and ensure 'date' column is parsed as datetime.date
            df_loaded = pd.read_csv(DATA_CSV_FILE)
            df_loaded['date'] = pd.to_datetime(df_loaded['date']).dt.date
            
            st.session_state.analyzed_data_raw = df_loaded.to_dict('records')
            st.write(f"DEBUG: Loaded {len(st.session_state.analyzed_data_raw)} items from CSV.")

            st.write(f"Processing {len(st.session_state.analyzed_data_raw)} items for sentiment analysis...")
            st.session_state.analyzed_data = analyze_sentiment(st.session_state.analyzed_data_raw)
            st.write(f"DEBUG: Sentiment analysis performed. Resulting items: {len(st.session_state.analyzed_data)}")

            st.markdown("### 🛠️ Debug Preview: Analyzed Data Snapshot (CSV Load)")
            st.write(f"📅 Today is: {datetime.today().date()}")
            if st.session_state.analyzed_data:
                debug_df_initial = pd.DataFrame(st.session_state.analyzed_data)
                st.dataframe(debug_df_initial[['date', 'source', 'sentiment', 'score', 'text']].head(10))
                st.write(f"Type of 'date' column in analyzed data: {debug_df_initial['date'].dtype}")
            else:
                st.info("⚠️ No data returned from sentiment analysis for CSV input. Check sentiment_analysis.py or CSV content.")
            st.success("Analysis complete! Data loaded from CSV. View the insights below.")

        except Exception as e:
            st.error(f"Error loading or processing data from {DATA_CSV_FILE}: {e}")
            st.warning("Please ensure the CSV file is correctly formatted. If the issue persists, try regenerating it.")
            st.session_state.analyzed_data_raw = []
            st.session_state.analyzed_data = []
    else:
        st.warning(f"'{DATA_CSV_FILE}' not found. Please run `generate_test_data.py` to create it.")
        st.session_state.analyzed_data_raw = []
        st.session_state.analyzed_data = []

# This button explicitly triggers fetching from utils functions
if st.sidebar.button("🔄 Re-Run Analysis (Using Live Data Sources)", key="rerun_live_data_button"):
    st.info("Re-running analysis using selected live data sources. This will replace current data.")
    all_raw_data_live = []
    with st.status("Fetching live data and performing sentiment analysis...", expanded=True) as status_message:
        # Import utilities here, as they are only needed when this button is clicked
        from utils.fetch_rss import get_rss_articles
        from utils.scrape_twitter import get_twitter_data
        from utils.scrape_facebook import get_facebook_data
        from utils.scrape_instagram import get_instagram_data
        from utils.scrape_tiktok import get_tiktok_data

        if "RSS" in source_option:
            st.write("Fetching RSS articles...")
            rss_fetched_data = get_rss_articles()
            all_raw_data_live.extend(rss_fetched_data)
            st.write(f"  Fetched {len(rss_fetched_data)} RSS items.")
        if "Twitter" in source_option:
            st.write("Fetching Twitter data...")
            twitter_fetched_data = get_twitter_data(query="Umo Eno Akwa Ibom", max_results=50)
            all_raw_data_live.extend(twitter_fetched_data)
            st.write(f"  Fetched {len(twitter_fetched_data)} Twitter items.")
        if "Facebook" in source_option:
            st.write("Fetching Facebook data (dummy from utils)...")
            facebook_fetched_data = get_facebook_data(query="Akwa Ibom Governor", max_results=20)
            all_raw_data_live.extend(facebook_fetched_data)
            st.write(f"  Fetched {len(facebook_fetched_data)} Facebook items.")
        if "Instagram" in source_option:
            st.write("Fetching Instagram data (dummy from utils)...")
            instagram_fetched_data = get_instagram_data(query="Umo Eno Akwa Ibom", max_results=20)
            all_raw_data_live.extend(instagram_fetched_data)
            st.write(f"  Fetched {len(instagram_fetched_data)} Instagram items.")
        if "TikTok" in source_option:
            st.write("Fetching TikTok data (dummy from utils)...")
            tiktok_fetched_data = get_tiktok_data(query="Akwa Ibom Governor", max_results=20)
            all_raw_data_live.extend(tiktok_fetched_data)
            st.write(f"  Fetched {len(tiktok_fetched_data)} TikTok items.")

        st.write(f"Total raw live data collected: {len(all_raw_data_live)} items.")

        if not all_raw_data_live:
            status_message.update(label="No live data fetched!", state="error", expanded=False)
            st.warning("No live data fetched from the selected sources. Please check your selections or API keys.")
            st.session_state.analyzed_data = []
            st.session_state.analyzed_data_raw = [] # Clear raw data too
        else:
            st.write(f"Processing {len(all_raw_data_live)} items for sentiment analysis...")
            st.session_state.analyzed_data = analyze_sentiment(all_raw_data_live)
            st.session_state.analyzed_data_raw = all_raw_data_live # Store raw live data too if needed for later debug
            st.write(f"Sentiment analysis completed for {len(st.session_state.analyzed_data)} items.")
            status_message.update(label="Live analysis complete!", state="complete", expanded=False)
            st.success("Live analysis complete! View the insights below.")


# Always apply filters to the currently available analyzed_data from session_state
filtered_data = list(st.session_state.analyzed_data) # Create a copy to modify during filtering

# --- DEBUGGING OUTPUTS (Final Filter Checks) ---
st.info(f"DEBUG: Data before filtering: {len(filtered_data)} items")


# Apply Keyword Filter
if keyword_filter:
    logging.info(f"Applying keyword filter: '{keyword_filter}'")
    original_count = len(filtered_data)
    filtered_data = [
        item for item in filtered_data
        if 'text' in item and isinstance(item['text'], str) and keyword_filter.lower() in item['text'].lower()
    ]
    st.info(f"DEBUG: Data after Keyword Filter ('{keyword_filter}'): {len(filtered_data)} items (from {original_count})")


# Apply Sentiment Filter
if sentiment_filter and set(sentiment_filter) != {"Positive", "Neutral", "Negative"}:
    logging.info(f"Applying sentiment filter: {sentiment_filter}")
    original_count = len(filtered_data)
    filtered_data = [
        item for item in filtered_data
        if 'sentiment' in item and item['sentiment'] in sentiment_filter
    ]
    st.info(f"DEBUG: Data after Sentiment Filter ({sentiment_filter}): {len(filtered_data)} items (from {original_count})")


# Apply Date Range Filter
if date_range and len(date_range) == 2 and all(isinstance(d, date) for d in date_range):
    start_date, end_date = date_range[0], date_range[1]
    logging.info(f"Applying date range filter: {start_date} to {end_date}")
    original_count = len(filtered_data)
    filtered_data = [
        item for item in filtered_data
        if 'date' in item and isinstance(item['date'], date) and start_date <= item['date'] <= end_date
    ]
    st.info(f"DEBUG: Data after Date Range Filter ({start_date} to {end_date}): {len(filtered_data)} items (from {original_count})")
elif date_range and len(date_range) == 1 and isinstance(date_range[0], date):
    selected_date = date_range[0]
    logging.info(f"Applying single date filter: {selected_date}")
    original_count = len(filtered_data)
    filtered_data = [
        item for item in filtered_data
        if 'date' in item and isinstance(item['date'], date) and item['date'] == selected_date
    ]
    st.info(f"DEBUG: Data after Single Date Filter ({selected_date}): {len(filtered_data)} items (from {original_count})")


st.info(f"DEBUG: Final data count after all filters: {len(filtered_data)} items")


if not filtered_data:
    st.info("No data available to display after applying filters. Adjust your selections or click 'Re-Run Analysis (Using Live Data Sources)'.")
else:
    # --- Key Metrics ---
    st.subheader("Overview Metrics")
    total_items = len(filtered_data)
    
    df_metrics = pd.DataFrame(filtered_data)
    if 'sentiment' in df_metrics.columns and not df_metrics.empty:
        sentiment_counts = df_metrics['sentiment'].value_counts()
    else:
        sentiment_counts = pd.Series(dtype='int64')

    positive_count = sentiment_counts.get('Positive', 0)
    negative_count = sentiment_counts.get('Negative', 0)
    neutral_count = sentiment_counts.get('Neutral', 0)

    positive_percent = (positive_count / total_items) * 100 if total_items > 0 else 0
    negative_percent = (negative_count / total_items) * 100 if total_items > 0 else 0
    neutral_percent = (neutral_count / total_items) * 100 if total_items > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Total Items", value=total_items, delta_color="off")
    with col2:
        st.metric(label="Positive Sentiment", value=f"{positive_percent:.1f}%", delta_color="off")
        st.markdown(f"<p style='text-align: center; color: #2ca02c; font-size: 0.9em; margin-top: -15px;'>({positive_count} items)</p>", unsafe_allow_html=True)
    with col3:
        st.metric(label="Negative Sentiment", value=f"{negative_percent:.1f}%", delta_color="off")
        st.markdown(f"<p style='text-align: center; color: #d62728; font-size: 0.9em; margin-top: -15px;'>({negative_count} items)</p>", unsafe_allow_html=True)
    with col4:
        st.metric(label="Neutral Sentiment", value=f"{neutral_percent:.1f}%", delta_color="off")
        st.markdown(f"<p style='text-align: center; color: #1f77b4; font-size: 0.9em; margin-top: -15px;'>({neutral_count} items)</p>", unsafe_allow_html=True)

    st.markdown("---")

    # --- Show Charts ---
    st.subheader(f"Sentiment Trends and Distribution")
    show_charts(filtered_data)


    # --- Export Functionality ---
    st.subheader("Data Export")
    df_export = pd.DataFrame(filtered_data)
    
    if 'score' in df_export.columns:
        df_export['score'] = df_export['score'].round(4)

    col_csv, col_pdf = st.columns(2)

    with col_csv:
        csv_data = df_export.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Data as CSV 💾",
            data=csv_data,
            file_name="sentiment_analysis_data.csv",
            mime="text/csv",
            key="download_csv_button"
        )

    with col_pdf:
        try:
            import pdfkit
            if not df_export.empty:
                html = df_export.to_html(index=False)
                pdf = pdfkit.from_string(html, False, options={
                    "enable-local-file-access": "",
                    "encoding": "UTF-8",
                    "no-stop-slow-scripts": True,
                    "page-size": "A4",
                    "orientation": "Landscape",
                    "margin-top": "1in",
                    "margin-right": "0.75in",
                    "margin-bottom": "1in",
                    "margin-left": "0.75in",
                    "enable-javascript": True,
                    "javascript-delay": 2000
                })
                
                st.download_button(
                    label="Download Data as PDF 📄",
                    data=pdf,
                    file_name="sentiment_analysis_data.pdf",
                    mime="application/pdf",
                    key="download_pdf_button"
                )
            else:
                st.info("No data to export to PDF.")
        except ImportError:
            st.info("To enable PDF export, please install `pdfkit` (`pip install pdfkit`) and `wkhtmltopdf` on your system.")
        except Exception as e:
            st.error(f"PDF export not available due to an error. Ensure `wkhtmltopdf` is installed and its path is configured if necessary. Error: {e}")


    # --- Show Raw Data Table (Toggle) ---
    st.markdown("---")
    if st.checkbox("Show Raw Data Table", key="show_raw_data_checkbox"):
        if filtered_data:
            st.subheader("Filtered Raw Data")
            st.dataframe(pd.DataFrame(filtered_data))
        else:
            st.info("No raw data to display after filtering.")
    else:
        st.info("Check the box to view the raw data table. This shows the original data before sentiment analysis and filtering.")