# FILE DOES NOT RELATE TO CODE, ONLY USED AS A DEMO
# an example of if we had a checkout to work with and a shopper was dishonest


cart = []

amount = int(input("How many items are in your cart? "))

for i in range(amount):
    cart.append(input(f"What is item {i+1}? "))
    
print("Your cart does not match the database, an alert has been sent.")