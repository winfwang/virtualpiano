####################################
# Influenced by LeapMotion starter code: <>
####################################
#import Leap, sys, thread, time 
# import module_manager
# module_manager.review()

import os, sys, inspect, thread, time

import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture


from Tkinter import *
import winsound

#from pydub import AudioSegment

# Audio Functionality influenced by:
# <https://pythonbasics.org/python-play-sound/>

# Audio Files drawn from: 
# <http://theremin.music.uiowa.edu/MISpiano.html>

# Influenced by website 
# <https://www.c-sharpcorner.com/blogs/basics-for-displaying-image-in-
# tkinter-python>

# Otherwise specfically cited, all Images and Gifs all drawn from Giphy Website:
# <https://giphy.com/>

####################################
# Notes:
# - include a splash screen that takes a bit to load to the home screen
# - how to download PIL for python 2.7
####################################

####################################
# Code below for PyAudio drawn from online website:
# <https://abhgog.gitbooks.io/pyaudio-manual/sample-project.html>
####################################
"""PyAudio Example: Play a WAVE file."""

import pyaudio
import wave
from array import array
from struct import pack

def play(file):
    CHUNK = 1024 #measured in bytes

    wf = wave.open(file, 'rb')

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(CHUNK)

    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()

    p.terminate()

###########################################################################
######################### Recording a WAV file ############################
###########################################################################
def record(outputFile):
    CHUNK = 1024 #measured in bytes
    FORMAT = pyaudio.paInt16
    CHANNELS = 2 #stereo
    RATE = 44100 #common sampling frequency
    # RECORD_SECONDS = 5 #change this record for longer or shorter!

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")
     
    import keyboard

    frames = []
    
    while not keyboard.is_pressed("s"):
        data = stream.read(CHUNK)
        frames.append(data)
        
    # for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    #     data = stream.read(CHUNK)
    #     frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(outputFile, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

####################################
# Leap Motion Classes
####################################

class HandIndicator(object):
    def __init__(self, x, y, z):
        self.x = x + 500 # since visualizer's 0,0 starts in the middle
        self.y = y
        self.z = z + 350 # 500 is half of width, 350 is half of height
        self.r = 10
        
    def drawFingerPosition(self, canvas):
        # z coord of visualizer is y of tkinter
        canvas.create_oval(self.x - self.r, self.z - self.r,
                           self.x + self.r, self.z + self.r,
                           fill = None, outline = "red", width = 5)
    
