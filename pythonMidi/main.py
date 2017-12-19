from pythonMidi import Launchpad
from pygame import midi
from time import sleep
import json
import numpy as np

class Options(Launchpad):
    COLOR = None
    toggle = False


    def __init__(self, readChannel, outputChannel):
        super().__init__(readChannel, outputChannel)

    def chooseColour(self):
        if self.toggle == False:
            for i in range(len(self.COORDS_SESSION)):
                for n in range(len(self.COORDS_SESSION[i])):
                    if [i, n] != [6,8] and [i, n ] != [7, 8]:
                        self.turnOnXY([i, n], self.COORDS_SESSION[i][n])
            self.COLOR = None

            while self.COLOR == None:
                b = self.readButtonPressed()
                if b[0] != None and b[1]:
                    y = b[0][0]
                    x = b[0][1]
                    if [y, x] != [6,8] and [y, x] != [7, 8]:
                        self.COLOR = self.COORDS_SESSION[y][x]


        
            for i in range(len(self.COORDS_SESSION)):
                for n in range(len(self.COORDS_SESSION[i])):
                    if [i, n] != [6,8] and [i, n ] != [7, 8]:
                        self.turnOnXY([i, n], self.COLOR)

            b = self.readButtonPressed()
            while True:
                b = self.readButtonPressed()
                if b[0] == [6, 8] and b[1]:
                    self.chooseColour()
                    print("Back")
                    return True

                elif b[0] == [7, 8] and b[1]:
                    self.reset()
                    self.toggle = True
                    print("Ok")
                    return False
                                 
                
        self.reset()

midi.init()
options = Options(1, 3)
options.reset()
options.chooseColour()
options.reset()