from math import pi

# Base class for Objects, Loops, and Triggers to inherit from.
class Layer:
    def __init__(self):
        # module-specific parameters.
        self.events = []
        self.z = 0

        self.current = {
            "Move": {
                "Value": [0, 0],
                "Time": 0
            },
            "MoveX": {
                "Value": 0,
                "Time": 0
            },
            "MoveY": {
                "Value": 0,
                "Time": 0
            },
            "Fade": {
                "Value": 1,
                "Time": 0
            },
            "Rotate": {
                "Value": 1,
                "Time": 0
            },
            "Colour": {
                "Value": [0, 0, 0],
                "Time": 0
            },
            "Scale": {
                "Value": 1,
                "Time": 0
            },
            "Vector": {
                "Value": [1, 1],
                "Time": 0,
            },
            "Time": 0,
            "X": 0,
            "Y": 0
        }

    # Empty method because it is always overriden.
    def getLine(self):
        return ""

    def compile(self, writer):
        writer.write(self.getLine())
        return {}

    def addEvent(self, event):
        self.events.append(event)
        return event

    def updateCurrent(self, event):
        self.current[event.__class__.__name__]["Value"] = event.getEndValue()
        self.current[event.__class__.__name__]["Time"] = event.getEndTime()
        self.current["Time"] = event.getEndTime()

    def fade(self, startTime, startFade, endTime="", endFade="", *, easing=0):
        event = Fade(startTime, startFade, endTime, endFade, easing)
        self.updateCurrent(event)
        return self.addEvent(event)

    def moveX(self, startTime, startX, endTime="", endX="", *, easing=0):
        event = MoveX(startTime, startX, endTime, endX, easing)
        self.updateCurrent(event)
        return self.addEvent(event)

    def moveY(self, startTime, startY, endTime="", endY="", *, easing=0):
        event = MoveY(startTime, startY, endTime, endY, easing)
        self.updateCurrent(event)
        return self.addEvent(event)

    def move(self, startTime, startX, startY, endTime="", endX="", endY="", *, easing=0):
        event = Move(startTime, startX, startY, endTime, endX, endY, easing)
        self.updateCurrent(event)
        return self.addEvent(event)

    def scale(self, startTime, startScale, endTime="", endScale="", *, easing=0):
        event = Scale(startTime, startScale, endTime, endScale, easing)
        self.updateCurrent(event)
        return self.addEvent(event)

    def vector(self, startTime, startX, startY, endTime="", endX="", endY="", *, easing=0):
        event = Vector(startTime, startX, startY, endTime, endX, endY, easing)
        self.updateCurrent(event)
        return self.addEvent(event)

    def rotate(self, startTime, startRotate, endTime="", endRotate="", *, easing=0):
        event = Rotate(startTime, startRotate, endTime, endRotate, easing)
        self.updateCurrent(event)
        return self.addEvent(event)

    def rotateDeg(self, startTime, startRotate, endTime="", endRotate="", *, easing=0):
        event = Rotate(startTime, startRotate * pi / 180, endTime, endRotate * pi / 180, easing)
        self.updateCurrent(event)
        return self.addEvent(event)

    def colourRGB(self, startTime, startR, startG, startB, endTime, endR="", endG="", endB="", *, easing=0):
        event = Colour(startTime, startR, startG, startB, endTime, endR, endG, endB, easing)
        self.updateCurrent(event)
        return self.addEvent(event)

    def colourHex(self, startTime, startHexcode, endTime="", endHexcode="", *, easing=0):
        # Convert hex to RGB
        colours = tuple(int(startHexcode.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
        if endHexcode != "":
            endColours = tuple(int(endHexcode.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
        else:
            endColours = ("", "", "")
        event = Colour(startTime, colours[0], colours[1], colours[2], endTime, endColours[0], endColours[1], endColours[2], easing)
        self.updateCurrent(event)
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

# Base parent event to be inherited from.
class Event:
    def __init__(self, startTime, endTime, easing):
        # osu!-specific parameters.
        self.easing = easing
        self.startTime = startTime
        self.endTime = endTime
        self.startValue = ""
        self.endValue = ""
        self.eventType = ""

        # module-specific parameters.

    def checkEnding(self):
        if self.endValue == "":
            self.endValue = self.startValue
        elif type(self.endValue) is list:
            for i in self.endValue:
                if i != "":
                    return
            self.endValue = self.startValue

    def getStartValue(self):
        if type(self.startValue) in [int, float]:
            return str(self.startValue)
        return self.startValue

    def getEndValue(self):
        return self.endValue if self.endValue != "" else self.startValue

    def getEndTime(self):
        return self.endTime if self.endTime != "" else self.startTime
    
    def compile(self, writer):
        writer.write(self.getLine())

    def getLine(self):

        def toStringList(val):
            if type(val) in [int, float]:
                val = [str(val)]
            return ",".join([str(i) for i in val])

        return ' {},{},{},{},{}{}\n'.format(self.eventType, self.easing, self.startTime,
                                            self.endTime, toStringList(self.startValue),
                                            ",{}".format(toStringList(self.endValue)) if (
                                                         self.startValue != self.endValue)
                                                         else "")


# Represents a fade command.
class Fade(Event):
    def __init__(self, startTime, startFade, endTime, endFade, easing):
        super().__init__(startTime, endTime, easing)
        # osu!-specific parameters.
        self.startValue = startFade
        self.endValue = endFade
        self.eventType = "F"
        self.checkEnding()

# Represents a movement command.
class Move(Event):
    def __init__(self, startTime, startX, startY, endTime, endX, endY, easing):
        super().__init__(startTime, endTime, easing)
        self.startValue = [startX, startY]
        self.endValue = [endX, endY]
        self.eventType = "M"
        self.checkEnding()

# Represents a movementX command.
class MoveX(Event):
    def __init__(self, startTime, startX, endTime, endX, easing):
        super().__init__(startTime, endTime, easing)
        # osu!-specific parameters.
        self.startValue = startX
        self.endValue = endX
        self.eventType = "MX"
        self.checkEnding()

# Represents a movementY command.
class MoveY(Event):
    def __init__(self, startTime, startY, endTime, endY, easing):
        super().__init__(startTime, endTime, easing)
        # osu!-specific parameters.
        self.startValue = startY
        self.endValue = endY
        self.eventType = "MY"
        self.checkEnding()

# Represents a scale command.
class Scale(Event):
    def __init__(self, startTime, startScale, endTime, endScale, easing):
        super().__init__(startTime, endTime, easing)
        # osu!-specific parameters.
        self.startValue = startScale
        self.endValue = endScale
        self.eventType = "S"
        self.checkEnding()

# Represents a vector command.
class Vector(Event):
    def __init__(self, startTime, startX, startY, endTime, endX, endY, easing):
        super().__init__(startTime, endTime, easing)
        # osu!-specific parameters.
        self.startValue = [startX, startY]
        self.endValue = [endX, endY]
        self.eventType = "V"

# Represents a rotate command.
class Rotate(Event):
    def __init__(self, startTime, startRotate, endTime, endRotate, easing):
        super().__init__(startTime, endTime, easing)
        # osu!-specific parameters.
        self.startValue = startRotate
        self.endValue = endRotate
        self.eventType = "R"
        self.checkEnding()

# Represents a colour command.
class Colour(Event):
    def __init__(self, startTime, startR, startG, startB, endTime, endR, endG, endB, easing):
        super().__init__(startTime, endTime, easing)
        # osu!-specific parameters.
        self.startValue = [startR, startG, startB]
        self.endValue = [endR, endG, endB]
        self.eventType = "C"
        self.checkEnding()

# Represents an other parameter command.
class Parameter(Event):
    def __init__(self, startTime, endTime, param, easing):
        super().__init__(startTime, endTime, easing)
        # osu!-specific parameters.
        self.startValue = param
        # Setting endValue to param so the string builder will ignore.
        self.endValue = param

# Represents a Loop command.
class Loop(Layer):
    def __init__(self, startTime, loopCount):
        super().__init__()
        # osu!-specific parameters.
        self.startTime = startTime
        self.loopCount = loopCount

    def compile(self, writer):
        super().compile(writer)
        for event in self.events:
            writer.write(" ")
            event.compile(writer)

    def getLine(self):
        return ' L,{},{}\n'.format(self.startTime, self.loopCount)

# Represents a Trigger command.
class Trigger(Layer):
    def __init__(self, triggerName, start, end):
        super().__init__()
        # osu!-specific parameters.
        self.triggerName = triggerName
        self.start = start
        self.end = end

    def compile(self, writer):
        super().compile(writer)
        for event in self.events:
            writer.write(" ")
            event.compile(writer)

    def getLine(self):
        return ' T,{},{},{}\n'.format(self.triggerName, self.start, self.end)
