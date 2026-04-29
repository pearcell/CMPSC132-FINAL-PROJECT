from bs4 import BeautifulSoup
import requests

URL = 'https://www.newegg.com/p/pl?d=laptop'

# parseSoup() retrieves the laptop data and inserts it into a BST
def parseSoup(url: str) -> BinarySearchTree:
    # Retrieve HTML and create BeautifulSoup object for parsing
    page = requests.get(url)
    print(page)
    soup = BeautifulSoup(page.text, "html.parser")
    # Parse soup; products is a list containing the HTML blocks which correspond to each laptop
    products = soup.find_all("div", class_ = "item-container position-relative")

    bst = BinarySearchTree()

    # Check for failed retrieval
    if products == None:
        print(page)
        return "Request failed"
    else:
        # Iterate through products
        for item in products:
            # Parse and format laptop name
            name = item.find("a", class_ = "item-title")
            name_s = name.text.strip()
            
            # Parse and format laptop price
            price = item.find("li", class_ = "price-current")
            price_s = price.text.strip("\u2013").strip()
            price_f = float(("".join(price_s.split(","))).strip("$"))

            # Parse and format laptop rating
            rating = item.find("a", class_ = "item-rating")
            if rating != None:
                rating = rating.find("i")
                rating_s = rating["aria-label"].strip("rated").strip()
            else:
                rating_s = None

            # Print laptop data
            print(f"Laptop: {name_s}") 
            print(f"Price: {price_s}")
            print(f"Ratings: {rating_s}")
            print("\n")

            # Create LaptopInfo object (for each laptop/once each loop) and insert it into the BST
            laptopInfo = LaptopInfo(name_s, price_f, rating_s)
            bst.insert(laptopInfo)

    return bst

# LaptopInfo contains the laptop data
class LaptopInfo:
    def __init__(self, name: str, price: float, rating: str):
        self._name = name
        self._price = price
        self._rating = rating

    def __str__(self):
        return (f"Laptop: {self._name}\nPrice: {self._price}\nRatings: {self._rating}")
    
    __rep__ = __str__

# Node class for BST implementation
class Node:
    def __init__(self, laptop: LaptopInfo):
        # Value for comparisons is the input laptops associated _price
        self._value = laptop._price
        # LaptopInfo object itself is stored in the node as part of a list to allow for insertion of laptops with the same price
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

    # Recursive insert helper function
    def insertHelper(self, node: Node, laptop: LaptopInfo):
        if laptop._price < node._value:
            if node._left == None:
                node._left = Node(laptop)
            else:
                self.insertHelper(node._left, laptop)
        # When current node price == the price of the laptop being inserted, the laptop is simply concatenated at the end of the current nodes _lst attribute
        elif laptop._price == node._value:
            node._lst += [laptop]
        else:
            if node._right == None:
                node._right = Node(laptop)
            else:
                self.insertHelper(node._right, laptop)

    # Searches by price; returns the laptop with the price closest to the input price
    def searchByPrice(self, price: float):
        if not self.isEmpty():
            # Float initialized to infity; during the search it will be always hold the value of the difference between the price of the node with a price closest to the desired price and the desired price itself
            smallestDif = float('inf')
            # closestNode always points to the node with a price value closest to the desired price; reassigned based on the smallestDif comparison
            closestNode = None
            current = self._root

            # Traverse list moving to right if current value if smaller than desired price and left if current value is greater than desired price
            while current:
                if price == current._value:
                    # If a node price matches the desired price all laptops associated with the _lst attribute of that node are printed
                    for element in current._lst:
                        print(element)
                        print("\n")
                        return
                else:
                    # dif is absolute value of difference between desired price and current node's price
                    dif = abs(price - current._value)
                    # if the current dif is smaller than the smallestDif it becomes the new smallestDif and its node becomes the new closestNode
                    if dif < smallestDif:
                        smallestDif = dif
                        closestNode = current
                    if price < current._value:
                        current = current._left
                    else:
                        current = current._right
            
            # In the case that no price matches the desired price all laptops associated with the _lst attribute with the closest price to the desired price are printed
            for element in closestNode._lst:
                print("\n")
                print(element)
            
            return

        else:
            return None
        
# Implementation of user input side of program
def main():
    # Lists commands/instructions
    print("Type 'exit' to terminate program\nType 'run' to run webscraper/fetch laptop data\nType 'search' to search by price")
    running = True
    bst = None

    # Loop ends when "exit" is input and running is set to False
    while running:
        print("\n")
        i = input("")
        if i == "exit":
            # Terminates program
            running = False
        elif i == "run":
            # Populates BST
            bst = parseSoup(URL)
        elif i == "search":
            # Requires BST to be populated/"run" to be executed before searching
            if bst == None:
                print("Type 'run' first before searching")
            else:
                # Prompts user to input price; if input is valid returns laptop(s) closest to input price
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
    