import inspect

# Base parent object to be inherited from.
# Under no circumstances is it to be used in scripting.
class Event:
    def __init__(self, startTime, endTime, easing):
        # osu!-specific parameters.
        self.easing = easing
        self.startTime = startTime
        self.endTime = endTime

        # module-specific parameters.
    
    def compile(self, writer):
        writer.write(str(self))

# Represents a fade command.
class Fade(Event):
    def __init__(self, startTime, startFade, endTime, endFade, easing):
        super().__init__(startTime, endTime, easing)
        # osu!-specific parameters.
        self.startFade = startFade
        self.endFade = endFade

    def __str__(self):
        return ' F,{},{},{},{}{}\n'.format(self.easing, self.startTime, self.endTime,
                                           self.startFade,
                                           # If endFade is the same as startFade
                                           # Then it's fine to omit the last parameter.
                                           ",{}".format(self.endFade) if not (
                                                        self.endFade == self.startFade) 
                                                        else "")

# Represents a movementX command.
class MoveX(Event):
    def __init__(self, startTime, startX, endTime, endX, easing):
        super().__init__(startTime, endTime, easing)
        # osu!-specific parameters.
        self.startX = startX
        self.endX = endX

    def __str__(self):
        return ' MX,{},{},{},{}{}\n'.format(self.easing, self.startTime, self.endTime,
                                            self.startX,
                                            # If endX is the same as startX,
                                            # Then it's fine to omit the last parameter.
                                            ",{}".format(self.endX) if not (
                                                         self.endX == self.startX or
                                                         self.endX == "")
                                                         else "")

# Represents a movementY command.
class MoveY(Event):
    def __init__(self, startTime, startY, endTime, endY, easing):
        super().__init__(startTime, endTime, easing)
        # osu!-specific parameters.
        self.startY = startY
        self.endY = endY

    def __str__(self):
        return ' MY,{},{},{},{}{}\n'.format(self.easing, self.startTime, self.endTime,
                                            self.startY,
                                            # If endX is the same as startX,
                                            # Then it's fine to omit the last parameter.
                                            ",{}".format(self.endY) if not (
                                                         self.endY == self.startY or
                                                         self.endY == "")
                                                         else "")

# Represents a movement command.
class Move(MoveX, MoveY, Event):
    def __init__(self, startTime, startX, startY, endTime, endX, endY, easing):
        MoveX.__init__(self, startTime, startX, endTime, endX, easing)
        MoveY.__init__(self, startTime, startY, endTime, endY, easing)

    def __str__(self):
        return ' M,{},{},{},{},{}{}\n'.format(self.easing, self.startTime, self.endTime,
                                              self.startX, self.startY, 
                                              # If endX and endY are the same as startX and startY,
                                              # Then it's fine to omit the last two parameters.
                                              ",{},{}".format(self.endX, self.endY) if not (
                                                              self.endX == self.startX and 
                                                              self.endY == self.startY) 
                                                              else "")

# Represents a scale command.
class Scale(Event):
    def __init__(self, startTime, startScale, endTime, endScale, easing):
        super().__init__(startTime, endTime, easing)
        # osu!-specific parameters.
        self.startScale = startScale
        self.endScale = endScale

    def __str__(self):
        return ' S,{},{},{},{}{}\n'.format(self.easing, self.startTime, self.endTime,
                                           self.startScale,
                                           # If endFade is the same as startFade
                                           # Then it's fine to omit the last parameter.
                                           ",{}".format(self.endScale) if not (
                                                        self.endScale == self.startScale) 
                                                        else "")

# Represents a vector command.
class Vector(Event):
    def __init__(self, startTime, startX, startY, endTime, endX, endY, easing):
        super().__init__(startTime, endTime, easing)
        # osu!-specific parameters.
        self.startX = startX
        self.startY = startY
        self.endX = endX
        self.endY = endY

    def __str__(self):
        return ' V,{},{},{},{},{}{}\n'.format(self.easing, self.startTime, self.endTime,
                                              self.startX, self.startY,
                                              # If endFade is the same as startFade
                                              # Then it's fine to omit the last parameter.
                                              ",{},{}".format(self.endX, self.endY) if not (
                                                              self.endX == self.startX and 
                                                              self.endY == self.startY) 
                                                              else "")

# Represents a rotate command.
class Rotate(Event):
    def __init__(self, startTime, startRotate, endTime, endRotate, easing):
        super().__init__(startTime, endTime, easing)
        # osu!-specific parameters.
        self.startRotate = startRotate
        self.endRotate = endRotate

    def __str__(self):
        return ' R,{},{},{},{}{}\n'.format(self.easing, self.startTime, self.endTime,
                                           self.startRotate,
                                           # If endFade is the same as startFade
                                           # Then it's fine to omit the last parameter.
                                           ",{}".format(self.endRotate) if not (
                                                        self.endRotate == self.startRotate) 
                                                        else "")

