from .event import Loop, Trigger, Layer

# Base parent object to be inherited from.
class Object(Layer):
    def __init__(self, path, layer, origin, posX, posY):
        super().__init__()
        # osu!-specific parameters.
        self.path = path
        self.layer = layer
        self.origin = origin
        self.posX = posX
        self.posY = posY

        # module-specific parameters.
        self.current = {
            "Move": {
                "Value": [posX, posY],
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

    def trigger(self, triggerName, start, end):
        event = Trigger(triggerName, start, end)
        return self.addEvent(event)

    def loop(self, startTime, loopCount):
        event = Loop(startTime, loopCount)
        return self.addEvent(event)

    def compile(self, writer):
        super().compile(writer)
        for event in self.events:
            self.current.update(event.compile(writer, self.current))

# Represents a normal sprite.
class Sprite(Object):
    def __init__(self, path, layer, origin, posX, posY):
        super().__init__(path, layer, origin, posX, posY)

    def getLine(self):
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

    def getLine(self):
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
        writer.write(self.getLine())

        for event in self.events:
            event.compile()

    def getLine(self):
        return 'Sample,{},{},"{}",{}\n'.format(self.time, self.layer, self.path, self.volume)
