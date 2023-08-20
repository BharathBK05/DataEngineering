from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

class flipkart():
    def __init__(self) -> None:

        #include your browser user agent
        self.HEADERS = ({'User-Agent':'', 'Accept-Language': 'en-US, en;q=0.5'})
        self.URL = "https://www.flipkart.com/search?q=iphone&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
        
    
    def get_links(self):
        webpage = requests.get(self.URL, headers=self.HEADERS)
        soup = BeautifulSoup(webpage.content, "html.parser")
        links = soup.find_all("a", attrs={'class':'_1fQZEK'})
        links_list = []

        for link in links:
                links_list.append(link.get('href'))

        dic = {"title":[], "price":[]}
        
        for link in links_list:
            new_webpage = requests.get("https://www.flipkart.com" + link, headers=self.HEADERS)

            new_soup = BeautifulSoup(new_webpage.content, "html.parser")

            dic['title'].append(self.get_title(new_soup))
            dic['price'].append(self.get_price(new_soup))

        
        flipkart_df = pd.DataFrame.from_dict(dic)
        flipkart_df['title'].replace('', np.nan, inplace=True)
        flipkart_df = flipkart_df.dropna(subset=['title'])
        flipkart_df.to_csv("flipkart_iphone.csv", header=True, index=False)

        
    def get_title(self,soup):

        try:
            title = soup.find("span", attrs={"class":'B_NuCI'})
            title_value = title.text
            title_string = title_value.strip()

        except AttributeError:
            title_string = ""

        return title_string


    def get_price(self,soup):

        try:
            price = soup.find("div", attrs={'class':'_30jeq3 _16Jk6d'}).string.strip()
            return price

        except Exception as e:
            print(e)


if __name__ == '__main__':
    obj = flipkart()
    obj.get_links()