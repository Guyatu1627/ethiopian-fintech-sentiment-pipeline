import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ==============================================================================
# 1. PAGE CONFIGURATION & THEME LAYOUT
# ==============================================================================
st.set_page_config(
    page_title="Fintech Customer Experience Analytics",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to match corporate consulting aesthetics
st.markdown("""
    <style>
    .main-title { font-size: 2.2rem; font-weight: 700; color: #1a365d; margin-bottom: 0.5rem; }
    .subtitle { font-size: 1.1rem; color: #4a5568; margin-bottom: 2rem; }
    .metric-card { background-color: #f7fafc; padding: 1.2rem; border-radius: 8px; border: 1px solid #e2e8f0; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🏦 Ethiopian Fintech: Customer Experience Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Real-Time Sentiment Intelligence & Operational Risk Engine | <b>Omega Consultancy</b></div>', unsafe_allow_html=True)

# ==============================================================================
# 2. HIGH-PERFORMANCE DATA INGESTION ENGINE
# ==============================================================================
@st.cache_data
def load_optimized_data():
    # Primary target: Enriched NLP & Topic modeled data from Task 3
    primary_path = "data/analyzed_reviews.csv"
    fallback_path = "data/cleaned_reviews.csv"
    
    if os.path.exists(primary_path):
        df = pd.read_csv(primary_path)
        df['date'] = pd.to_datetime(df['date'])
        return df, "Enriched AI Dataset Loaded"
    elif os.path.exists(fallback_path):
        df = pd.read_csv(fallback_path)
        df['date'] = pd.to_datetime(df['date'])
        # Synthesize fallback sentiment attributes if pipeline is run out of sync
        if 'sentiment_label' not in df.columns:
            df['sentiment_label'] = df['rating'].apply(lambda r: 'Positive' if r >= 4 else ('Negative' if r <= 2 else 'Neutral'))
        return df, "Base Dataset Loaded (Sentiment Approximated)"
    else:
        return None, "Missing Data Artifacts"

df, data_status = load_optimized_data()

if df is None:
    st.error("⚠️ Core Data Framework Not Detected! Please execute your data collection pipeline (`python main.py`) or run your notebook cells to generate files within the `data/` folder directory.")
    st.stop()

# ==============================================================================
# 3. INTERACTIVE MULTI-TENANT SIDEBAR FILTERS
# ==============================================================================
st.sidebar.header("🎛️ Operational Controls")
st.sidebar.markdown("---")

# Bank Multiselect
available_banks = df['bank'].unique()
selected_banks = st.sidebar.multiselect(
    "Select Target Institutions:",
    options=available_banks,
    default=available_banks
)

# Sentiment Multiselect
available_sentiments = df['sentiment_label'].unique()
selected_sentiments = st.sidebar.multiselect(
    "Filter by Sentiment Tone:",
    options=available_sentiments,
    default=available_sentiments
)

# Date Range Slicer
min_date = df['date'].min().to_pydatetime()
max_date = df['date'].max().to_pydatetime()
selected_date_range = st.sidebar.date_input(
    "Select Timeline Window:",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Apply dynamic matrix filtering
filtered_df = df[df['bank'].isin(selected_banks) & df['sentiment_label'].isin(selected_sentiments)]
if len(selected_date_range) == 2:
    start_date, end_date = pd.to_datetime(selected_date_range[0]), pd.to_datetime(selected_date_range[1])
    filtered_df = filtered_df[(filtered_df['date'] >= start_date) & (filtered_df['date'] <= end_date)]

# ==============================================================================
# 4. EXECUTIVE LEVEL KPI SCORECARDS
# ==============================================================================
if filtered_df.empty:
    st.warning("✨ No data metrics available for the selected filter configuration. Adjust your sidebar inputs.")
else:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="Total Analyzed Volume", value=f"{len(filtered_df):,}")
    
    with col2:
        avg_rating = round(filtered_df['rating'].mean(), 2)
        st.metric(label="Mean Experience Score", value=f"{avg_rating} / 5.0")
        
    with col3:
        pos_count = len(filtered_df[filtered_df['sentiment_label'] == 'Positive'])
        pos_pct = (pos_count / len(filtered_df)) * 100 if len(filtered_df) > 0 else 0
        st.metric(label="Customer Satisfaction Share", value=f"{round(pos_pct, 1)}%")
        
    with col4:
        neg_count = len(filtered_df[filtered_df['sentiment_label'] == 'Negative'])
        neg_pct = (neg_count / len(filtered_df)) * 100 if len(filtered_df) > 0 else 0
        st.metric(label="Critical Risk Friction Rate", value=f"{round(neg_pct, 1)}%", delta_color="inverse")

    st.divider()

    # ==============================================================================
    # 5. HIGH-FIDELITY DATA VISUALIZATIONS (PLOTLY HIERARCHY)
    # ==============================================================================
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.subheader("📊 Comparative Sentiment Distribution")
        fig_sentiment = px.histogram(
            filtered_df,
            x="bank",
            color="sentiment_label",
            barmode="group",
            labels={"bank": "Financial Institution", "count": "Total Verified Reviews", "sentiment_label": "Sentiment"},
            color_discrete_map={"Positive": "#2bc4a0", "Negative": "#e53e3e", "Neutral": "#718096"},
            category_orders={"sentiment_label": ["Positive", "Neutral", "Negative"]}
        )
        fig_sentiment.update_layout(plot_bgcolor="rgba(0,0,0,0)", yaxis_title="Review Volumetrics")
        st.plotly_chart(fig_sentiment, use_container_width=True)

    with chart_col2:
        st.subheader("📈 Experience Trajectory Metrics Over Time")
        time_series_data = filtered_df.groupby([filtered_df['date'].dt.date, 'bank'])['rating'].mean().reset_index()
        fig_timeline = px.line(
            time_series_data,
            x="date",
            y="rating",
            color="bank",
            labels={"date": "Timeline Intercept", "rating": "Daily Mean Rating", "bank": "Enterprise Target"},
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        fig_timeline.update_layout(plot_bgcolor="rgba(0,0,0,0)", yaxis=dict(showgrid=True))
        st.plotly_chart(fig_timeline, use_container_width=True)

    st.divider()

    # ==============================================================================
    # 6. REPOSITORY AD-HOC DEEP-DIVE REVIEWS SEARCH LOGIC
    # ==============================================================================
    st.subheader("🔍 Deep-Dive Review & Operational Issue Explorer")
    
    # Text-matching search field
    query_search = st.text_input(
        "Search cross-sectional customer feedback arrays by custom keyword parameters (e.g., 'OTP', 'login', 'network', 'fee'):"
    )
    
    if query_search:
        search_mask = filtered_df['review'].str.contains(query_search, case=False, na=False)
        matched_results = filtered_df[search_mask]
        
        st.markdown(f"Found **{len(matched_results)}** analytical matching entries:")
        st.dataframe(
            matched_results[['bank', 'rating', 'sentiment_label', 'date', 'review']],
            use_container_width=True,
            column_config={
                "date": st.column_config.DateColumn("Review Timestamp", format="YYYY-MM-DD"),
                "rating": st.column_config.NumberColumn("Score (1-5)"),
                "sentiment_label": "Sentiment Category",
                "bank": "Bank Entity",
                "review": "Raw Text Transcript"
            }
        )
    else:
        st.markdown("_Showing raw data matrix view. Input filter expressions above to parse target engineering fault vectors._")
        st.dataframe(
            filtered_df[['bank', 'rating', 'sentiment_label', 'date', 'review']].head(100),
            use_container_width=True
        )