#booring
import sys
import subprocess  # Added for separate process handling
import os          # Added for path management

# Existing path setup
sys.path.append("Camera-Folder")

# --- Run config.py as a SEPARATE PROCESS ---
# We use sys.executable to ensure we use the same Python version
config_path = os.path.join("Camera-Folder", "config.py")
subprocess.Popen([sys.executable, config_path])

# --- Existing imports and logic ---
import camera_setup
camera_setup.setup()

import camera_second_try

if camera_setup.use_cameras:
    camera_second_try.videoPlay()