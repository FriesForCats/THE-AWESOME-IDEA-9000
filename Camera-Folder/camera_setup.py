import cv2

use_cameras = True
caps = []

def setup():
    global caps

    cap_num = int(input("How many cameras will be used? "))
    

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