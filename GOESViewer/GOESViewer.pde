
/*


This is the actual viewer. Change the settings that you need / want to change and then if it runs fine, you can compile it by going to File->Export Application and then click Export.
This will give you an executable that can run standalone. Which is good for cases where you want it to autostart in case of a power loss.


*/



// The default starting view
// 0 = CONUS 1 = FD 2 = Custom Meso 3 = FSCLR FD 4 = FSCLR MESOA 5 = MesoM1 6 = MesoM2
int currentlyViewing = 0;

// The Base Directories, shouldn't have to change these unless you start doing something custom, like in my case, reading from a network drive
String CONUSDir = "MostRecentCONUS";
String MESOADir = "MostRecentMESOA";
String FDDir = "MostRecentFullDisk";
String MesoM1 = "MostRecentMeso/M1";
String MesoM2 = "MostRecentMeso/M2";

// How long we should wait until reload any full disk derived images (Full Disk, CONUS, Custom Meso A). Default is 10 minutes in msec, due to 30 minute image transmission rate
long delayBetweenFullDiskDerivedUpdates = 600000;
// How long we should wait until reload NOAA Selected Meso images(M1 and M2). Default is 5 minutes in msec
long delayBetweenNOAAMesoUpdates = 300000;

// Playback speed. Lower is faster;
int timeBetweenAnims = 100;
// How long it pauses before resetting the loop (in msec)
int timeBeforeReset = 2000;

//Do you want to loop images?
boolean animate = true;




//------------------------------------------------------------------------------//





// Program Support stuff, shouldn't have to change any this. 
// Though if you want to expeirment, by all means. 

long delayBetweenUpdates = 0;
long lastMillis = 0;
long lastMillisUpdate = 0;
long lastAnimMillis = 0;
int maxImagesToLoad = 20;
int ImageToView = 0;
boolean hasSet = false;
boolean state = false;
boolean initFirstImages = true;
boolean loadImg = false;
PImage[] FSCLR;
PImage[] Band064;
PImage[] Band39;
PImage[] Band62;
PImage[] Band69;
PImage[] Band103;
PImage[] Band112;
PImage[] Band123;
String ActiveDir = "";


void setup(){
  
  // If we aren't animating the loop, no sense in loading a lot of images
  if(animate == false){
    maxImagesToLoad = 1;
  }
  
  // Creating the arrays to load the images into memory
  FSCLR = new PImage[maxImagesToLoad];
  Band064 = new PImage[maxImagesToLoad];
  Band39 = new PImage[maxImagesToLoad];
  Band62 = new PImage[maxImagesToLoad];
  Band69 = new PImage[maxImagesToLoad];
  Band103 = new PImage[maxImagesToLoad];
  Band112 = new PImage[maxImagesToLoad];
  Band123 = new PImage[maxImagesToLoad];
  
  
  // Uncomment your resolution (default is 1080p). Feel free to add your own. The panels should scale without issue, well as long as it is a 16:9 ratio.
  size(1920,1080); // 1080p
  //size(2560,1440); //2560p or 2K
  
  
  
  background(0);
  // We want to update our update time and what directory we are looking at right away
  updateView();
  
  // Setting the size of the info text
  textSize(20);
}


void draw(){
  
  // Blank the screen
  background(0);
  
  // Handle input (up/down arrow changes view. A bit clunky but it works. Will hopefully be improved later on)
  KeyDetection();
  
  // Wait the specified length of time before reloading the images
  if(millis() > lastMillis + delayBetweenUpdates || initFirstImages){
    
    lastMillis = millis();
    lastMillisUpdate = millis();
    loadImg = true;
    initFirstImages = false;
    
  }
  
  // Once we have the ok to update, we want to wait a few frames to make sure the "Updating..." text is displayed.
  if(loadImg && millis() > lastMillisUpdate + 1000){
  
   // Reload the images after a second
   loadImages(); 
   lastMillisUpdate = millis();
   loadImg = false;
   
  }
 
  
  // If we are animating, we want to decrease the ImageToView number. The delay specifies how long to wait before resetting the anim. This that pause at the end of loops that you normally see.
  if(animate){
  
  if(millis() >= lastAnimMillis + timeBetweenAnims){
  ImageToView--;
  if(ImageToView <= -1){delay(timeBeforeReset);ImageToView = maxImagesToLoad-1;}
  lastAnimMillis = millis();
  }
  }
  
  // This is actually the function that finally displays the images in panels.
  displayImages(ImageToView);
  
  
  // Just some info text handling
  fill(255);
  text(ActiveDir + " Img: " + str(ImageToView+1), width-300, height-100);
  if(loadImg){
  fill(255,0,0);
  text("Updating...", width-300, height-50);
  }
  else{
  fill(0,255,0);
  text("Up to Date", width-300, height-50);
  }
  
  
}


