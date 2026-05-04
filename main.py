#booring
import sys
import subprocess
import os
import time  # 1. Import the time module

# 2. Define paths
gui_path = os.path.join("GUI-Folder", "my-app")
config_path = os.path.join("Camera-Folder", "config.py")

print("Starting GUI...")
subprocess.Popen(["npm", "start"], cwd=gui_path, shell=True)

print("Running config...")
subprocess.Popen([sys.executable, config_path])

# 3. Add the delay here
# This gives the background processes time to breathe
print("Waiting 5 seconds for systems to initialize...")
time.sleep(5) 

# 4. Existing logic
sys.path.append("Camera-Folder")
import camera_setup

# Since camera_setup has an input(), the terminal will pause here
# after the 5-second delay.
camera_setup.setup()

import camera_second_try
if camera_setup.use_cameras:
    camera_second_try.videoPlay()