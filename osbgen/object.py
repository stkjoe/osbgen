import inspect
from .event import Fade, MoveX, MoveY, Move, Scale, Vector, Rotate, Colour, Parameter, Loop, Trigger

# Base parent object to be inherited from.
# Under no circumstances is it to be used in scripting.
class Object:
    def __init__(self, path, *, layer="Background", origin="Centre", posX=320, posY=240):
        # osu!-specific parameters.
        self.path = path
        self.layer = layer
        self.origin = origin
        self.posX = posX
        self.posY = posY

        # module-specific parameters.
        self.events = []
        self.posZ = 0
        
        lineNum = inspect.getframeinfo(inspect.stack()[1][0])
        self.valid = self.init_check(lineNum)

    def init_check(self, lineNum):
        # Checks to see if the current sprite is valid.
        errors = []

        # Check if sprite file is correct.
        if self.path.split(".")[-1] not in ["png", "jpg"]:
            errors.append(("[{}] Error: Expected "
                           "['png', 'jpg']. "
                           "Got {}.").format(lineNum, self.path.split(".")[-1]))

        # Checks if the layer is valid.
        if self.layer not in ["Background", "Foreground", "Pass", "Fail"]:
            errors.append(("[{}] Error: Expected "
                           "['Background', 'Foreground', 'Pass', 'Fail']. "
                           "Got {}.").format(lineNum, self.layer))
        
        # Checks if the origin is valid.
        if self.layer not in ["TopLeft", "TopCentre", "TopRight", 
                              "CentreLeft", "Centre", "CentreRight",
                             "BottomLeft", "BottomCentre", "BottomRight"]:
            errors.append(("[{}] Error: Expected "
                           "['TopLeft', 'TopCentre', 'TopRight', "
                           "'CentreLeft', 'Centre', 'CentreRight', "
                           "'BottomLeft', 'BottomCentre', 'BottomRight']. "
                           "Got {}.").format(lineNum, self.origin))

        return errors

    def compile(self):
        if self.valid:
            for error in self.valid:
                print(error)
            return bool(self.valid)

    def fade(self, startTime, endTime, startFade, endFade="", *, easing=0):
        fade = Fade(startTime, endTime, startFade, endFade=endFade, easing=easing)
        self.events.append(fade)
        return fade

    def moveX(self, startTime, endTime, startX, endX="", *, easing=0):
        moveX = MoveX(startTime, endTime, startX, endX, easing=easing)
        self.events.append(moveX)
        return moveX

    def moveY(self, startTime, endTime, startY, endY="", *, easing=0):
        moveY = MoveY(startTime, endTime, startY, endY, easing=easing)
        self.events.append(moveY)
        return moveY

    def move(self, startTime, endTime, startX, startY, endX="", endY="", *, easing=0):
        move = Move(startTime, endTime, startX, startY, endX, endY, easing=easing)
        self.events.append(move)
        return move

    def scale(self, startTime, endTime, startScale, endScale="", *, easing=0):
        scale = Scale(startTime, endTime, startScale, endScale, easing=0)
        self.events.append(scale)
        return scale

    def vector(self, startTime, endTime, startX, startY, endX="", endY="", *, easing=0):
        vector = Vector(startTime, endTime, startX, startY, endX, endY, easing=0)
        self.events.append(vector)
        return vector

    def rotate(self, startTime, endTime, startRotate, endRotate="", *, easing=0):
        rotate = Rotate(startTime, endTime, startRotate, endRotate, easing=0)
        self.events.append(rotate)
        return rotate

    def colourRGB(self, startTime, endTime, startR, startG, startB, endR="", endG="", endB="", *, easing=0):
        colour = Colour(startTime, endTime, startR, startG, startB, endR, endG, endB, easing=easing)
        self.events.append(colour)
        return colour

    def colourHex(self, startTime, endTime, hexcode, endHexcode, *, easing=0):
        colours = tuple(int(hexcode[i:i+2], 16) for i in (0, 2, 4))
        endColours = tuple(int(endHexcode[i:i+2], 16) for i in (0, 2, 4))
        colour = Colour(startTime, endTime, colours[0], colours[1], colours[2], endColours[0], endColours[1], endColours[2], easing=easing)
        self.events.append(colour)
        return colour

    def trigger(self, triggerName, start, end):
        trigger = Trigger(triggerName, start, end)
        self.events.append(trigger)
        return trigger

    def loop(self, startTime, loopCount):
        loop = Loop(startTime, loopCount)
        self.events.append(loop)
        return loop

    def flipX(self, startTime, endTime, easing=0):
        parameter = Parameter(startTime, endTime, "H", easing=0)
        self.events.append(parameter)
        return parameter

    def flipY(self, startTime, endTime, easing=0):
        parameter = Parameter(startTime, endTime, "V", easing=0)
        self.events.append(parameter)
        return parameter

    def additiveBlend(self, startTime, endTime, easing=0):
        parameter = Parameter(startTime, endTime, "A", easing=0)
        self.events.append(parameter)
        return parameter