void KeyDetection(){
  
  // Not much going on in here. Its all pretty self explanatory.
  // You can change the keys here if you would like, but I would recommend looking at processings tutorials before making changes
  
  if(keyPressed){
  if (key == CODED) {
    // If you press the arrow UP, increase the currentlyViewing ID.
    if (keyCode == UP) {
      currentlyViewing+=1;
      // If we go over view 6, reset back to the first view (0)
      if(currentlyViewing > 6){currentlyViewing = 0;}
      background(0);
      hasSet = false;
      // Update the variables to look at the new info
      updateView();
      //delay to prevent multiple key press
      delay(100);
      
      // Basically the same as above, just the other direction
    } else if (keyCode == DOWN) {
      currentlyViewing-=1;
      if(currentlyViewing < 0){currentlyViewing = 6;}
      background(0);
      hasSet = false;
      updateView();
      delay(100);
      
      // If you press the LEFT arrow, it will force an update.
    } else if (keyCode == LEFT) {
      initFirstImages = true;
    }
  }
  }
  
  
  
}



void updateView(){
  
  // This just updates the ActiveDir to the correct Directory variable so we look in the right folders.
  // It also updates the delay times between updates.
  
  if(!hasSet){
    if(currentlyViewing == 0){
      ActiveDir = CONUSDir;
      delayBetweenUpdates = delayBetweenFullDiskDerivedUpdates;
    }
    if(currentlyViewing == 1){
      ActiveDir = FDDir;
      delayBetweenUpdates = delayBetweenFullDiskDerivedUpdates;
    }
    if(currentlyViewing == 2){
      ActiveDir = MESOADir;
      delayBetweenUpdates = delayBetweenFullDiskDerivedUpdates;
    }
    if(currentlyViewing == 5){
      ActiveDir = MesoM1;
      delayBetweenUpdates = delayBetweenNOAAMesoUpdates;
    }
    if(currentlyViewing == 6){
      ActiveDir = MesoM2;
      delayBetweenUpdates = delayBetweenNOAAMesoUpdates;
    }
    if(currentlyViewing == 3){
      ActiveDir = "Full Disk FSCLR";
      delayBetweenUpdates = delayBetweenFullDiskDerivedUpdates;
    }
    if(currentlyViewing == 4){
      ActiveDir = "CMesoA FSCLR";
      delayBetweenUpdates = delayBetweenFullDiskDerivedUpdates;
    } 
    hasSet = true;
    // Force a reload of images to the new updated view
    initFirstImages = true;
  }
  
  
}


