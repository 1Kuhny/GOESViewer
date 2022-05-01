'''

This file sorter is important for the processing program

Every 10 seconds, this will look at the directory specified for images
If it finds any it will split the file name up to figure out where it needs to go.

Since the process is the same for all views, only one is commented

I only have one Custom Meso, so if you need more feel free to add them, should be copy and paste for the most part. 
You will need to change the folder paths and create the needed blank image files and folders.

'''

import os
import shutil
import time

enhancedImage =True

# This is your image folder name. Keep in mind, this python program needs to be in the folder just before the image folder you specify here.
# You could technically change all of the file paths and get this to still work, but for ease of use, set your image output to point to the GOESImages folder.
directory = "GOESImages" 
# The file format of your images
fileFormat = ".jpg"

# This controls how many images are shifted. Needed for image looping.
# Increasing this to insane numbers will slow the sorter over all.
# You will also need to add more blank images so the program doesn't try and shift images that don't exist (explained more in the README)
maxLoopedImages = 20

#Should We create Blank Images?
# Leave this on. If the program gets shut down mid transfer, there is a chance that you can lose files in the sequence and the sorter WILL run into issues.
# This will wipe all images in the image buffer sequence (other sorted images will still be there) but this will atleast fix any issues automatically.
# However, if you are able to interperate what files are missing based off of the error messages. You can set this to false, restart the program and then copy and paste new blanks or other surrounding images. Just be sure to name copied image to the one it says that it cant find.
createBlanks = True

# How often should the program search the main image folder (in seconds)
timeBetweenSearch = 10

# Store the images in the respective bands
StoreImages = True;

products = ["FSCLR", "IR(3.9)", "IR(6.2)", "IR(6.9)", "IR(10.3)", "IR(11.2)", "IR(12.3)", "VIS(0.64)"]

if createBlanks:
    print("Creating Blanks...")
    #Loop though all products and place the blank files. The blank files are listed in the "BlankFolder" folder
    for i in range(maxLoopedImages):
        for d in range(8):

            shutil.copy("GOESViewer/EmptyFolders/blank" + fileFormat, "GOESViewer/MostRecentFullDisk/"+ products[d] +"/" + str(i) + ".jpg")   
            shutil.copy("GOESViewer/EmptyFolders/blank" + fileFormat, "GOESViewer/MostRecentCONUS/"+ products[d] +"/" + str(i) + ".jpg") 
            shutil.copy("GOESViewer/EmptyFolders/blank" + fileFormat, "GOESViewer/MostRecentMESOA/"+ products[d] +"/" + str(i) + ".jpg")
            shutil.copy("GOESViewer/EmptyFolders/blank" + fileFormat, "GOESViewer/MostRecentMeso/M1/"+ products[d] +"/" + str(i) + ".jpg")
            shutil.copy("GOESViewer/EmptyFolders/blank" + fileFormat, "GOESViewer/MostRecentMeso/M2/"+ products[d] +"/" + str(i) + ".jpg")

            shutil.copy("GOESViewer/EmptyFolders/blank" + fileFormat, "GOESViewer/MostRecentFullDisk/"+ products[d] +"/Enhanced/" + str(i) + ".jpg")   
            shutil.copy("GOESViewer/EmptyFolders/blank" + fileFormat, "GOESViewer/MostRecentCONUS/"+ products[d] +"/Enhanced/" + str(i) + ".jpg") 
            shutil.copy("GOESViewer/EmptyFolders/blank" + fileFormat, "GOESViewer/MostRecentMESOA/"+ products[d] +"/Enhanced/" + str(i) + ".jpg")
            shutil.copy("GOESViewer/EmptyFolders/blank" + fileFormat, "GOESViewer/MostRecentMeso/M1/"+ products[d] +"/Enhanced/" + str(i) + ".jpg")
            shutil.copy("GOESViewer/EmptyFolders/blank" + fileFormat, "GOESViewer/MostRecentMeso/M2/"+ products[d] +"/Enhanced/" + str(i) + ".jpg")

    print("Done")


