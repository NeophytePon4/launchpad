from pygame import midi
from time import sleep
import json
import pprint
import numpy as np


class Launchpad():
    
    COORDS_DRUM=[
        [64, 65, 66, 67, 96, 97, 98, 99, 100],
        [60, 61, 62, 63, 92, 93, 94, 95, 101],
        [56, 57, 58, 59, 88, 89, 90, 91, 102],
        [52, 53, 54, 55, 84, 85, 86, 87, 103],
        [48, 49, 50, 51, 80, 81, 82, 83, 104],
        [44, 45, 46, 47, 76, 77, 78, 79, 105],
        [40, 41, 42, 43, 72, 73, 74, 75, 106],
        [36, 37, 38, 39, 68, 69, 70, 71, 107]
        ]

    COORDS_SESSION=[
        [81, 82, 83, 84, 85, 86, 87, 88, 89],
        [71, 72, 73, 74, 75, 76, 77, 78, 79],
        [61, 62, 63, 64, 65, 66, 67, 68, 69],
        [51, 52, 53, 54, 55, 56, 57, 58, 59],
        [41, 42, 43, 44, 45, 46, 47, 48, 49],
        [31, 32, 33, 34, 35, 36, 37, 38, 39],
        [21, 22, 23, 24, 25, 26, 27, 28, 29],
        [11, 12, 13, 14, 15, 16, 17, 18, 19]
        ]

    def __init__(self, readChannel, outputChannel):
        self.read = midi.Input(readChannel)
        self.output = midi.Output(outputChannel)
              

    def turnOnXY(self, lightXY, color):
        self.output.note_on(note=Launchpad.COORDS_SESSION[lightXY[0]][lightXY[1]], velocity=color, channel=0)


    def turnOn(self, light, color):
        self.output.note_on(note=light, velocity=color, channel=0)

    def turnOffXY(self, lightXY):
        self.output.note_off(note=Launchpad.COORDS_SESSION[lightXY[0]][lightXY[1]], channel=0)

    def loadingAnimation(self):
        for i in range(11, 100):
            self.output.note_on(note=i, velocity=i-10, channel=0)
            sleep(0.01)
    
    def reset(self):
        for i in range(110):
            self.output.note_off(note=i, channel=0)

    def printLetter(self, letter, color, **kwargs):
        length = 2
        if "time" in kwargs.keys():
            length = kwargs["time"]

        for i in range(len(letter)):
            self.turnOnXY(letter[i], color)

        sleep(length)
        self.reset()

    def scrollLetter(self, letter, color, speed, amount):

        for i in range(len(letter)):
            letter[i][1] += 9
        
        for i in range(40):

            for n in range(len(letter)):
                try:
                    self.turnOnXY(letter[n],33)
                except:
                    pass
            
            for n in range(len(letter)):
                letter[n][1] -= 1
                print(letter[n])
                if letter[n][1] < -9:
                    letter[n][1] += abs(letter[n][1]) - 1
            sleep(speed)
            self.reset()
        
    def scrollWord(self, word, color, speed):
        debug = open("Debug.json", "w")
        word = word.upper()
        letters = [[] for x in range(len(word))]

        letters = self.getWord(word)

        #Starting Pos Loop
        for i in range(len(letters)):
            for n in range(len(letters[i])):
                letters[i][n][1] += 9 * i

        
        #Scroll Loop
        for i in range(10 * len(letters)):

            #Print Loop
            for n in range(len(letters)):
                for x in range(len(letters[n])):
                    print(len(letters[n]))
                    try:
                        self.turnOnXY(letters[n][x],33)
                        print(letters[n][x])
                    except IndexError:
                        pass
                    

            #Change Coords Loop
            for n in range(len(letters)):
                for x in range(len(letters[n])):
                    letters[n][x][1] -= 1
                    if letters[n][x][1] < 0:
                        letters[n][x][1] = -60
                    

            self.reset()

        debug.write(str(letters))

    @staticmethod
    def getLetter(letter):
        chars = json.load(open("Chars.json"))
        letters = chars["letters"]
        print("----------------")
        print(letters[letter])
        print("--------------")
        return letters[letter]

    @staticmethod
    def getWord(word):
        chars = json.load(open("Chars.json"))
        letters = chars["letters"]
        outp = [[] for x in range(len(word))]
        for i in range(len(word)):
            print(word[i])
            outp[i] = letters[word[i]]

        
        return outp

    def readButtonPressed(self):
        coord = None
        state = None
        r = self.read.read(1)
        if len(r) > 0 and r[0][0][2] == 127:
            try:         
                for i, subList in enumerate(self.COORDS_SESSION):
                    if r[0][0][1] in subList:

                        place = subList.index(r[0][0][1])
                        
                        coord = [i, place]
                        state = True
                        
            except IndexError as e:
                coord = None

        elif len(r) > 0 and r[0][0][2] == 0:
            try:         
                for i, subList in enumerate(self.COORDS_SESSION):
                    if r[0][0][1] in subList:

                        place = subList.index(r[0][0][1])
                        
                        coord = [i, place]
                        state = False
                        
            except IndexError as e:
                coord = None

        else:
            coord = None
            
        return coord, state

if __name__ == "__main__":
    midi.init()
    for i in range(midi.get_count()):
        print(midi.get_device_info(i))

    #rdr = int(input("Input Channel:"))
    #out = int(input("Output Channel:"))
    rdr = 1
    out = 3
    launchpadMK2 = Launchpad(rdr, out)
    launchpadMK2.reset()




    while True:
        print(launchpadMK2.readButtonPressed())

    launchpadMK2.reset()
    midi.quit()


