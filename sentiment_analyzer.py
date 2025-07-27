from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import re

LABEL_MAPPING = {0: "Negative", 1: "Positive"}

class SentimentAnalyzer:
    
    def __init__(self, model_name):

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        print(f'Loaded Tokenizer and Model for model {model_name}')

    def clean_text(self, reviews):
        temp_reviews = []
        for text in reviews:
            # Replace digits with '0'
            text = re.sub(r'\d', '0', text)

            # Remove links and URLs
            if 'www.' in text or 'http:' in text or 'https:' in text or '.com' in text:
                text = re.sub(r"(?:https?://|www\.)\S+|\b\S*\.com\S*", " ", text)

            # Remove non-alphabetic characters (except spaces)
            text = re.sub(r'[^a-zA-Z\s]', ' ', text)

            # Remove extra spaces and strip leading/trailing whitespace
            text = re.sub(r'\s+', ' ', text).strip()

            temp_reviews.append(text)
        return temp_reviews

    def preprocess(self, reviews):
        
        reviews = self.clean_text(reviews)

        encodings = self.tokenizer(
                reviews,
                truncation=True,
                padding=True,
                max_length=128,
                return_tensors='pt'
        )

        return encodings
    
    def predict_sentiment(self, reviews):
        
        encodings = self.preprocess(reviews)

        # perform inderence
        with torch.no_grad():
            outputs = self.model(**encodings)
        
        # Get predicted class probabilities and then the class with highest probability
        logits = outputs.logits
        predictions = torch.argmax(logits, dim=1).cpu().numpy()

        # Map numerical predictions back to sentiment labels
        sentiment_labels = [LABEL_MAPPING[p] for p in predictions]
        
        return sentiment_labels
