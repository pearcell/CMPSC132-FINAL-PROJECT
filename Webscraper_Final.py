from bs4 import BeautifulSoup
import requests

URL = 'https://www.newegg.com/p/pl?d=laptop'

def parseSoup(url: str) -> BinarySearchTree:
    page = requests.get(url)
    print(page)
    soup = BeautifulSoup(page.text, "html.parser")
    products = soup.find_all("div", class_ = "item-container position-relative")

    bst = BinarySearchTree()

    if products == None:
        print(page)
        return "Request failed"
    else:
        for item in products:
            name = item.find("a", class_ = "item-title")
            name_s = name.text.strip()
            
            price = item.find("li", class_ = "price-current")
            price_s = price.text.strip("\u2013").strip()
            price_f = float(("".join(price_s.split(","))).strip("$"))

            rating = item.find("a", class_ = "item-rating")
            if rating != None:
                rating = rating.find("i")
                rating_s = rating["aria-label"].strip("rated").strip()
            else:
                rating_s = None

            print(f"Laptop: {name_s}") 
            print(f"Price: {price_s}")
            print(f"Ratings: {rating_s}")
            print("\n")

            laptopInfo = LaptopInfo(name_s, price_f, rating_s)
            bst.insert(laptopInfo)

    return bst

class LaptopInfo:
    def __init__(self, name: str, price: float, rating: str):
        self._name = name
        self._price = price
        self._rating = rating

    def __str__(self):
        return (f"Laptop: {self._name}\nPrice: {self._price}\nRatings: {self._rating}")
    
    __rep__ = __str__

class Node:
    def __init__(self, laptop: LaptopInfo):
        self._value = laptop._price
        self._lst = [laptop]
        self._left = None
        self._right = None


class BinarySearchTree:
    def __init__(self):
        self._root = None

    def isEmpty(self):
        return self._root == None

    def insert(self, laptop: LaptopInfo):
        if self._root == None:
            self._root = Node(laptop)
        else:
            self.insertHelper(self._root, laptop)

    def insertHelper(self, node: Node, laptop: LaptopInfo):
        if laptop._price < node._value:
            if node._left == None:
                node._left = Node(laptop)
            else:
                self.insertHelper(node._left, laptop)
        elif laptop._price == node._value:
            node._lst += [laptop]
        else:
            if node._right == None:
                node._right = Node(laptop)
            else:
                self.insertHelper(node._right, laptop)

    def searchByPrice(self, price: float):
        if not self.isEmpty():
            smallestDif = float('inf')
            closestNode = None
            current = self._root

            while current:
                if price == current._value:
                    for element in current._lst:
                        print(element)
                        return
                else:
                    dif = abs(price - current._value)
                    if dif < smallestDif:
                        smallestDif = dif
                        closestNode = current
                    if price < current._value:
                        current = current._left
                    else:
                        current = current._right
            
            for element in closestNode._lst:
                print(element)
            
            return

        else:
            return None
        
def main():
    print("Type 'exit' to terminate program\nType 'run' to run webscraper/fetch laptop data\nType 'search' to search by price")
    running = True
    bst = None

    while running:
        print("\n")
        i = input("")
        if i == "exit":
            running = False
        elif i == "run":
            bst = parseSoup(URL)
        elif i == "search":
            if bst == None:
                print("Type 'run' first before searching")
            else:
                try:
                    pr = float(input("Type price: $"))
                    if pr > 0:
                        "Laptop(s) with closest price:"
                        bst.searchByPrice(pr)
                    else:
                        print("Input invalid")
                except ValueError:
                    print("Input invalid")
        else:
            print("Input invalid")

    print("Session ended")


main()
    