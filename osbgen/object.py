import inspect
from event import Event

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

# Represents a normal sprite.
class Sprite(Object):
    def __init__(self, path, layer="Background", origin="Centre", posX=320, posY=240):
        super().__init__(path, layer=layer, origin=origin, posX=posX, posY=posY)

    def compile(self):
        with open("output.txt", "a") as file:
            # The base sprite line.
            file.write(('Sprite,{},{},"{}",{},{}\n').format(self.layer, self.origin, self.path,
                                                          self.posX, self.posY))
            for event in self.events:
                event.compile()

    def __str__(self):
        return self.compile()

# Represents an animation sprite.
class Animation(Object):
    def __init__(self, path, *, layer="Background", origin="Centre", posX=320, posY=240,
                 frameCount, frameDelay, loopType="loopForever"):
        Object.__init__(self, path, layer=layer, origin=origin, posX=posX, posY=posY)
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
    def __init__(self, path, *, time, layer="Background", volume=100):
        # osu!-specific parameters.
        self.path = path
        self.time = time
        self.layer = layer
        self.volume = volume

        # module-specific parameters.
        self.events = []

    def compile(self):
        with open("output.txt", "a") as file:
            # The base sprite line.
            file.write(('Sample,{},{},"{}",{}\n').format(self.time, self.layer, self.path, self.volume))
            for event in self.events:
                event.compile()

    def __str__(self):
        return self.compile()
