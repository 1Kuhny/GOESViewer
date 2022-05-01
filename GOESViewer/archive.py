'''

This archives the "Today" Folder 
- Copies the folder
- Saves it as what would then be yesterdays date
- Deletes now old today folder
- Creates a new blank today folder that has all of the needed blank image files for sequence loop

'''

import os
import shutil
import time
from datetime import date

# Make this true if you want to test the program immediately 
# THIS WILL EFFECT and MOVE FILES
# Make a back up of your 'Today Folder' before running
# Should be False for normal operation
testRun = False




if testRun:
    # This will force immediate run
    lastDay = 0
else:
    # Record last date as today so that the program doesn't run immediately
    lastDay = date.today().day



print("Started")

while True:

    # No sense in checking as quick as possible for the date change, delay for 10 seconds
    time.sleep(10)

    # Wait until the day changes to back up.
    if lastDay != date.today().day:

        print("Backing Up")
        src_dir = 'Today'
 
        # The new folder name will be the date of (what would be) yesterday
        dest_dir = str(lastDate)
 
        # Get all Folders in the 'Today' Folder
        files = os.listdir(src_dir)
        print("Copying Files")
        shutil.copytree(src_dir, dest_dir)
        print("Removing Images from Today Folder")
        shutil.rmtree(src_dir)
        print("Creating new Today Folder")
        shutil.copytree('EmptyFolders', 'Today')

        # Record the day, so we can detect the next day change.
        lastDay = date.today().day
        # Record the date string so it can be used to create the next back up
        lastDate = date.today()