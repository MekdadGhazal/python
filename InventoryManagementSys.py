
# Inventory Management System

import sys

class Product:

    def __init__(self, name, price, quantity):
        if not isinstance(price, float) or price < 0:
            raise ValueError("Input must be an float.")
        
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("Input must be an integer.")
        
        self.name = name
        self.price = float(price)
        self.quantity = quantity


    def display(self):
        return f"Product: {self.name}, Price: {self.price}, Quantity: {self.quantity}"

    def __str__(self):
        return f"Product: {self.name}, Price: {self.price}, Quantity: {self.quantity}"
    
    def update_quantity(self, amount: int):
        if self.quantity + amount < 0:
            raise ValueError(f"Cannot reduce quantity below zero. Current stock: {self.quantity}")
        self.quantity += amount
        print(f"Updated quantity for {self.name}. New quantity: {self.quantity}")



class Inventory:

    def __init__(self):
        self.products = []

    def add_product(self, new_product : Product) :
        for product in self.products:
            if product.name == new_product.name:
                print(f"Info: Product '{new_product.name}' already exists in the inventory.")
                return
            
        self.products.append(new_product)
        print(f"Success: Product '{new_product.name}' added to inventory.")
            

    def find_product(self, product_name) :
        if not isinstance(product_name, str):
            raise ValueError("Input must be an String.")
        
        for product in self.products :
            if product.name == product_name :
                return product
        
        return None
    
    # def display_inventory(self):
    #     if not self.products :
    #         return "Storage Empty!"
        
    #     return self.products

    def display_inventory(self):

        print("\n--- Current Inventory ---")

        if not self.products:
            print("The inventory is currently empty.")
        else:
            for product in self.products:
                print(product)
        print("-------------------------\n")
    


def print_menu():
    """Prints the main menu for the user."""
    print("\n--- Inventory Management System ---")
    print("1. Add a new product")
    print("2. Display all products")
    print("3. Find a product by name")
    print("4. Update a product's quantity")
    print("5. Exit")
    print("-----------------------------------")

def main():
    """Main function to run the interactive inventory system."""
    inventory = Inventory()

    while True:
        print_menu()
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            # Add a new product
            try:
                name = input("Enter product name: ")
                price = float(input("Enter product price: "))
                quantity = int(input("Enter product quantity: "))
                product = Product(name, price, quantity)
                inventory.add_product(product)
            except ValueError as e:
                print(f"\nInvalid input: {e}. Please try again.")

        elif choice == '2':
            # Display all products
            inventory.display_inventory()

        elif choice == '3':
            # Find a product
            name = input("Enter the name of the product to find: ")
            product = inventory.find_product(name)
            if product:
                print("\nProduct Found:")
                print(product)
            else:
                print(f"\nProduct '{name}' not found.")

        elif choice == '4':
            # Update quantity
            name = input("Enter the name of the product to update: ")
            product = inventory.find_product(name)
            if product:
                try:
                    amount = int(input("Enter amount to add/remove (e.g., 10 or -5): "))
                    product.update_quantity(amount)
                except ValueError:
                    print("\nInvalid input. Please enter a valid integer for the amount.")
            else:
                print(f"\nProduct '{name}' not found.")

        elif choice == '5':
            # Exit
            print("\nGoodbye!")
            sys.exit()

        else:
            print("\nInvalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()