while True:
    
    try:
        # for each file in the directory
        for filename in os.listdir(directory):
            # Find all images that end with the correct extension (format)
            if filename.endswith(fileFormat): 

                # Grab the file name
                fileName = os.path.join(directory, filename)
                # Split the file name up
                newFileName = fileName.split("-")

                print("Moving File:" + fileName)

                # Check if the image is an enhanced verison
                if newFileName[3] == "e":
                    enhancedImage = True
                else:
                    enhancedImage = False





                # Full Disk Image Sorting
                if(newFileName[1] == "Full Disk"):
                
                    # Find the Channele Name (IR Wavelength)
                    dest = newFileName[2]

                    if enhancedImage == False:

                        # Contingency. For some reason I have gotten images that have no band or ID name, so this detects that. This isn't needed for CONUS or Mesos
                        if dest != "":

                            # This is the shifter for the loop function. Start at the oldest image and then set it to the image before it. Ex 9 is now 8, 8 is now 7, 7 is now 6 etc. 
                            # Do this for all until you hit image 0 (most recent). Once image 1 is set to image 0, 0 is deleted. Yes the sleep is necessary, if you dont, the shiting process goes out of sync and the program will stop.
                            for i in reversed(range(1,maxLoopedImages)):
                                os.replace("GOESViewer/MostRecentFullDisk/"+ dest + "/" + str(i-1) + fileFormat, "GOESViewer/MostRecentFullDisk/"+ dest + "/" + str(i) + fileFormat)
                                time.sleep(.5)

                            
                            time.sleep(.25)
                            # Finally, we are going to copy the file that we are currently sorting. This will send it over and replace the image 0 we removed in the shifting proccess.
                            shutil.copy(os.path.join(directory, filename), "GOESViewer/MostRecentFullDisk/"+ dest +"/0" + fileFormat)
                            time.sleep(.25)
                            # After we replaced 0 we no longer need it in our bulk image folder. Move it to the proper band folder which deletes it out of the bulk image folder
                            
                            # If we want to store the images, move it, if not, delete it
                            if StoreImages:
                                shutil.move(os.path.join(directory, filename), "GOESViewer/FullDisk/"+dest+"/" + filename)
                            else:
                                os.remove(os.path.join(directory, filename))

                        # Contingency Handling. If it detected as un-sortable, move it to the 'Other' folder located in the FullDiskFolder
                        else:
                            print("Image not sortable, moving to Other")
                            if StoreImages:
                               shutil.move(os.path.join(directory, filename), "GOESViewer/FullDisk/Other/" + filename)
                            else:
                                os.remove(os.path.join(directory, filename))

                    
                    else:
                        # This sorts the enhanced images so they are kept seperate. These are the ones used in the processing program. For the most part, this is identical to the above code.
                        if dest != "":
                            
                            for i in reversed(range(1,maxLoopedImages)):
                                os.replace("GOESViewer/MostRecentFullDisk/"+ dest + "/Enhanced/" + str(i-1) + fileFormat, "GOESViewer/MostRecentFullDisk/"+ dest + "/Enhanced/" + str(i) + fileFormat)
                                time.sleep(.5)

                            time.sleep(.25)
                            shutil.copy(os.path.join(directory, filename), "GOESViewer/MostRecentFullDisk/"+ dest +"/Enhanced/0" + fileFormat)
                            time.sleep(.25)
                            if StoreImages:
                                shutil.move(os.path.join(directory, filename), "GOESViewer/Today/FullDisk/" + dest + "/Enhanced/"+ filename)
                            else:
                                os.remove(os.path.join(directory, filename))

                        else:
                            print("Image not sortable, moving to Other")
                            if StoreImages:
                                shutil.move(os.path.join(directory, filename), "GOESViewer/Today/FullDisk/Other/" + filename)
                            else:
                                os.remove(os.path.join(directory, filename))
                
                            



                # CONUS Image Sorting
                if(newFileName[1] == "CMeso_CONUS"):


                    dest = newFileName[2]

                    if enhancedImage == False:

                        for i in reversed(range(1,maxLoopedImages)):
                            os.replace("GOESViewer/MostRecentCONUS/"+ dest + "/" + str(i-1) + fileFormat, "GOESViewer/MostRecentCONUS/"+ dest + "/" + str(i) + fileFormat)
                            time.sleep(.5)

                        time.sleep(.25)
                        shutil.copy(os.path.join(directory, filename), "GOESViewer/MostRecentCONUS/"+ dest +"/0" + fileFormat)
                        time.sleep(.25)
                        if StoreImages:
                            shutil.move(os.path.join(directory, filename), "GOESViewer/Today/CONUS/"+ dest +"/"+ filename)
                        else:
                            os.remove(os.path.join(directory, filename))

                    else:

                        for i in reversed(range(1,maxLoopedImages)):
                            os.replace("GOESViewer/Today/MostRecentCONUS/"+ dest + "/Enhanced/" + str(i-1) + fileFormat, "GOESViewer/MostRecentCONUS/"+ dest + "/Enhanced/" + str(i) + fileFormat)
                            time.sleep(.5)

                        time.sleep(.25)
                        shutil.copy(os.path.join(directory, filename), "GOESViewer/MostRecentCONUS/"+ dest +"/Enhanced/0" + fileFormat)
                        time.sleep(.25)
                        if StoreImages:
                            shutil.move(os.path.join(directory, filename), "GOESViewer/Today/CONUS/" + dest + "/Enhanced/"+ filename)
                        else:
                            os.remove(os.path.join(directory, filename))







                # Mesoscale Image Sorting for both M1 and M2
                if(newFileName[1] == "Mesoscale"):

                    

                    if newFileName[3] == "M1" or newFileName[4] == "M1":
                        destOne = "M1"
                    elif newFileName[3] == "M2" or newFileName[4] == "M2":
                        destOne = "M2"

                    destTwo = newFileName[2]

                    if enhancedImage == False:
                    

                        for i in reversed(range(1,maxLoopedImages)):
                            os.replace("GOESViewer/MostRecentMeso/"+ destOne + "/" + destTwo +"/" + str(i-1) + fileFormat, "GOESViewer/MostRecentMeso/"+ destOne + "/" + destTwo +"/" + str(i) + fileFormat)
                            time.sleep(.5)

                        time.sleep(.25)
                        shutil.copy(os.path.join(directory, filename), "GOESViewer/MostRecentMeso/"+ destOne + "/" + destTwo +"/0" + fileFormat)
                        time.sleep(.25)
                        if StoreImages:
                            shutil.move(os.path.join(directory, filename), "GOESViewer/Today/Mesoscale/"+destOne+"/" + destTwo + "/" + filename)
                        else:
                            os.remove(os.path.join(directory, filename))

                    else:

                        for i in reversed(range(1,maxLoopedImages)):
                            os.replace("GOESViewer/MostRecentMeso/"+ destOne + "/" + destTwo + "/Enhanced/" + str(i-1) + fileFormat, "GOESViewer/MostRecentMeso/"+ destOne + "/" + destTwo + "/Enhanced/" + str(i) + fileFormat)
                            time.sleep(.5)
                        
                        time.sleep(.25)
                        shutil.copy(os.path.join(directory, filename), "GOESViewer/MostRecentMeso/"+ destOne + "/" + destTwo +"/Enhanced/0" + fileFormat)
                        time.sleep(.25)
                        if StoreImages:
                            shutil.move(os.path.join(directory, filename), "GOESViewer/Today/Mesoscale/"+destOne+"/" + destTwo + "/Enhanced/"+ filename)
                        else:
                            os.remove(os.path.join(directory, filename))








                if(newFileName[1] == "CMeso_A"):


                    if enhancedImage == False:



                        dest = newFileName[2]

                        for i in reversed(range(1,maxLoopedImages)):
                            os.replace("GOESViewer/MostRecentMESOA/"+ dest + "/" + str(i-1) + fileFormat, "GOESViewer/MostRecentMESOA/"+ dest + "/" + str(i) + fileFormat)
                            time.sleep(.5)

                        time.sleep(.25)
                        shutil.copy(os.path.join(directory, filename), "GOESViewer/MostRecentMESOA/"+ dest +"/0" + fileFormat)
                        time.sleep(.25)
                        shutil.move(os.path.join(directory, filename), "GOESViewer/Today/MESOA/"+dest+"/" + filename)

                    else:

                        dest = newFileName[2]

                        
                        for i in reversed(range(1,maxLoopedImages)):
                            os.replace("GOESViewer/MostRecentMESOA/"+ dest + "/Enhanced/" + str(i-1) + fileFormat, "GOESViewer/MostRecentMESOA/"+ dest + "/Enhanced/" + str(i) + fileFormat)
                            time.sleep(.5)

                        time.sleep(.25)
                        shutil.copy(os.path.join(directory, filename), "GOESViewer/MostRecentMESOA/"+ dest +"/Enhanced/0" + fileFormat)
                        time.sleep(.25)
                        if StoreImages:
                            shutil.move(os.path.join(directory, filename), "GOESViewer/Today/MESOA/" + dest + "/Enhanced/"+ filename)
                        else:
                            os.remove(os.path.join(directory, filename))

                continue
            else:
                continue
            time.sleep(timeBetweenSearch)
    except Exception as e:
        print(e)
        time.sleep(10)
        