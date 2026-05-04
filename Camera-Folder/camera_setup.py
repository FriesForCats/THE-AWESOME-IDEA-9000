import cv2

use_cameras = True
caps = []
allowed_amounts = [1, 2] # change to allow higher or lower amounts of captures

def setup():
    global caps

    cap_num = int(input(f"How many cameras will be used? (Max: {allowed_amounts[-1]}) "))
    
    if cap_num not in allowed_amounts:
        cap_num = 1

    for cap in range(cap_num):
        
        caps.append(cv2.VideoCapture(cap))

    has_cap = True
    i = 0

    while has_cap and i < len(caps):
        has_cap = caps[i].isOpened()
        i += 1

    caps = caps[:i]

    if len(caps) != cap_num:
        print(f"{len(caps)} of the {cap_num} cameras were able to be instantiated")
        cont = input("Continue anyway? [Y/N] ")
        if cont.lower() != 'y':
            use_cameras = False
        else:
            print("Continuing to database connection!")
    else:
        print(f"{len(caps)} cameras instantiated!")
        print("Continuing to database connection!")

setup()