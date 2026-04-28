from bs4 import BeautifulSoup
import requests

url = 'https://www.newegg.com/p/pl?d=laptop'
page = requests.get(url)

soup = BeautifulSoup(page.text, "html.parser")

products = soup.find_all("div", class_ = "item-container position-relative")

for item in products:
    name = item.find("a", class_ = "item-title")
    name_s = name.text.strip()
    
    price = item.find("li", class_ = "price-current")

    rating = item.find("a", class_ = "item-rating")
    if rating != None:
        rating = rating.find("i")
        rating_s = rating["aria-label"].strip("rated").strip()
    

    print(f"Laptop: {name_s}") 
    print(f"Price: {price.text.strip("\u2013").strip()}")
    print(f"Ratings: {rating_s}")
    print("\n")
