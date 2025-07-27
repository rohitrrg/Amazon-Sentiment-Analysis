import streamlit as st
import numpy as np
import streamlit as st
from PIL import Image
import requests
from io import BytesIO
from scraper import AmazonProductDetails
from sentiment_analyzer import SentimentAnalyzer

scrapy = AmazonProductDetails()
sentiment_analyzer = SentimentAnalyzer(model_name="fine_tuned_sentiment_model")

st.set_page_config(page_title="Amazon Product Review Sentiment Analysis", layout="centered")

st.markdown(
    """
    <style>
    .main { background-color: #f7f7f7; }
    .review-box { background-color: white; padding: 1em; border-radius: 10px; box-shadow: 0 0 5px #ccc; margin-bottom: 1em; }
    .sentiment-positive { color: green; font-weight: bold; }
    .sentiment-negative { color: red; font-weight: bold; }
    .sentiment-neutral { color: gray; font-weight: bold; }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🛒 Amazon Product Review Sentiment Analysis")

st.write("Enter a product name to analyze reviews and detect sentiment.")

with st.form(key="product_form"):
    product_name = st.text_input("🔍 Product Name")
    submit = st.form_submit_button("Search")

if submit and product_name.strip() != "":
    with st.spinner("Fetching product data..."):
        product_data = scrapy.get_product_details(product_name)

    st.markdown("### 🛒 Product Details")

    # Product Display
    col1, col2 = st.columns([1,2])

    with col1:
        response = requests.get(product_data["img_url"])
        img = Image.open(BytesIO(response.content))
        st.image(img, width=250)
    
    with col2:
        st.markdown(f" {product_data['title']}")
        st.markdown(f"**💰 Price:**  {product_data['price']}")
    

    reviews_ratings = product_data['reviews']
    reviews = reviews_ratings['review']
    ratings = reviews_ratings['rating']

    sentiments = sentiment_analyzer.predict_sentiment(reviews)

    # Reviews
    st.markdown("### 💬 Reviews with Sentiment")
    for i in range(len(reviews)):
        review = reviews[i]
        rating = ratings[i]
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
                <strong>⭐ Rating: </strong> {int(rating)} / 5<br>
                <strong>📝 Review: </strong> {review}<br>
                <strong>📊 Sentiment: </strong> <span class="{sentiment_class}">{emoji} {sentiment_text}</span>
            </div>
        """, unsafe_allow_html=True)