class TouchSoundLink(object):
    def __init__(self, width, height, isPressed, fingerX, fingerY, keyboardWidth, keyboardHeight):
        self.width = width
        self.height = height
        self.isPressed = isPressed
        self.fingerX = fingerX + 500
        self.fingerY = fingerY + 350
        self.keyboardX0, self.keyboardX = keyboardWidth 
        self.keyboardY0, self.keyboardY = keyboardHeight
        self.whiteKeyLst = ["A0","B0",
                            "C1","D1","E1","F1","G1","A1","B1",
                            "C2","D2","E2","F2","G2","A2","B2",
                            "C3","D3","E3","F3","G3","A3","B3",
                            "C4","D4","E4","F4","G4","A4","B4",
                            "C5","D5","E5","F5","G5","A5","B5",
                            "C6","D6","E6","F6","G6","A6","B6",
                            "C7","D7","E7","F7","G7","A7","B7",
                            "C8"]
        self.blackKeyLst = ["Bb0",
                            "Db1","Eb1","Gb1","Ab1","Bb1",
                            "Db2","Eb2","Gb2","Ab2","Bb2",
                            "Db3","Eb3","Gb3","Ab3","Bb3",
                            "Db4","Eb4","Gb4","Ab4","Bb4",
                            "Db5","Eb5","Gb5","Ab5","Bb5",
                            "Db6","Eb6","Gb6","Ab6","Bb6",
                            "Db7","Eb7","Gb7","Ab7","Bb7"]
        self.blackKeyMiddlesLst = ["Ab1","Ab2","Ab3","Ab4","Ab5","Ab6","Ab7",]
    
    def playSound(self, numOfKeys, blackKeyHeight, whiteKeyWidth, scrollX, groupTwoLst, groupTwoLstOne, groupTwoLstMiddles):
        
        if self.isPressed:
            # look at coord for pointable and play sound based off that
            # bottom area without black keys
            
            for i in range(numOfKeys):
                x0 = (self.keyboardX0 + whiteKeyWidth * i) - scrollX
                x = (self.keyboardX0 + whiteKeyWidth * (i + 1)) - scrollX
                
                if self.keyboardY0 <= self.fingerY <= blackKeyHeight:
                    newX0 = (self.keyboardX0 + whiteKeyWidth * (i + 0.7)) - scrollX
                    if i == 1:
                        if x0 - self.width * 0.01 <= self.fingerX - scrollX <= newX0 - self.width * 0.01:
                            winsound.PlaySound("Piano.ff." + self.blackKeyLst[0] + ".wav", winsound.SND_ASYNC)
                            
                    elif i == 51:
                        continue
                        
                    elif i in groupTwoLst:
                        if i in groupTwoLstOne:
                            if x0 - self.width * 0.023 <= self.fingerX - scrollX <= newX0 - self.width * 0.023:
                                for key in range(numOfKeys):
                                    if x0 == self.keyboardX0 + whiteKeyWidth * key and \
                                    newX0 == self.keyboardX0 + whiteKeyWidth * (key + 0.7):
                                        if key in [3,10,17,24,31,38,45]:
                                            noteFile = "Db"
                                        else:
                                            noteFile = "Gb"
                                        winsound.PlaySound("Piano.ff." + noteFile + str(key // 7 + 1) + ".wav", winsound.SND_ASYNC)
                                 
                        else:
                            if x0 - self.width * 0.01 <= self.fingerX - scrollX <= newX0 - self.width * 0.01:
                                for key in range(numOfKeys):
                                    if x0 == self.keyboardX0 + whiteKeyWidth * key and \
                                    newX0 == self.keyboardX0 + whiteKeyWidth * (key + 0.7):
                                        if key in [4,11,18,25,32,39,46]:
                                            noteFile2 = "Eb"
                                            fileLevel = key // 7 + 1
                                        else:
                                            noteFile2 = "Bb"
                                            fileLevel = key // 7
                                            
                                        winsound.PlaySound("Piano.ff." + noteFile2 + str(fileLevel) + ".wav", winsound.SND_ASYNC)
                    
                    elif i in groupTwoLstMiddles:
                        if x0 - self.width * 0.017 <= self.fingerX - scrollX <= newX0 - self.width * 0.017:
                                for key in range(numOfKeys):
                                    if x0 == self.keyboardX0 + whiteKeyWidth * key and \
                                    newX0 == self.keyboardX0 + whiteKeyWidth * (key + 0.7):
                                        winsound.PlaySound("Piano.ff.Ab" + str(key / 7) + ".wav", winsound.SND_ASYNC)
            
                elif self.keyboardY0 <= self.fingerY <= self.keyboardY and x0 <= self.fingerX - scrollX <= x:
                    for key in range(numOfKeys):
                        if x0 == self.keyboardX0 + whiteKeyWidth * key and \
                        x == self.keyboardX0 + whiteKeyWidth * (key + 1):

                            winsound.PlaySound("Piano.ff." + self.whiteKeyLst[key] + ".wav", winsound.SND_ASYNC)


####################################
# Animation Framework
####################################
def init(data):
    data.controller = Leap.Controller()
    data.frame = data.controller.frame()
    data.fingerNames = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    data.boneNames = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    
    data.timerDelay = 10
    data.timer = 0
    
    #counts number of fingers that are pointable and extended
    data.numOfFingers = 0
    
    # button positions
    # homescreen buttons
    
    data.buttonY0, data.buttonY = data.height * 0.65 - 90, data.height * 0.65 + 90
    data.button1X0, data.button1X = data.width * 0.25 - 85, data.width * 0.25 + 85
    data.button2X0, data.button2X = data.width * 0.5 - 85, data.width * 0.5 + 85
    data.button3X0, data.button3X = data.width * 0.75 - 85, data.width * 0.75 + 85
        
    # back to home button
    data.homebuttonX = data.width * 0.05 - 30
    data.homebuttonY = data.height * 0.95 - 100
    data.homebuttonX1 = data.width * 0.05 + 30
    data.homebuttonY1 = data.height * 0.95 - 10
    
    # booleans determining screen
    data.isHomeScreen = True
    data.isPianoPracticeScreen = False
    data.isSongLearningScreen = False
    data.isSavedRecordingsScreen = False
    
    # keyboard 
    data.numOfWhiteKeys = 52
    data.scrollX, data.scrollY = -700, 0
    data.keyboardX0, data.keyboardY0 = 0, data.height // 3
    data.keyboardX = data.width * 2.6 # for 52 (white) keys (36 black keys)
    data.keyboardY = data.height // 3 * 2
    data.whiteKWidth = data.width * 0.05 
    data.blackKLength = data.height // 20 * 10.5
    # black key: (don't mind the groupTwo name)
    data.groupTwoLst = [3,4,6,8,10,11,13,15,17,18,20,22,24,25,27,29,31,32,34,36,38,39,41,43,45,46,48,50]
    data.groupTwoLstOne = [3,6,10,13,17,20,24,27,31,34,38,41,45,48]
    data.groupTwoLstMiddles = [7,14,21,28,35,42,49]
    
    # keyboard map
    data.mapX0, data.mapX = 0, data.width
    data.mapY0, data.mapY = data.height // 18, data.height // 18 * 3
    data.mapKeyLength = 19.23076923076923 
    data.mapBlackKeyLength = data.height // 18 * 2 * 1.05
    
    # scroll box
    data.scroll2X = -700
    
    data.scrollX0 = data.mapX0 + data.mapKeyLength * 14
    data.scrollY0 = data.height // 18 * 0.5
    data.scrollX1 = data.mapX0 + data.mapKeyLength * 34
    data.scrollY1 = data.height // 18 * 3.5
    
    data.imgFrame = PhotoImage(file = "frame.gif")
    
    data.imgUpArrow = PhotoImage(file = "arrow.gif")
  
    # to draw where fingers are
    data.fingerCircles = []
    
    # initialize TouchSoundLink Class
    data.soundLink = TouchSoundLink(data.width, data.height, False, 0, 0, (0,0), (0,0))
    
    # images uploaded
    data.img1Frames = 5
    data.img1Index = 0
    data.img1 = PhotoImage(file = "PianoFalling.gif")
    data.img2 = PhotoImage(file = "animePiano.gif")    
    data.img3 = PhotoImage(file = "apeSmash2.gif")    
    data.img4 = PhotoImage(file = "catPiano.gif")    
    data.img5 = PhotoImage(file = "corgiPiano.gif")    
    data.img6 = PhotoImage(file = "classicalColors.gif")    
    data.img7 = PhotoImage(file = "homeBackground.gif")    
    data.img8Frames = 3
    data.img8Index = 0
    data.img8 = PhotoImage(file = "tvBlur.gif")
    data.img9 = PhotoImage(file = "drawnKeys.gif")
    data.img10 = PhotoImage(file = "pianoBackground4.gif")
    data.img11 = PhotoImage(file = "Studio1.gif")
    
    # title images
    data.imgV = PhotoImage(file = "letterV.gif", format = "gif -index 1")
    data.imgI2 = PhotoImage(file = "letterI2.gif")    
    data.imgR = PhotoImage(file = "letterR.gif")
    data.imgT = PhotoImage(file = "letterT.gif")    
    data.imgU = PhotoImage(file = "letterU.gif")    
    data.imgA2 = PhotoImage(file = "letterA2.gif")    
    data.imgL = PhotoImage(file = "letterL.gif")        
    data.imgP = PhotoImage(file = "letterP.gif")    
    data.imgI = PhotoImage(file = "letterI.gif")    
    data.imgA = PhotoImage(file = "letterA.gif")
    data.imgN = PhotoImage(file = "letterN.gif")    
    data.imgO = PhotoImage(file = "letterO.gif")    
    data.imgI3 = PhotoImage(file = "letterI3.gif", format = "gif -index 8")    
    data.imgN2 = PhotoImage(file = "letterN2.gif")
        
    # button images
    data.imgHomeButton = PhotoImage(file = "Inkedbutton1.gif")
    data.imgbuttTxt1 = PhotoImage(file = "textButt1.gif")
    data.imgbuttTxt2 = PhotoImage(file = "textButt2.gif")
    data.imgbuttTxt3 = PhotoImage(file = "textButt3.gif")
    
    data.imgPlayButton = PhotoImage(file = "playButton.gif")
    data.playButtonX0 = data.width // 7 * 3 - 45
    data.playButtonX = data.width // 7 * 3 + 45
    data.PSButtonY0 = data.height * 0.85 - 45
    data.PSButtonY = data.height * 0.85 + 45
    data.playIsPressed = False
    data.imgStopButton = PhotoImage(file = "stopButton.gif")
    data.stopButtonX0 = data.width // 7 * 4 - 45
    data.stopButtonX = data.width // 7 * 4 + 45
    data.stopIsPressed = True
    
    data.recordingNum = 1
    
    data.imgBackButton = PhotoImage(file = "homeArrow.gif")
    
    # drop down menu vars
    data.img12 = PhotoImage(file = "vinyl.gif")
    data.img13 = PhotoImage(file = "dropDown.gif")
    data.dropDownMenu = False
    
    data.scrollUpDown = 0 
    
    data.mainPath = r"C:\Users\win12\Desktop\15-112 S19\TP\LeapDeveloperKit_3.2.0+45899_win\LeapSDK\lib"
    data.fileLst = []
    
def mousePressed(event, data):
    buttonWidth = data.width * 0.3
    buttonHeight = data.height * 0.05
    
    
    # home screen buttons
    # use event.x and event.y
    if data.isHomeScreen:
        if data.buttonY0 <= event.y <= data.buttonY:
            if data.button1X0 <= event.x <= data.button1X:
                data.isHomeScreen = False
                data.isPianoPracticeScreen = True
                
            elif data.button2X0 <= event.x <= data.button2X:
                data.isHomeScreen = False
                data.isSongLearningScreen = True
                
            elif data.button3X0 <= event.x <= data.button3X:
                data.isHomeScreen = False
                data.isSavedRecordingsScreen = True
    
    # back to home button
    if not data.isHomeScreen:
        if data.homebuttonX <= event.x <= data.homebuttonX1 \
        and data.homebuttonY <= event.y <= data.homebuttonY1:
            data.isHomeScreen = True
            if data.isPianoPracticeScreen:
                init(data)
                data.isPianoPracticeScreen = False
                
            elif data.isSongLearningScreen:
                data.isSongLearningScreen = False
                
            elif data.isSavedRecordingsScreen:
                data.isSavedRecordingsScreen = False
    
    if data.isSavedRecordingsScreen:
        if data.width * 0.2 - 45 <= event.x <= data.width * 0.2 + 45 and \
        data.height * 0.3 - 50 <= event.y <= data.height * 0.3 + 50:
            data.dropDownMenu = True
        
        if data.dropDownMenu:
            if data.height * 0.15 <= event.y <= data.height * 0.25 and \
            data.width * 0.7 <= event.x <= data.width * 0.9:
                play("recording1.wav")
            elif data.height * 0.35 <= event.y <= data.height * 0.45 and \
            data.width * 0.7 <= event.x <= data.width * 0.9:
                play("recording2.wav")
            elif data.height * 0.55 <= event.y <= data.height * 0.65 and \
            data.width * 0.7 <= event.x <= data.width * 0.9:
                play("recording3.wav")
                
    # recording button
    # if data.isPianoPracticeScreen:
        # # play button is pressed
        # if data.playButtonX0 <= event.x <= data.playButtonX and \
        # data.PSButtonY0 <= event.y <= data.PSButtonY:
        #     data.playIsPressed = True
        #     data.stopIsPressed = False
        #     
        # # stop button is pressed
        # elif data.stopButtonX0 <= event.x <= data.stopButtonX and \
        # data.PSButtonY0 <= event.y <= data.PSButtonY:
        #     data.playIsPressed = False
        #     data.stopIsPressed = True
            
    # scroll box moving
    # if 0 <= event.x <= data.width and \
    # (data.height // 18) <= event.y <= (data.height // 18 * 3):
    #     data.scrollX0 = event.x - data.mapKeyLength * 10 - data.scroll2X - 700
    #     
    #     data.scrollX1 = event.x + data.mapKeyLength * 10 - data.scroll2X - 700
    
        
    
    pass

def keyPressed(event, data):
    # use event.char and event.keysym
    if data.isPianoPracticeScreen:
        if event.keysym == "Right" and data.scrollX > -1600:
            data.scrollX -= 10
            data.scroll2X -= (data.mapKeyLength / 5)
        elif event.keysym == "Left" and data.scrollX < 0:
            data.scrollX += 10
            data.scroll2X += (data.mapKeyLength / 5)
        
        # play button is pressed
        if event.char == "p":
            data.playIsPressed = True
            data.stopIsPressed = False
            
        # stop button is pressed
        elif event.char == "s":
            data.playIsPressed = False
            data.stopIsPressed = True
    
    if data.isSavedRecordingsScreen:
        if event.keysym == "Up":
            data.scrollUpDown += 10
        elif event.keysym == "Down":
            data.scrollUpDown -= 10
    
    
    pass

def timerFired(data):
    if data.timer < 1000:
        data.timer += 1
    else:
        data.timer = 0
    
    if data.img8Index < data.img8Frames - 1:
        data.img8Index += 1
    else:
        data.img8Index = 0

    data.img8 = PhotoImage(file = "tvBlur.gif", format = "gif -index %d" % (data.img8Index))
    
    updateLeapMotionData(data)
    printLeapMotionData(data)
    
def updateLeapMotionData(data):
    data.frame = data.controller.frame()
    

def printLeapMotionData(data):
    frame = data.frame
    interactionBox = frame.interaction_box
    
    for hand in frame.hands:
        data.fingerCircles = []
        handType = "Right" if hand.is_right else "Left"
        for pointable in frame.pointables:
            data.fingerCircles.append(HandIndicator(pointable.tip_position.x,
                                                    pointable.tip_position.y,
                                                    pointable.tip_position.z))
            normalizedPosition = interactionBox.normalize_point(pointable.tip_position)
            if not pointable.is_extended:
                data.soundLink = TouchSoundLink(data.width, data.height,
                                                True, 
                                                pointable.tip_position.x, 
                                                pointable.tip_position.z,
                                                (data.keyboardX0, data.keyboardX), 
                                                (data.keyboardY0, data.keyboardY))
                data.soundLink.playSound(data.numOfWhiteKeys, data.blackKLength, data.whiteKWidth, data.scrollX, data.groupTwoLst, data.groupTwoLstOne, data.groupTwoLstMiddles)
    pass
    
def drawHomeScreen(canvas, data):
    buttonWidth = data.width * 0.3
    buttonHeight = data.height * 0.05
    
    # background
    for i in range(100):
        canvas.create_rectangle(0, 0 + data.height // 100 * i, 
                                data.width, data.height // 100 * (i + 1), 
                                fill = "white", width = 0)
    
    canvas.create_image(data.width // 2, data.height // 2, image = data.img8)
    canvas.create_image(data.width // 2, 0, image = data.img8, anchor = "n")    
    canvas.create_image(data.width // 2, data.height, image = data.img8, anchor = "s")    
    canvas.create_image(data.width, data.height // 2, image = data.img8, anchor = "e")    
    canvas.create_image(0, data.height // 2, image = data.img8, anchor = "w")    
    canvas.create_image(0, 0, image = data.img8, anchor = "nw")    
    canvas.create_image(data.width, 0, image = data.img8, anchor = "ne")    
    canvas.create_image(0, data.height, image = data.img8, anchor = "sw")    
    canvas.create_image(data.width, data.height, image = data.img8, anchor = "se")    
    
    canvas.create_image(data.width * 0.08, data.height * 0.3, image = data.imgV)
    
    canvas.create_image(data.width * 0.1, data.height, image = data.img9, anchor = "s")
    canvas.create_image(data.width * 0.45, data.height, image = data.img9, anchor = "s")
    canvas.create_image(data.width * 0.8, data.height, image = data.img9, anchor = "s")
    
    # canvas.create_image(data.width * 0.1, 0, image = data.img9, anchor = "n")
    # canvas.create_image(data.width * 0.45, 0, image = data.img9, anchor = "n")
    # canvas.create_image(data.width * 0.8, 0, image = data.img9, anchor = "n")
    # title
    #canvas.create_image(data.width * 0.08, data.height * 0.3, image = data.imgV)
    canvas.create_image(data.width * 0.25, data.height * 0.15, image = data.imgI2)
    canvas.create_image(data.width * 0.35, data.height * 0.15, image = data.imgR)
    canvas.create_image(data.width * 0.475, data.height * 0.15, image = data.imgT)
    canvas.create_image(data.width * 0.625, data.height * 0.15, image = data.imgU)
    canvas.create_image(data.width * 0.775, data.height * 0.15, image = data.imgA2)
    canvas.create_image(data.width * 0.9, data.height * 0.15, image = data.imgL)
    
    canvas.create_image(data.width * 0.25, data.height * 0.375, image = data.imgP)
    canvas.create_image(data.width * 0.375, data.height * 0.375, image = data.imgI)
    canvas.create_image(data.width * 0.5, data.height * 0.375, image = data.imgA)
    canvas.create_image(data.width * 0.65, data.height * 0.375, image = data.imgN)
    canvas.create_image(data.width * 0.775, data.height * 0.375, image = data.imgO)
                            
    # button1: Start Practicing!
    canvas.create_image(data.width * 0.25, data.height * 0.75, image = data.imgHomeButton)
    canvas.create_image(data.width * 0.2495, data.height * 0.755, image = data.imgbuttTxt1)
   
    # button2: Learn a Song!
    canvas.create_image(data.width * 0.5, data.height * 0.75, image = data.imgHomeButton)
    canvas.create_image(data.width * 0.5, data.height * 0.75, image =  data.imgbuttTxt2)
    

    # button3: Saved Recordings
    canvas.create_image(data.width * 0.75, data.height * 0.75, image = data.imgHomeButton)
    canvas.create_image(data.width * 0.75, data.height * 0.75, image = data.imgbuttTxt3)
   
                       
def drawPianoPractice(canvas, data):
    # background
    for i in range(100):
        canvas.create_rectangle(0, 0 + data.height // 100 * i, 
                                data.width, data.height // 100 * (i + 1), 
                                fill = "gray" + str(i + 1), width = 0)
    
    canvas.create_image(data.width // 2, data.height // 2, image = data.img10)
    canvas.create_rectangle(0, data.keyboardY0, data.width, data.keyboardY, fill = "white")
                            
    # map keyboard
    canvas.create_rectangle(data.mapX0, data.mapY0, data.mapX, data.mapY,
                            fill = "white", width = 0)
    for num in range(data.numOfWhiteKeys):
        mX0, mY0 = data.mapX0 + data.mapKeyLength * num, data.mapY0
        mX, mY = data.mapX0 + data.mapKeyLength * num, data.mapY
        canvas.create_line(mX0, mY0, mX, mY, fill = "black")
        # middle c mark
        canvas.create_text(data.mapX0 + data.mapKeyLength * 23.5, (data.mapY0 + data.mapY) * 0.68, text = "C", font = "Times 8 bold")
        newX = data.mapX0 + data.mapKeyLength * (num + 0.7)
        newY = data.mapBlackKeyLength
        if num == 1:
            canvas.create_rectangle(mX0 - data.width * 0.005, mY0, 
                                    newX - data.width * 0.005, newY, 
                                    fill = "black")
            
        elif num == 51:
            continue
        
        elif num in data.groupTwoLst:
            if num in data.groupTwoLstOne:
                keyDiff = data.width * 0.009
            else:
                keyDiff = data.width * 0.005
            canvas.create_rectangle(mX0 - keyDiff, mY0,
                                    newX - keyDiff, newY,
                                    fill = "black")
                                    
        elif num in data.groupTwoLstMiddles:
            canvas.create_rectangle(mX0 - data.width * 0.007, mY0, 
                                    newX - data.width * 0.007, newY, 
                                    fill = "black")
    
    # scrolling box
    canvas.create_image((data.scrollX0 + data.scrollX1) // 2 - data.scroll2X - 730.461538462,
                        (data.scrollY0 + data.scrollY1) // 2, image = data.imgFrame)
                        
    canvas.create_image((data.scrollX0 + data.scrollX1) // 2 - data.scroll2X - 700,
                        data.scrollY1 * 1.25, image = data.imgUpArrow)
    
    canvas.create_text((data.scrollX0 + data.scrollX1) * 0.45 - data.scroll2X - 700,
                        data.scrollY1 * 1.35, text = "You \nAre \nHere", font = ("courier", 20, "bold"), fill = "white")
        
    # main keyboard
    x0, y0 = data.keyboardX0 + data.scrollX, data.keyboardY0 + data.scrollY
    x, y = data.keyboardX + data.scrollX, data.keyboardY + data.scrollY
    canvas.create_rectangle(x0, y0, x, y, fill = "white")
    
    # white keys
    for num in range(data.numOfWhiteKeys):
        a0 = data.keyboardX0 + data.whiteKWidth * num + data.scrollX
        b0 = data.keyboardY0 + data.scrollY
        a = data.keyboardX0 + data.whiteKWidth * num + data.scrollX
        b = data.keyboardY + data.scrollY
        canvas.create_line(a0, b0, a, b, fill = "black")
        canvas.create_text(data.keyboardX0 + data.whiteKWidth * 23.5 + \
                           data.scrollX, 
                           (data.keyboardY0 + data.keyboardY) * 0.635 + \
                           data.scrollY, text = "C", font = "Times 30 bold")
        
    # black keys
        newA = data.keyboardX0 + data.whiteKWidth * (num + 0.7) + data.scrollX
        newB = data.blackKLength + data.scrollY
        
        # beginning two keys
        if num == 1:
            canvas.create_rectangle(a0 - data.width * 0.01, b0, 
                                    newA - data.width * 0.01, newB, 
                                    fill = "black")
                                    
        # end key
        elif num == 51:
            continue
            
        # double group (seven)
        elif num in data.groupTwoLst:
            if num in data.groupTwoLstOne:
                groupTwoDiff = data.width * 0.023
            else:
                groupTwoDiff = data.width * 0.01
            canvas.create_rectangle(a0 - groupTwoDiff, b0, 
                                    newA - groupTwoDiff, newB, 
                                    fill = "black")
                                    
        elif num in data.groupTwoLstMiddles:
            canvas.create_rectangle(a0 - data.width * 0.017, b0, newA - data.width * 0.017, newB, fill = "black")
        
    # home screen button
    canvas.create_image(data.width * 0.05, data.height * 0.95, image = data.imgBackButton, anchor = "s")
    
    # user comments/interactions
    # record and stop recording button
    if not data.playIsPressed and data.stopIsPressed:
        canvas.create_image(data.width // 7 * 3, data.height * 0.85, image = data.imgPlayButton)
        canvas.create_text(data.width // 7 * 4, data.height * 0.85, text = "Record", fill = "white", font = "courier 20 bold")
    elif not data.stopIsPressed and data.playIsPressed:
        canvas.create_image(data.width // 7 * 4, data.height * 0.85, image = data.imgStopButton)
        record("recording" + str(data.recordingNum) + ".wav")
        data.recordingNum += 1

    pass
    
def drawSongLearning(canvas, data):
    # background
    
    canvas.create_image(data.width, 0, image = data.img1, anchor = "ne")
    canvas.create_image(0, data.height, image = data.img2, anchor = "sw")
    canvas.create_image(data.width, data.height, image = data.img3, anchor = "se")
    canvas.create_image(data.width, data.height // 2, image = data.img4, anchor = "e") 
    canvas.create_image(0, 0, image = data.img6, anchor = "nw")     
    canvas.create_image(0, data.height // 3 * 2, image = data.img5, anchor = "w") 
    canvas.create_image(data.width // 2, data.height - (262 // 2), image = data.img7)
    
    # home screen button
    canvas.create_image(data.width * 0.05, data.height * 0.95, image = data.imgBackButton, anchor = "s")
    pass

# Below "printFiles" function drawn from 15-112 courses notes and slightly 
# modified:
# <https://www.cs.cmu.edu/~112/notes/notes-recursive-applications.html>

def printFiles(path):
    if os.path.isfile(path):
        if "recording" in path:
            print(path)
    else:
        for filename in os.listdir(path):
            printFiles(path + "/" + filename)
            
def printFilesWrapper(path, lst):
    lst.append(printFiles(path))
    return lst
    
def drawSavedRecording(canvas, data):
    # background
    canvas.create_image(data.width // 2, data.height // 2, image = data.img11)
    
    # home screen button
    canvas.create_image(data.width * 0.05, data.height * 0.95, image = data.imgBackButton, anchor = "s")
    
    # saved recordings button
    canvas.create_image(data.width * 0.2, data.height * 0.3, image = data.img12)
    
    canvas.create_text(data.width * 0.2, data.height * 0.35, text = "Recordings", font = "courier 25 bold", fill = "white")
    
    # menu
    if data.dropDownMenu:
        #printFilesWrapper(data.mainPath, data.fileLst)
        canvas.create_image(data.width * 0.8, data.height * 0.4, image = data.img13)
        canvas.create_text(data.width * 0.8, data.height * 0.8, text = "Select any saved \nrecordings you \nwant to listen to!", font = "courier 20 bold", fill = "white")
        # canvas.create_text(data.width * 0.8, data.height * 0.4 + data.scrollUpDown, text = "\n".join(data.fileLst), font = "courier 20 bold", fill = "black")
        canvas.create_text(data.width * 0.8, data.height * 0.2, text = "recording1.wav", font = "courier 15 bold", fill = "black")
        canvas.create_text(data.width * 0.8, data.height * 0.4, text = "recording2.wav", font = "courier 15 bold", fill = "black")
        canvas.create_text(data.width * 0.8, data.height * 0.6, text = "recording3.wav", font = "courier 15 bold", fill = "black")
    
    
    
    pass
    
def redrawAll(canvas, data):
    # draw in canvas
    
    if data.isHomeScreen:
        # home screen
        drawHomeScreen(canvas, data)
        
    elif data.isPianoPracticeScreen:
        # piano practice screen
        drawPianoPractice(canvas, data)
        for fingerCircle in data.fingerCircles:
            fingerCircle.drawFingerPosition(canvas)
            
    elif data.isSongLearningScreen:
        # song learning screen
        drawSongLearning(canvas, data)
        
    elif data.isSavedRecordingsScreen:
        # saved recordings screen
        drawSavedRecording(canvas, data)
        
    pass

####################################
# use the run function as-is
####################################


def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    root = Tk()
    class Struct(object): pass
    
    
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 20 # milliseconds
    init(data)
    # create the root and the canvas
    
    root.resizable(width=False, height=False) # prevents resizing window
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    
    # Influenced by website: 
    # <https://www.c-sharpcorner.com/blogs/basics-for-displaying-image-in-
    # tkinter-python>
    # Image from: 
    # <https://pixabay.com/vectors/full-size-keyboard-music-piano-2024898/>
    # keyboardImg = ImageTk.PhotoImage(Image.open("keyboard"))
    #img = PhotoImage(file = "keyboard")
    
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(1000, 750)

