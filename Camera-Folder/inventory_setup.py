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
    # print("Successfully connected to the database!")
    
except mysql.connector.Error as err:
    print(f"Database Connection Error: {err}")
    sys.exit()
    
cursor.execute("SELECT COUNT(*) FROM inventory") # Selects all rows
count = cursor.fetchone()[0] # checks if at least 1 row exists

def inv_setup(count):
    """ Prompts user for use of previous storage then creates a new inventory of items and amounts if no inventory is available or user chooses to delete previous data
    
    Args:  
        count: Checks if rows of data exist
    
    Returns:
        None
    """

    # checks for previous data
    if count != 0:
        to_delete = input("Would you like to use previous data?[Y/N] ") 
        if to_delete.lower() == 'n':
            to_delete = input("Are you sure you wish to delete all previous data? This is irreversible. [Y/N] ")
            if to_delete.lower() == 'y':
                print("Removing previous item labels and amounts...")
                cursor.execute("TRUNCATE TABLE inventory") # deletes previously stored data
                db.commit()
                count = 0 # sets count to 0 after deleting
    
    
    if count == 0:   # no items in inventory      
        
        num_labels = int(input("How many different items are available in store? "))

        labels = []
        amounts = [] 
        inventory = []

        for i in range(num_labels): # prompts user for each item
            labels.append(input(f"What is item {i+1}? "))
            amounts.append(input(f"How many {labels[i]}s are available? "))
            
        for i in range(num_labels):
            inventory.append((labels[i], amounts[i]))
            
        # allows user to check inventory to make sure its correct
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
            inv_setup(0) # redoes setup if inventory is incorrect
            
inv_setup(count)
                

