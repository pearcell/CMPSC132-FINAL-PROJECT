from bs4 import BeautifulSoup
import requests

URL = 'https://www.newegg.com/p/pl?d=laptop'

def parseSoup(url: str):
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

class LaptopInfo:
    def __init__(self, name: str, price: float, rating: str):
        self.__name = name
        self.__price = price
        self.__rating = rating

    def __str__(self):
        return (f"Laptop: {self.__name}\nPrice: {self.__price}\nRatings: {self.__rating}")
    
    __rep__ = __str__

class Node:
    def __init__(self, laptop: LaptopInfo):
        self.__value = laptop.__price
        self.__lst = [laptop]
        self.__left = None
        self.__right = None


class BinarySearchTree:
    def __init__(self):
        self.__root = None

    def isEmpty(self):
        return self.__root == None

    def insert(self, laptop: LaptopInfo):
        if self.__root == None:
            self.__root = Node(laptop)
        else:
            self.insertHelper(self.__root, laptop)

    def insertHelper(self, node: Node, laptop: LaptopInfo):
        if laptop.__price < node.__value:
            if node.__left == None:
                node.__left = Node(laptop)
            else:
                self._insertHelper(node.__left, laptop)
        elif laptop.__price == node.__value:
            node.__lst += [laptop]
        else:
            if node.__right == None:
                node.__right = Node(laptop)
            else:
                self._insertHelper(node.__right, laptop)

    def searchByPrice(self, price: float):
        if not self.isEmpty():
            smallestDif = float('inf')
            closestNode = None
            current = self.__root

            while current:
                if price == current.__value:
                    for element in current.__lst:
                        print(element)
                        return
                else:
                    dif = abs(price - current.__value)
                    if dif < smallestDif:
                        smallestDif = dif
                        closestNode = current
                    if price < current.__value:
                        current = current.__left
                    else:
                        current = current.__right
            
            for element in closestNode.__lst:
                print(element)
            
            return

        else:
            return None


    