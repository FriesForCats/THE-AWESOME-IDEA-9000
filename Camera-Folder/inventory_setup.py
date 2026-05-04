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
    
cursor.execute("SELECT COUNT(*) FROM inventory")
count = cursor.fetchone()[0]

def inv_setup(count):

    if count != 0:
        to_delete = input("Would you like to use previous data?[Y/N] ")
        if to_delete.lower() == 'n':
            print("Removing previous item labels and amounts...")
            cursor.execute("TRUNCATE TABLE inventory")
            db.commit()
            count = 0
            
    if count == 0:        
        
        num_labels = int(input("How many different items are available in store? "))

        labels = []
        amounts = []
        inventory = []

        for i in range(num_labels):
            labels.append(input(f"What is item {i+1}? "))
            amounts.append(input(f"How many {labels[i]}s are available? "))
            
        for i in range(num_labels):
            inventory.append((labels[i], amounts[i]))
            

        print("Your store has:")

        for i in range(num_labels):
            if amounts[i] == 1:
                    print(f"1 {labels[i]}")
            else:
                    print(f"{amounts[i]} {labels[i]}s")
                    
        check = input("Are these values correct? [Y/N] ")

        if check.lower() == 'y':
            try:
                sql = "INSERT INTO inventory (label, amount ) VALUES (%s, %s)"
                cursor.executemany(sql, inventory)
                db.commit()
                
            except mysql.connector.Error as e:
                print(f"Logging error: {e}")
        else: 
            inv_setup(0)
            
inv_setup(count)
                

