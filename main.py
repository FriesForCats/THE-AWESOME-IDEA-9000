#boooring
import sys

sys.path.append("Camera-Folder")

import camera_setup

camera_setup.setup()

import camera_first_try

if camera_setup.use_cameras:
    camera_first_try.videoPlay()