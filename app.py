from flask import Flask, render_template, request, render_template_string
import pickle
import re
from scrapy import AmazonReviews
import pandas as pd

app = Flask(__name__)

model = pickle.load(open('model.pkl', 'rb'))
countvect = pickle.load(open('countvect.pkl','rb'))
stwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]


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

@app.route('/', methods=['POST'])
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
    htm = df.to_html()
    pos_count = round((pos_count/total)*100)
    neg_count = round((neg_count/total)*100)

    return render_template('index.html', product = obj.title, 
                                        rev_count = total,
                                        pos_per = str(pos_count)+"%",
                                        neg_per = str(neg_count)+"%",
                                        url = htm)


    


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
    app.run(debug=True)