# Represents a normal sprite.
class Sprite(Object):
    def __init__(self, path, layer="Foreground", *, origin="Centre", posX=320, posY=240):
        super().__init__(path, layer=layer, origin=origin, posX=posX, posY=posY)

    def compile(self):
        check = super().compile()
        if check:
            return check

        with open("output.txt", "a") as file:
            # The base sprite line.
            file.write(('Sprite,{},{},"{}",{},{}\n').format(self.layer, self.origin, self.path,
                                                            self.posX, self.posY))
            for event in self.events:
                event.compile()

        return 0

    def __str__(self):
        return self.compile()

# Represents an animation sprite.
class Animation(Object):
    def __init__(self, path, layer="Foreground", *, origin="Centre", posX=320, posY=240,
                 frameCount, frameDelay, loopType="loopForever"):
        super().__init__(path, layer=layer, origin=origin, posX=posX, posY=posY)
        # Additional osu!-specific parameters.
        self.frameCount = frameCount
        self.frameDelay = frameDelay
        self.loopType = loopType

    def init_check(self, lineNum):
        errors = Object.init_check(self, lineNum)
        # Animation-specific checks.

        # Checks if frameCount is valid.
        if self.frameCount <= 0:
            errors.append(("[{}] Error: Invalid frameCount. "
                            "Must be greater than 0. "
                            "Got {}.").format(lineNum, self.frameCount))
    
        # Checks if loopType is valid.
        if self.loopType not in ["LoopForever", "LoopOnce"]:
            errors.append(("[{}] Error: Expected "
                            "['LoopForever', 'LoopOnce']. "
                            "Got {}.").format(lineNum, self.loopType))
        return errors

    def compile(self):
        super().compile()

        with open("output.txt", "a") as file:
            # The base sprite line.
            file.write(('Animation,{},{},"{}",{},{},{},{},{}\n').format(self.layer, self.origin, self.path,
                                                          self.posX, self.posY, self.frameCount,
                                                          self.frameDelay, self.loopType))
            for event in self.events:
                event.compile()

    def __str__(self):
        return self.compile()

# Represents an audio sprite.
class Audio:
    def __init__(self, path, layer="Foreground", *, time, volume=100):
        # osu!-specific parameters.
        self.path = path
        self.time = time
        self.layer = layer
        self.volume = volume

        # module-specific parameters.
        self.events = []

        lineNum = inspect.getframeinfo(inspect.stack()[1][0])
        self.valid = self.init_check(lineNum)

    def init_check(self, lineNum):
        errors = []
        # Audio-specific checks.
        
        # Check if audio file is correct.
        if self.path.split(".")[-1] not in ["wav", "mp3", "ogg"]:
            errors.append(("[{}] Error: Expected "
                           "['wav', 'mp3', 'ogg']. "
                           "Got {}.").format(lineNum, self.path.split(".")[-1]))

        # Checks if the layer is valid.
        if self.layer not in ["Background", "Foreground", "Pass", "Fail"]:
            errors.append(("[{}] Error: Expected "
                           "['Background', 'Foreground', 'Pass', 'Fail']. "
                           "Got {}.").format(lineNum, self.layer))

        # Checks if the volume is valid.
        try:
            if not 0 <= float(self.volume) <= 100:
                errors.append(("[{}] Error: Volume must be between 0 and 100."
                               "Got {}.").format(lineNum, self.volume))

        except ValueError:
            errors.append(("[{}] Error: Expected an integer."
                           "Got {}.").format(lineNum, self.volume))

        return errors


    def compile(self):
        if self.valid:
            return self.valid

        with open("output.txt", "a") as file:
            # The base sprite line.
            file.write(('Sample,{},{},"{}",{}\n').format(self.time, self.layer, self.path, self.volume))
            for event in self.events:
                event.compile()

        return 0

    def __str__(self):
        return self.compile()
