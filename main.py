import pyautogui as pag
import time
import keyboard
import numpy as np
import random
import win32api, win32con
from PIL import ImageGrab
from functools import partial
from pathlib import Path
ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)

time.sleep(1)   #wait to start program

pixelVariance = random.randint(-5,5)

def quickSleep(): #sleep between 0.1 and 0.3 secs
    time.sleep(np.random.uniform(0.1,0.3))

# click left mouse button at (x,y) pixel coordinates
# with introduced randomness
# pixelVariance might not change with each call, possibly static from program start
def clickAt(x,y):
    pag.click(x + pixelVariance, y + pixelVariance)
    quickSleep

def pressKey(x):       # press key x (needs commas, pressKey('x'))
    pag.keyDown(x)
    quickSleep
    pag.keyUp(x)
    quickSleep
    
def checkPixelColor(x,y,a,b,c): # checks if pixel(x,y) is RGB value (a,b,c)
    if pag.pixel(x,y)[0][1][2] == [a,b,c]:
        return True
    else:
        return False

def clickImage(image,conf,time): # locates image, puts cursor in center, clicks
    (x,y) = pag.locateCenterOnScreen(image, confidence=conf, minSearchTime=time)
    clickAt(x,y)

def getCoins(): #collect coins
        clickAt(100,600) # focus app
        clickAt(980,620) # collect all
        # should change this to image recognition for portability
        time.sleep(np.random.uniform(0.3,0.5))
        try:
            clickImage('pics/checkButton.png',0.9,0.5)
        except pag.ImageNotFoundException:  #manually click where button should be
            clickAt(350,550)
            clickAt(520,550)
            clickAt(100,600)
        return


def getTreats():    # get treats
    for i in range(2):  # image is dynamic, so try multiple times
        try:
            while pag.locateCenterOnScreen('pics/treats.png', grayscale=False,confidence=0.6, minSearchTime=0.5) != None:
                clickImage('pics/treats.png',0.7,1)
        except pag.ImageNotFoundException:
            i+1
    return


def changeMap(islandCounter):   # change island
    clickImage('pics/map.png',0.9,0.5)    # open map
    time.sleep(np.random.uniform(1,1.5))
    # uses first island as a reference point
    try:
        (x,y) = pag.locateCenterOnScreen('pics/plantIsland.png',confidence=0.9,minSearchTime=0.5)
        clickAt(x,y+40)
    # if not found, scroll up
    except pag.ImageNotFoundException:
        clickAt(170,210)
        (x,y) = pag.locateCenterOnScreen('pics/plantIsland.png',confidence=0.9,minSearchTime=0.5)
        time.sleep(np.random.uniform(1,1.5))
        clickAt(x,y+45)
    # should make this dynamically scroll up until plant island appears
        
    time.sleep(np.random.uniform(2,2.5))
    # from plant island, scroll through islands based on number of islands
    # that should be checked
    for x in range(0, islandCounter):
        clickImage('pics/forwardArrow.png',0.9,0.5)
        time.sleep(np.random.uniform(1,1.2))
    
    clickImage('pics/goButton.png',0.9,0.5) # go to island
    time.sleep(np.random.uniform(1.5,2))

    
def main():

    pag.FAILSAFE = True # pyautogui library failsafe
                        # abort when mouse is moved to upper left corner
    
    # user should start from plant island, hence starting
    # at 1 instead of 0
    islandCounter = 1

    while keyboard.is_pressed('q') == False: #exit code whn q is pressed
        getCoins()
        time.sleep(np.random.uniform(0.9,1.2))
        getTreats()
        time.sleep(np.random.uniform(0.9,1.2))
        changeMap(islandCounter)
        time.sleep(np.random.uniform(0.9,1.2))
        islandCounter = islandCounter + 1

        #reset when all islands are checked
        if islandCounter == 5:
            islandCounter = 0
        
    



if __name__ == "__main__":
    main()
