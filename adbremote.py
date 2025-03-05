#!/usr/bin/env python

#List of adb input comands
#https://gist.github.com/arjunv/2bbcca9a1a1c127749f8dcb6d36fb0bc
#for scrolling
#adb shell input roll <dx> <dy>
import PySimpleGUI as sg
from os import system


#Pushes the string to ADB, and also prints it for debug purpouses
def ADB(Input):
    print(Input)
    system(Input)

#works by taking screenshots of the glass's screen and copying them over, this
#gets the inital screenshot
ADB("adb shell screencap -p /sdcard/screen.png")
ADB("adb pull /sdcard/screen.png")

#Import the image
ScreenShot = sg.Image(key="-IMAGE-", filename="screen.png", enable_events = True)
#Create the window
window = sg.Window("Image Viewer", [[ScreenShot]], return_keyboard_events=True)

# Run the Event Loop
while True:
    event, values = window.read()

    print(event, values) #Debug
    #As near as I can tell there is no obvious way to get the position of the 
    #Curser inside the window so it needs to be derived
    AbsX, AbsY = window.mouse_location()
    RelX, RelY = window.current_location(without_titlebar = True)

    #Window and picture size
    WSX, WSY = window.size
    PSX, PSY = window["-IMAGE-"].get_size() 

    #Calculate the offset
    XOffset = (WSX - PSX)/2
    YOffset = (WSY - PSY)/2
    
    #The actual touch location
    TouchX = AbsX - RelX - XOffset
    TouchY = AbsY - RelY - YOffset
    print("loctation:", (TouchX, TouchY)) #Debug
   
    #we know where they clicked on the screen, time to send the click to the glass
    ADB("adb shell input tap %s %s" % (TouchX, TouchY))
    #and grab a new screenshot
    ADB("adb shell screencap -p /sdcard/screen.png")
    ADB("adb pull /sdcard/screen.png")


    window["-IMAGE-"].update(filename="screen.png") 
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    # Folder name was filled in, make a list of files in the folder

window.close()
