import inspect
from event import Event

class Sprite:
    def __init__(self, path, layer="Background", origin="Centre", posX=320, posY=240, 
                 animation=False, frameCount=0, frameDelay=0, loopType="LoopForever"):
        # osu!-specific parameters.
        self.path = path
        self.layer = layer
        self.origin = origin
        self.posX = posX
        self.posY = posY
        if animation:
            self.frameCount = frameCount
            self.frameDelay = frameDelay
            self.loopType = loopType

        # module-specific parameters.
        self.animation = animation
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

        # Animation-specific checks.
        if self.animation:
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
        lines = []
        # The base sprite line.
        lines.append(('{},{},{},"{}",{},{}{}').format("Animation" if self.animation else "Sprite",
                                                      self.layer, self.origin, self.path, self.posX, 
                                                      self.posY, ",{},{},{}".format(
                                                          self.frameCount, self.frameDelay, 
                                                          self.loopType) if self.animation else ""))
        for event in self.events:
            lines.append(event.compile())
        return lines

    def __str__(self):
        return self.compile()
