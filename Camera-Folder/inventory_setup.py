import mysql.connector
import sys
import warnings

# DATABASE CONNECTION 
try:
    db = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="password", # very secure password
        database="vision_project",
        port=3306
    )
    cursor = db.cursor()
    print("Successfully connected to the database!")
    
except mysql.connector.Error as err:
    print(f"Database Connection Error: {err}")
    sys.exit()
    
num_labels = input("How many different items are available in store? ")

labels = []
amounts = []
inventory = []

for label in range(num_labels):
    labels[label] = input(f"What is item {label}? ")
    amounts[label] = input(f"How many {labels[label]}s are available? ")
    
for i in range(num_labels):
    inventory.append((label[i], amounts[i]))
    

print("Your store has:")

for i in range(num_labels):
    if amounts[i] == 1:
            print(f"1 {labels[i]}")
    else:
            print(f"{amounts[i]} {labels[i]}s")
            
check = input("Are these values correct? [Y/N] ")

if check.lower() == 'y':
    
    for label, amount in inventory:

        try:
            sql = "INSERT INTO inventory (label, amount ) VALUES (%s, %s)"
            cursor.execute(sql, (item_name, float(item[4]), "HELD"))
            db.commit()

            last_logged_time[item_name] = current_time
            print(f"Database Updated: {item_name}")
        except mysql.connector.Error as e:
            print(f"Logging error: {e}")
                    
    
