from bs4 import BeautifulSoup
import requests
import re

class AmazonReviews:
    def __init__(self, product_link):
        self.product_link = product_link
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36','referer':self.product_link}
        page = requests.get(self.product_link, headers=self.header)
        self.soup = BeautifulSoup(page.content, features="lxml")
        self.title = self.soup.findAll("span", {"class": "a-size-large product-title-word-break"})[0].text[7:]
        print(self.title)

    def searchreviewpage(self, review_link):
        url = str(self.product_link[:21])+review_link
        page = requests.get(url,headers=self.header)
        if page.status_code==200:
            return page
        else:
            return "Error"


    def scrap(self, pages=10, sortby="recent"):
        reviews_link =  self.soup.findAll("a", {"data-hook":"see-all-reviews-link-foot"})[0]['href']
        reviews = []
        for num in range(1, pages+1):
            reviewpage = self.searchreviewpage(reviews_link+"&pageNumber="+str(num)+"&sortBy="+str(sortby)) # "helpful"
            if reviewpage != "Error":
                soup = BeautifulSoup(reviewpage.content, features="lxml")
                temp =  soup.findAll('span', {'data-hook':'review-body'})
                if len(temp)!=0:
                    for i in temp:
                        if len(i.text)>5:
                            reviews.append(re.sub("\n", "", i.text))
                        else:
                            pass
                else:
                    break
    
        return reviews