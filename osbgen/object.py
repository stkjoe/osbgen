from .event import Fade, MoveX, MoveY, Move, Scale, Vector, Rotate, Colour, Parameter, Loop, Trigger

# Base parent object to be inherited from.
# Under no circumstances is it to be used in scripting.
class Object:
    def __init__(self, path, layer, origin, posX, posY):
        # osu!-specific parameters.
        self.path = path
        self.layer = layer
        self.origin = origin
        self.posX = posX
        self.posY = posY

        # module-specific parameters.
        self.events = []
        self.posZ = 0

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

    def trigger(self, triggerName, start, end):
        event = Trigger(triggerName, start, end)
        return self.addEvent(event)

    def loop(self, startTime, loopCount):
        event = Loop(startTime, loopCount)
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

    def compile(self, writer):
        writer.write(str(self))

        for event in self.events:
            event.compile(writer)

# Represents a normal sprite.
class Sprite(Object):
    def __init__(self, path, layer, origin, posX, posY):
        super().__init__(path, layer, origin, posX, posY)

    def __str__(self):
        return 'Sprite,{},{},"{}",{},{}\n'.format(self.layer, self.origin, self.path,
                                                     self.posX, self.posY)

# Represents an animation sprite.
class Animation(Object):
    def __init__(self, path, frameCount, frameDelay, layer, origin, posX, posY, loopType):
        super().__init__(path, layer, origin, posX, posY)
        # Additional osu!-specific parameters.
        self.frameCount = frameCount
        self.frameDelay = frameDelay
        self.loopType = loopType

    def __str__(self):
        return 'Animation,{},{},"{}",{},{},{},{},{}\n'.format(self.layer, self.origin, self.path,
                                                               self.posX, self.posY, self.frameCount,
                                                                self.frameDelay, self.loopType)

# Represents an audio sprite.
class Audio:
    def __init__(self, path, time, layer, volume):
        # osu!-specific parameters.
        self.path = path
        self.time = time
        self.layer = layer
        self.volume = volume

        # module-specific parameters.
        self.events = []

    def compile(self, writer):
        writer.write(str(self))

        for event in self.events:
            event.compile()

    def __str__(self):
        return 'Sample,{},{},"{}",{}\n'.format(self.time, self.layer, self.path, self.volume)
