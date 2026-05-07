import cv2

use_cameras = True
caps = [] # list of available captures
allowed_amounts = [1, 2] # change to allow higher or lower amounts of captures

def setup():
    """ Initiates a user-specified amount of cameras
    
    Args:
        None
    
    Returns:
        None
    """
    global caps

    cap_num = int(input(f"How many cameras will be used? (Max: {allowed_amounts[-1]}) "))
    
    # sets cap_num to 1 if an erroring amount of captures would occur
    if cap_num not in allowed_amounts:
        cap_num = 1 

    # instantiates captures
    for cap in range(cap_num):
        
        caps.append(cv2.VideoCapture(cap))

    
    has_cap = True
    i = 0

    # tests if each camera actually works
    while has_cap and i < len(caps):
        has_cap = caps[i].isOpened()
        i += 1

    caps = caps[:i]

    # alerts user if cameras fail and allows them to restart 
    if len(caps) != cap_num:
        print(f"{len(caps)} of the {cap_num} cameras were able to be instantiated")
        cont = input("Continue anyway? [Y/N] ")
        if cont.lower() != 'y':
            cont = input("Restart camera setup? [Y/N] ")
            if cont.lower() == 'y':
                setup() # redoes camera setup
            else:
                use_cameras = False # stops image detection from continuing
        else:
            print("Continuing to database connection!")
            
    else:
        print(f"{len(caps)} cameras instantiated!")
        print("Continuing to database connection!")

setup()