void loadImages(){
  
  
  // Here we read all of the images into memory for quick play back
  
  
  print("Running Update");
  
  
  initFirstImages = false;
  
  // We need a "try/catch" here because if we load images while the sorter program is moving files, we could throw an error. This handes that and allows the program to continue until it gets the images its looking for
  
  try{
  
  
  // Not sure if its because my reception isn't good enough or if its by design, but I only get four bands on NOAA Mesos. So I had no choice but to split the views into their own for loops.
  
  // If we are viewing a Full Disk Derived view, load all bands.
  if(currentlyViewing != 3 && currentlyViewing != 4 && currentlyViewing != 5 && currentlyViewing != 6){
  
  // For each image, 
  for(int i = 0; i < maxImagesToLoad; i++){
    
    //Look at the correct band folder and load the image into the array.
    FSCLR[i] = loadImage(ActiveDir + "/FSCLR/"+ str(i) + ".jpg");
    //Resize the image so that we can fit everything in the window space we have specified.
    FSCLR[i].resize(width/3, height/3);
    
    //The same thing for the rest of the bands
    Band064[i] = loadImage(ActiveDir + "/VIS(0.64)/"+ str(i) + ".jpg");
    Band064[i].resize(width/3, height/3);
    Band39[i] = loadImage(ActiveDir + "/IR(3.9)/Enhanced/"+ str(i) + ".jpg");
    Band39[i].resize(width/3, height/3);
    Band62[i] = loadImage(ActiveDir + "/IR(6.2)/Enhanced/"+ str(i) + ".jpg");
    Band62[i].resize(width/3, height/3);
    Band69[i] = loadImage(ActiveDir + "/IR(6.9)/Enhanced/"+ str(i) + ".jpg");
    Band69[i].resize(width/3, height/3);
    Band103[i] = loadImage(ActiveDir + "/IR(10.3)/Enhanced/"+ str(i) + ".jpg");
    Band103[i].resize(width/3, height/3);
    Band112[i] = loadImage(ActiveDir + "/IR(11.2)/Enhanced/"+ str(i) + ".jpg");
    Band112[i].resize(width/3, height/3);
    Band123[i] = loadImage(ActiveDir + "/IR(12.3)/Enhanced/"+ str(i) + ".jpg");
    Band123[i].resize(width/3, height/3);
  }
  
  //This ensures our update interval is started from the end of the update.
  lastMillis = millis();
  }
  
  
  
  
  else{
    
    
    // Basically the same as above, but with only the Full Disk FSCLR, because it looks cool.
    if(currentlyViewing == 3){
      for(int i = 0; i < maxImagesToLoad; i++){
        FSCLR[i] = loadImage("MostRecentFullDisk/FSCLR/"+ str(i) + ".jpg");
        FSCLR[i].resize(height-80, height-80);
      }
    lastMillis = millis();
    }
    
    // Only the Custom Meso A FSCLR, because again it looks cool.
    if(currentlyViewing == 4){
      for(int i = 0; i < maxImagesToLoad; i++){
        FSCLR[i] = loadImage("MostRecentMESOA/FSCLR/"+ str(i) + ".jpg");
        FSCLR[i].resize(height-80, height-80);
      }
    lastMillis = millis();
    }
    
    
    // NOAA Selected Mesos (M1 and M2). Not sure if its by design or if its because of my bad reception but I have only gotten these 4 bands...
    // If you get other bands, let me know. Would be fairly easy to add them in.
    if(currentlyViewing == 5 || currentlyViewing == 6){
      
      for(int i = 0; i < maxImagesToLoad; i++){
        FSCLR[i] = loadImage(ActiveDir + "/FSCLR/"+ str(i) + ".jpg");
        FSCLR[i].resize(width/2, height/2);
        Band064[i] = loadImage(ActiveDir + "/VIS(0.64)/"+ str(i) + ".jpg");
        Band064[i].resize(width/2, height/2);
        Band39[i] = loadImage(ActiveDir + "/IR(3.9)/Enhanced/"+ str(i) + ".jpg");
        Band39[i].resize(width/2, height/2);
        Band103[i] = loadImage(ActiveDir + "/IR(10.3)/Enhanced/"+ str(i) + ".jpg");
        Band103[i].resize(width/2, height/2);
        lastMillis = millis();
      }
      
    }
    

    
  }
  }
  catch(Exception e){
    lastMillis = millis();
  }

}







void displayImages(int i){
  
  // This actually draws the images to the screen.
  
  
  // Another try/catch just in case of null pointers during intial loading
  
  try{
  
  // If we are updating for the first time, we dont want to keep doing it. Disabling.
  initFirstImages = false;
  
  if(currentlyViewing != 3 && currentlyViewing != 4 && currentlyViewing != 5 && currentlyViewing != 6){

    // Display the specified image. Specified by the function param 'i'
    
    
    image(FSCLR[i], 0, 0);
    image(Band064[i], (width/3), 0);
    image(Band39[i], (width/3)*2, 0);
    image(Band62[i], 0, (height/3));
    image(Band69[i], (width/3), (height/3));
    image(Band103[i], (width/3)*2, (height/3));
    image(Band112[i], 0, (height/3)*2);
    image(Band123[i], (width/3), (height/3)*2);
  

  }

  else{
    
    
    // Same as above but with only FSCLR Full Disk
    if(currentlyViewing == 3){
    image(FSCLR[i], (width/4)-100, 0);

    }
    
    // Same as above but with only FSCLR Custom Meso A
    if(currentlyViewing == 4){
    image(FSCLR[i],(width/4)-100, 0);

    }
    
    // Same as above but NOAAs Selected Mesos
    if(currentlyViewing == 5 || currentlyViewing == 6){
      
      
        image(FSCLR[i], 0, 0);        
        image(Band064[i],(width/2), 0);        
        image(Band39[i], 0, (height/2));
        image(Band103[i],(width/2), (height/2));
      
    }
    
    
    
  }
  }
  catch(Exception e){
  }
}

  
  
  
