
################ THIS CODE IS EXPERIMENTAL, MAKE A BACK UP OF YOUR IMAGES #######################


Prerequisites
- Install Python. Anaconda is recommended.
https://www.anaconda.com/products/distribution?gclid=Cj0KCQjwvLOTBhCJARIsACVldV21gCtwWYyxqvIEVWwF0NLjoCvp__YOVxMHDd3Bh9hz8-Du1m4pF80aAv2bEALw_wcB
- Add Python to system path variables.
- No other libraries needed.

- Install Processing
https://processing.org/download



#################### Sorter ##########################

To get this set up without having to change any major part of the program:



1.  Go into what ever program you are using for generating the images, and tell it to place all images in the GOESImages Folder

2.  Open the sort.py using the included editor that is installed by python (usually IDLE), or by using notepad (not recommended due to indentation issues).

3.  Configure the settings that you want. Mainly what fileFormat (can be anything really, but .jpg is default), timeBetweenSearch (how often the proram searches the main image folder), and maxLoopedImages (this will tell the program how many blank images to create and then later shift)

3a. Run the sorter by opening powershell (Shift Right click in the folder contaning the sort.py and click "open powershell window here") and running "python sort.py"
3b  Or, run it by simply running the runFileTransfer.bat



##### The sorter should be running at this point #####



4. It should say "Creating Blanks". This may or may not take a long time depending on how many images you set to loop. This is it making the place holder images so that the sorter has images to shift and wont run into issues.

5. After the blanks are created, it will start looking for images in the GOESImages Folder (delay between checks is set by the timeBetweenSearch variable)

6. Once it finds an image, it will split the file name up to figure out what it is and where it should go.

7. It will then shift the image sequence, delete the oldest one (more of an overwrite) and then copy the image that it found, into the 0 position.

8. It will then move the image from the main GOESImages folder to the correct view and then to the correct band.


################## Processing #######################


9.  Next, go into the prossing sketch (GOESViewer.pde)

10. Go through the top variables and configure them to your needs

11. Set your resolution by commenting/uncommenting it on lines 89 and 90 (The one uncommented by default is 1080p, the other is 2k)

11. Run the script by pressing the play button at the top or by pressing CTRL+R

12 Finally, if everything runs good, you can complile it and run standalone by going to File->Export Application and then click Export





#################### Extra #########################

If you need an image archiver, I have included one. It is located in the GOESViewer Folder (archive.py). More details in the programs comments if interested.