# Represents a colour command.
class Colour(Event):
    def __init__(self, startTime, startR, startG, startB, endTime, endR, endG, endB, easing):
        super().__init__(startTime, endTime, easing)
        # osu!-specific parameters.
        self.startR = startR
        self.startG = startG
        self.startB = startB
        self.endR = endR
        self.endG = endG
        self.endB = endB

    def __str__(self):
        return ' C,{},{},{},{},{},{}{}\n'.format(self.easing, self.startTime, self.endTime,
                                                 self.startR, self.startG, self.startB,
                                                 # If endFade is the same as startFade
                                                 # Then it's fine to omit the last parameter.
                                                 ",{},{},{}".format(self.endR, self.endG, self.endB) if not (
                                                                    self.startR == self.endR and
                                                                    self.startG == self.endG and
                                                                    self.startB == self.endB) 
                                                                    else "")

# Represents an other parameter command.
class Parameter(Event):
    def __init__(self, startTime, endTime, param, easing):
        super().__init__(startTime, endTime, easing)
        # osu!-specific parameters.
        self.param = param

    def __str__(self):
        return ' P,{},{},{},{}\n'.format(self.easing, self.startTime, self.endTime,
                                         self.param)

# Base class for Loops and Triggers to inherit from.
# Different to events in that these contain events but different to Objects.
class Layer:
    def __init__(self):
        self.events = []

    def compile(self, writer):
        writer.write(str(self))

    def addEvent(self, event):
        self.events.append(event)
        return event

    def fade(self, startTime, startFade, endTime=None, endFade=None, *, easing=0):
        event = Fade(startTime, startFade, endTime, endFade, easing)
        return self.addEvent(event)

    def moveX(self, startTime, startX, endTime=None, endX=None, *, easing=0):
        event = MoveX(startTime, startX, endTime, endX, easing)
        return self.addEvent(event)

    def moveY(self, startTime, startY, endTime=None, endY=None, *, easing=0):
        event = MoveY(startTime, startY, endTime, endY, easing)
        return self.addEvent(event)

    def move(self, startTime, startX, startY, endTime=None, endX=None, endY=None, *, easing=0):
        event = Move(startTime, startX, startY, endTime, endX, endY, easing)
        return self.addEvent(event)

    def scale(self, startTime, startScale, endTime=None, endScale=None, *, easing=0):
        event = Scale(startTime, startScale, endTime, endScale, easing)
        return self.addEvent(event)

    def vector(self, startTime, startX, startY, endTime=None, endX=None, endY=None, *, easing=0):
        event = Vector(startTime, startX, startY, endTime, endX, endY, easing)
        return self.addEvent(event)

    def rotate(self, startTime, startRotate, endTime=None, endRotate=None, *, easing=0):
        event = Rotate(startTime, startRotate, endTime, endRotate, easing)
        return self.addEvent(event)

    def colourRGB(self, startTime, startR, startG, startB, endTime, endR=None, endG=None, endB=None, *, easing=0):
        event = Colour(startTime, startR, startG, startB, endTime, endR, endG, endB, easing)
        return self.addEvent(event)

    def colourHex(self, startTime, startHexcode, endTime=None, endHexcode=None, *, easing=0):
        # Convert hex to RGB
        colours = tuple(int(startHexcode.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
        endColours = tuple(int(endHexcode.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
        event = Colour(startTime, colours[0], colours[1], colours[2], endTime, endColours[0], endColours[1], endColours[2], easing)
        return self.addEvent(event)

    def flipX(self, startTime, endTime, *, easing=0):
        event = Parameter(startTime, endTime, "H", easing)
        return self.addEvent(event)

    def flipY(self, startTime, endTime, *, easing=0):
        event = Parameter(startTime, endTime, "V", easing)
        return self.addEvent(event)

    def additiveBlend(self, startTime, endTime, *, easing=0):
        event = Parameter(startTime, endTime, "A", easing)
        return self.addEvent(event)

# Represents a Loop command.
class Loop(Layer):
    def __init__(self, startTime, loopCount):
        super().__init__()
        # osu!-specific parameters.
        self.startTime = startTime
        self.loopCount = loopCount

    def __str__(self):
        return ' L,{},{}\n'.format(self.startTime, self.loopCount)

# Represents a Trigger command.
class Trigger(Layer):
    def __init__(self, triggerName, start, end):
        super().__init__()
        # osu!-specific parameters.
        self.triggerName = triggerName
        self.start = start
        self.end = end

    def __str__(self):
        return ' T,{},{},{}\n'.format(self.triggerName, self.start, self.end)
