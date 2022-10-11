from flask import Flask, render_template, request
import pickle
from nltk.corpus import stopwords
import re

from scrapy import AmazonReviews
import pandas as pd

app = Flask(__name__)

model = pickle.load(open('model.pkl', 'rb'))
countvect = pickle.load(open('countvect.pkl','rb'))
stwords = stopwords.words('english')



def clean_texts(reviews):
    texts = []
    for i in range(len(reviews)):
        text = re.sub('\d','0',reviews[i])
        if 'www.' in text or 'http:' in text or 'https:' in text or '.com' in text: # remove links and urls
            text = re.sub(r"([^ ]+(?<=\.[a-z]{3}))", " ", text)
        
        text = re.sub('[^a-zA-Z]', ' ', text)
        text = text.lower()
        text = text.split()
        text = [word for word in text if not word in stwords] # remove stopwords 
        text = ' '.join(text)
        texts.append(text)
    return texts


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    link = request.form.get("review")
    obj = AmazonReviews(link)
    reviews = obj.scrap()
    cleaned_reviews = clean_texts(reviews)
    reviews_vect = countvect.transform(cleaned_reviews)
    pred = model.predict(reviews_vect)
    total = len(pred)
    pos_count = (pred==1).sum()
    neg_count = (pred==0).sum()
    df = pd.DataFrame({'Reviews':reviews, 'Sentiments':pred})
    df['Sentiments'] = df['Sentiments'].apply(lambda x: 'negative' if x==0 else 'positive')
    df.to_html('./templates/reviews.html')
    df.to
    pos_count = round((pos_count/total)*100)
    neg_count = round((neg_count/total)*100)

    return render_template('index.html', product = obj.title, 
                                        rev_count = total,
                                        pos_per = str(pos_count)+"%",
                                        neg_per = str(neg_count)+"%")

@app.route('/reviews')
def show_reviews():
    return render_template('reviews.html')

    


# @app.route('/predict',methods=['POST'])
# def predict():
#     '''
#     For rendering results on HTML GUI
#     '''
#     review = request.form.get("review")
#     input_txt = clean_texts(review)
#     input_txt_vec = countvect.transform([input_txt])
#     pred = model.predict(input_txt_vec)

#     if pred[0]==0:
#         output = "Negative"
#     else:
#         output = "Positive"
    
#     return render_template('index.html', review=review, 
#                             prediction_text="prediction: {}.".format(output) )



if __name__=="__main__":
    app.run(port="8000")