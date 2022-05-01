
########## THIS CODE IS EXPERIMENTAL, MAKE A BACK UP OF YOUR IMAGES ###########


Prerequisites
- Install Python. Anaconda is recommended.
https://www.anaconda.com/products/distribution?gclid=Cj0KCQjwvLOTBhCJARIsACVldV21gCtwWYyxqvIEVWwF0NLjoCvp__YOVxMHDd3Bh9hz8-Du1m4pF80aAv2bEALw_wcB
- Add Python to system path variables.
- No other libraries needed.

- Install Processing
https://processing.org/download

- Optional but highly recmmended.
  - Move the autoDel.bat and autoDelete.py to the folder that is before the folder that contains the LRIT files (in my case, this program is put in output/Images)
  - This autodelete program will make sure that the image processor does not continue to output the same image over and over again. Which will cause the sequence to display the same image over and over again.
  - My reception is not overly great so this could be why the image processor I use does not delete the LRIT files properly

#################### Sorter ##########################

To get this set up without having to change any major part of the program:



1.  Go into what ever program you are using for generating the images, and tell it to place all images in the GOESImages Folder

2.  Open the sort.py using the included editor that is installed by python (usually IDLE), or by using notepad (not recommended due to indentation issues).

3.  Configure the settings that you want. Mainly what fileFormat (can be anything really, but .jpg is default), timeBetweenSearch (how often the proram searches the main image folder), maxLoopedImages (this will tell the program how many blank images to create and then later shift), and StoreImages which tells the program if it should store images in the correct folders after shifting or just delete them (default is to store them)

4. Run the runFileTransfer.bat to start the sorter



##### The sorter should be running at this point #####



5. It should say "Creating Blanks". This may or may not take a long time depending on how many images you set to loop. This is it making the place holder images so that the sorter has images to shift and wont run into issues.

6. After the blanks are created, it will start looking for images in the GOESImages Folder (delay between checks is set by the timeBetweenSearch variable)

7. Once it finds an image, it will split the file name up to figure out what it is and where it should go.

8. It will then shift the image sequence, delete the oldest one (more of an overwrite) and then copy the image that it found, into the 0 position.

9. If told to do so, it will then move the image from the main GOESImages folder to the correct view and then to the correct band. Otherwise it will just be deleted.


################## Processing #######################


10.  Next, go into the prossing sketch (GOESViewer.pde)

11. Go through the top variables and configure them to your needs

12. Set your resolution by commenting/uncommenting it on lines 89 and 90 (The one uncommented by default is 1080p, the other is 2k)

13. Run the script by pressing the play button at the top or by pressing CTRL+R

14 Finally, if everything runs good, you can complile it and run standalone by going to File->Export Application and then click Export





#################### Extra #########################

If you need an image archiver, I have included one. It is located in the GOESViewer Folder (archive.py). More details in the programs comments if interested.
