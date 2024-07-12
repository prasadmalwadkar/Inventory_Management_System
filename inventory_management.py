import json

class Product:
    def __init__(self, id, name, price, quantity): #Constructor of the Product with all the necessary attributes
        self.id = id
        self.name = name
        self.price = price
        self.quantity = quantity

    def __repr__(self):  #return values of the product 
        return f"Product(id={self.id}, name={self.name}, price={self.price}, quantity={self.quantity})"


class Inventory:
    def __init__(self, data_file='inventory.json'): #Constructor of the Inventory class
        self.products = {} #Empty dictionary to store products
        self.data_file = data_file 
        self.load_data()  #Load the data from JSON file

    def add_product(self, product):  #Method to add product in the Inventory system
        if product.id in self.products: #Check if the product Id is already exists in the file
            raise ValueError(f"Product with ID {product.id} already exists.")
        self.products[product.id] = product #If product is not present in the file, Add the product into the system

    def update_product(self, product_id,name,price,quantity):
        if product_id not in self.products: # Check if the product_id exists in the inventory
            raise ValueError(f"Product with ID {product_id} not found.")
        if name:
            self.products[product_id].name = name #Update the name of the product 
        if price is not None:
            self.products[product_id].price = price #Update the price of the product
        if quantity is not None:
            self.products[product_id].quantity = quantity  #Update the quantity of the product

    def delete_product(self, product_id):
        if product_id not in self.products:  #Check if the product_id exists
            raise ValueError(f"Product with ID {product_id} not found.")
        del self.products[product_id] #Delete the product from the inventory

    def view_product(self, product_id):
        return self.products.get(product_id, None) #Return the product if found, otherwise return None

    def list_all_products(self):
        return list(self.products.values()) #Return a list of all product

    def low_stock_alert(self, threshold):
        return [product for product in self.products.values() if product.quantity < threshold] #Return a list of products with quantity below the threshold

    def total_inventory_value(self):
        total_value=0 # Initialize the sum to zero
        for product in self.products.values(): #Iterate 
            total_value+=product.price * product.quantity #Calculate the value of each product
        return total_value

    def load_data(self): #Load data function to load and add the data into the file
        try:
            with open(self.data_file, 'r') as file: #open the file with read accessibilty
                data = json.load(file) #Load the data from the file, which is expected to be in JSON format
                for item in data:
                    product = Product(**item) # The **item unpacks the dictionary into keyword arguments for the Product constructor
                    self.add_product(product) #Add the created Product object to the inventory system
        except (FileNotFoundError): #Throws an error if no file is present. It will create the empty file
            print("No inventory data found.")

    def save_data(self): #to save the data after making changes to the file
        with open(self.data_file, 'w') as file:
            products_list = [vars(product) for product in self.products.values()] #Each product is converted to a dictionary using the vars() function
            json.dump(products_list, file) #Dump the list of product dictionaries to the file in JSON format


def get_valid_input(prompt, input_type=str, condition=None, error_message="Invalid input"): #Check for the valid inputs
    while True:
        try:
            value = input_type(input(prompt)) #Prompt for input and convert it
            if condition and not condition(value):
                raise ValueError()
            return value
        except ValueError:
            print(error_message)

def is_positive(value):
    return value > 0

def main():
    inventory = Inventory() # Initialize Inventory object

    menu = """
    1. Add Product
    2. Update Product
    3. Delete Product
    4. View Product
    5. List All Products
    6. Low-Stock Alert
    7. Total Inventory Value
    8. Exit
    """
    while True:  # Enter an infinite loop to continuously display the menu
        print(menu)
        choice = get_valid_input("Choose an option: ", int, lambda x: 1 <= x <= 8, "Please enter a number between 1 and 8.") # Get a valid input from the user for the menu choice

        if choice == 1: #Add Product
            product_id = input("Product ID: ")
            name = input("Product name: ")
            price = get_valid_input("Product price: ", float, is_positive, "Enter a positive number.") #Number check
            quantity = get_valid_input("Quantity: ", int, is_positive, "Enter a positive integer.") #Number check
           
            try:
                product = Product(product_id, name, price, quantity)
                inventory.add_product(product) 
                print("Product added successfully.")
            except ValueError as e:
                print(e)

        elif choice == 2: #Update the product
            product_id = input("Product ID to update: ") #New product details
            name = input("New name : ")
            price = input("New price : ")
            quantity = input("New quantity : ")
            try:
                inventory.update_product(
                    product_id,
                    name,
                    float(price),
                    int(quantity), 
                )
                print("Product updated successfully.")
            except ValueError as e:
                print(e)

        elif choice == 3: #Delete the product ID
            product_id = input("Product ID to delete: ")
            try:
                inventory.delete_product(product_id)
                print("Product deleted successfully.")
            except ValueError as e:
                print(e)

        elif choice == 4: #Shwo products
            product_id = input("ID to view: ")
            product = inventory.view_product(product_id)
            if product:
                print(product)
            else:
                print("Product not found.")

        elif choice == 5: #List all the products in inventory
            products = inventory.list_all_products()
            if products:
                for product in products:
                    print(product)
            else:
                print("No products in inventory.")

        elif choice == 6: #Low stock products
            threshold = 2 #I have set the threshold as 2
            products = inventory.low_stock_alert(threshold)
            if products:
                for product in products:
                    print(product)
            else:
                print("No products below the threshold.")

        elif choice == 7: #Total current Inventory Value
            total=inventory.total_inventory_value()
            print(f"Total Inventory Value: {total}" )

        elif choice == 8: #Save the data into Json and exit
            inventory.save_data()
            print("Inventory data saved.")
            break

if __name__ == '__main__':
    main()
