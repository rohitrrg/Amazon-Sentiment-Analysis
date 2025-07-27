from bs4 import BeautifulSoup
import requests

class AmazonProductDetails:
    def __init__(self):
        self.amazon = "https://www.amazon.in"
        self.HEADER = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) Gecko/20100101 Firefox/141.0',
            'Accept-Language': 'en-US, en;q=0.5'})
    
    def error(self, soup, filename):
        with open(f"{filename}_error.html", "w", encoding="utf-8") as f:
            f.write(soup.prettify())

    def get_page(self, url):
        page = requests.get(url, headers=self.HEADER)
        soup = BeautifulSoup(page.content, features="html.parser")
        return soup
    
    def search_product(self, product_name):
        url = f"https://www.amazon.in/s?k={product_name}"
        soup = self.get_page(url)
        links = soup.find_all("a", attrs={'class': "a-link-normal s-line-clamp-2 s-line-clamp-3-for-col-12 s-link-style a-text-normal"})
        link = links[0].get('href')
        return link
    
    def get_product_details(self, product_name):
        url = self.search_product(product_name)
        url = self.amazon + url
        soup = self.get_page(url)
        title = soup.find('span', attrs={'id':'productTitle'}).text.strip()
        price = soup.find('span', attrs={'class':'a-price-whole'}).text.strip()
        try:
            img_url = soup.find('img', {'class':'a-dynamic-image a-stretch-horizontal'}).get('src')
        except:
            img_url = soup.find('img', {'class':'a-dynamic-image a-stretch-vertical'}).get('src')
        reviews = self.get_reviews(soup)

        return {'title':title, 'price':price, 'img_url':img_url, 'reviews':reviews}
    
    def get_reviews(self, soup):
        reviews = soup.find_all('li', {'data-hook':'review'})
        dict = {'review':[], 'rating':[]}
        if len(reviews)!=0:
            for review in reviews:
                try:
                    rating = review.find('span', {"class":'a-icon-alt'}).text.split(' ')[0]
                    rating = float(rating)
                except Exception as e:
                    print(e)
                    self.error(review, 'rating')
                    rating = 0
                
                review_body = review.find('div', {'data-hook':'review-collapsed'}).text
                dict['review'].append(review_body); dict['rating'].append(rating)

            return dict
        return dict
