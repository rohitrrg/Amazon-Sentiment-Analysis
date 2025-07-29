import streamlit as st
from PIL import Image
import requests
from io import BytesIO
from sentiment_analyzer import SentimentAnalyzer
from reviews import Reviews
import plotly.express as px
import pandas as pd

rev = Reviews()
sentiment_analyzer = SentimentAnalyzer(model_name="fine_tuned_sentiment_model")

st.set_page_config(page_title="Amazon Product Review Sentiment Analysis", layout="centered")

st.title("🛒 Amazon Product Review Sentiment Analysis")

st.write("Enter a product name to analyze reviews and detect sentiment.")

with st.form(key="product_form"):
    product_name_selected = st.selectbox(
                 "Choose a Product:",
    options=rev.reviews.keys()
)
    submit = st.form_submit_button("Search")

if submit and product_name_selected.strip() != "":
    with st.spinner("Fetching product data..."):
        product_data = rev.get_review(product_name_selected)

    st.markdown("### 🛒 Product Details")

    reviews = product_data['reviews']
    sentiments = sentiment_analyzer.predict_sentiment(reviews)

    sentiment_counts = pd.Series(sentiments).value_counts()
    total_reviews = len(sentiments)
    st.subheader("Sentiment Distribution")
    sentiment_df = pd.DataFrame(sentiment_counts).reset_index()
    sentiment_df.columns = ['Sentiment', 'Count']
    color_map = {
                    "Positive": "#28a745",
                    "Negative": "#dc3545"
                }
    full_df = pd.DataFrame({'Sentiment': ["Positive", "Negative"]})
    sentiment_df = pd.merge(full_df, sentiment_df, on='Sentiment', how='left').fillna(0)
                

    # Product Display
    col1, col2 = st.columns([1,2])

    with col1:
        response = requests.get(product_data["img_url"])
        img = Image.open(BytesIO(response.content))
        st.image(img, width=250)
    
    with col2:
        st.markdown(f" {product_data['title']}")
        st.markdown(f"**💰 Price:**  {product_data['price']}")
    
    # Display Pie
    fig = px.pie(
                    sentiment_df,
                    values='Count',
                    names='Sentiment',
                    title='Distribution of Sentiments',
                    color='Sentiment',
                    color_discrete_map=color_map,
                    hole=0.3 # Optional: makes it a donut chart
                )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)

    # Reviews
    st.markdown("### 💬 Reviews with Sentiment")
    for i in range(len(reviews)):
        review = reviews[i]
        sentiment = sentiments[i]

        if sentiment == "Positive":
            sentiment_text = f"Positive ✅"
            sentiment_class = "sentiment-positive"
            emoji = "😊"
        else:
            sentiment_text = f"Negative ❌"
            sentiment_class = "sentiment-negative"
            emoji = "😠"

        st.markdown(
                """
                <style>
                .main { background-color: #f7f7f7; }

                .review-box {
                    background-color: black;  /* Light Blue */
                    padding: 1em;
                    border-radius: 10px;
                    box-shadow: 0 0 5px #ccc;
                    margin-bottom: 1em;
                }

                .sentiment-positive { color: green; font-weight: bold; }
                .sentiment-negative { color: red; font-weight: bold; }
                </style>
                """,
                unsafe_allow_html=True
                )
        st.markdown(f"""
            <div class="review-box">
                <strong>📝 Review: </strong> {review}<br>
                <strong>📊 Sentiment: </strong> <span class="{sentiment_class}">{emoji} {sentiment_text}</span>
            </div>
        """, unsafe_allow_html=True)