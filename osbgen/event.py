import inspect

# Base parent object to be inherited from.
# Under no circumstances is it to be used in scripting.
class Event:
    def __init__(self, startTime, endTime, *, easing):
        # osu!-specific parameters.
        self.easing = easing
        self.startTime = startTime
        self.endTime = endTime

        # module-specific parameters.

        lineNum = inspect.getframeinfo(inspect.stack()[1][0])
        self.valid = self.init_check(lineNum)

    def init_check(self, lineNum):
        # Checks to see if the current event is valid.
        errors = []

        # TODO: Add checks for general event.

        return errors
    
    def compile(self):
        if self.valid:
            for _ in self.valid:
                print(_)
            return bool(self.valid)

# Represents a fade command.
class Fade(Event):
    def __init__(self, startTime, endTime, startFade, endFade="", *, easing=0):
        super().__init__(startTime=startTime, endTime=endTime, easing=easing)
        # osu!-specific parameters.
        self.startFade = startFade
        self.endFade = endFade

    def init_check(self, lineNum):
        errors = Event.init_check(self, lineNum)
        # TODO: Add checks for movement event.
        return errors

    def compile(self):
        check = super().compile()
        if check:
            return check

        with open("output.txt", "a") as file:
            file.write((' F,{},{},{},{}{}\n').format(self.easing, self.startTime, self.endTime,
                                                     self.startFade,
                                                     # If endFade is the same as startFade
                                                     # Then it's fine to omit the last parameter.
                                                     ",{}".format(self.endFade) if not (
                                                                  self.endFade == self.startFade) 
                                                                  else ""))

        return 0

    def __str__(self):
        return self.compile()

# Represents a movementX command.
class MoveX(Event):
    def __init__(self, startTime, endTime, startX, endX="", *, easing):
        super().__init__(startTime=startTime, endTime=endTime, easing=easing)
        # osu!-specific parameters.
        self.startX = startX
        self.endX = endX

    def init_check(self, lineNum):
        errors = Event.init_check(self, lineNum)
        # TODO: Add checks for movementX event.
        return errors

    def compile(self):
        check = super().compile()
        if check:
            return check

        with open("output.txt", "a") as file:
            file.write((' MX,{},{},{},{}{}\n').format(self.easing, self.startTime, self.endTime,
                                                      self.startX,
                                                      # If endX is the same as startX,
                                                      # Then it's fine to omit the last parameter.
                                                      ",{}".format(self.endX) if not (
                                                                   self.endX == self.startX or
                                                                   self.endX == "")
                                                                   else ""))

        return 0

    def __str__(self):
        return self.compile()

# Represents a movementY command.
class MoveY(Event):
    def __init__(self, startTime, endTime, startY, endY="", *, easing):
        super().__init__(startTime=startTime, endTime=endTime, easing=easing)
        # osu!-specific parameters.
        self.startY = startY
        self.endY = endY

    def init_check(self, lineNum):
        errors = Event.init_check(self, lineNum)
        # TODO: Add checks for movementY event.
        return errors

    def compile(self):
        check = super().compile()
        if check:
            return check

        with open("output.txt", "a") as file:
            file.write((' MY,{},{},{},{}{}\n').format(self.easing, self.startTime, self.endTime,
                                                      self.startY,
                                                      # If endX is the same as startX,
                                                      # Then it's fine to omit the last parameter.
                                                      ",{}".format(self.endY) if not (
                                                                   self.endY == self.startY or
                                                                   self.endY == "")
                                                                   else ""))

        return 0

    def __str__(self):
        return self.compile()

# Represents a movement command.
class Move(MoveX, MoveY, Event):
    def __init__(self, startTime, endTime, startX, startY, endX="", endY="", *, easing):
        MoveX.__init__(self, startTime=startTime, endTime=endTime, easing=easing,
                       startX=startX, endX=endX)
        MoveY.__init__(self, startTime=startTime, endTime=endTime, easing=easing,
                       startY=startY, endY=endY)

    def init_check(self, lineNum):
        errors = MoveX.init_check(self, lineNum) + MoveY.init_check(self, lineNum)
        # TODO: Add checks for general movement event.
        return errors

    def compile(self):
        check = Event.compile(self)
        if check:
            return check

        with open("output.txt", "a") as file:
            file.write((' M,{},{},{},{},{}{}\n').format(self.easing, self.startTime, self.endTime,
                                                        self.startX, self.startY, 
                                                        # If endX and endY are the same as startX and startY,
                                                        # Then it's fine to omit the last two parameters.
                                                        ",{},{}".format(self.endX, self.endY) if not (
                                                                        self.endX == self.startX and 
                                                                        self.endY == self.startY) 
                                                                        else ""))

        return 0

    def __str__(self):
        return self.compile()

# Represents a scale command.
class Scale(Event):
    def __init__(self, startTime, endTime, startScale, endScale="", *, easing=0):
        super().__init__(startTime=startTime, endTime=endTime, easing=easing)
        # osu!-specific parameters.
        self.startScale = startScale
        self.endScale = endScale

    def init_check(self, lineNum):
        errors = Event.init_check(self, lineNum)
        # TODO: Add checks for scale event.
        return errors

    def compile(self):
        check = super().compile()
        if check:
            return check

        with open("output.txt", "a") as file:
            file.write((' S,{},{},{},{}{}\n').format(self.easing, self.startTime, self.endTime,
                                                     self.startScale,
                                                     # If endFade is the same as startFade
                                                     # Then it's fine to omit the last parameter.
                                                     ",{}".format(self.endScale) if not (
                                                                  self.endScale == self.startScale) 
                                                                  else ""))

        return 0

    def __str__(self):
        return self.compile()

# Represents a vector command.
class Vector(Event):
    def __init__(self, startTime, endTime, startX, startY, endX="", endY="", *, easing=0):
        super().__init__(startTime=startTime, endTime=endTime, easing=easing)
        # osu!-specific parameters.
        self.startX = startX
        self.startY = startY
        self.endX = endX
        self.endY = endY

    def init_check(self, lineNum):
        errors = Event.init_check(self, lineNum)
        # TODO: Add checks for scale event.
        return errors

    def compile(self):
        check = super().compile()
        if check:
            return check

        with open("output.txt", "a") as file:
            file.write((' V,{},{},{},{},{}{}\n').format(self.easing, self.startTime, self.endTime,
                                                        self.startX, self.startY,
                                                        # If endFade is the same as startFade
                                                        # Then it's fine to omit the last parameter.
                                                        ",{},{}".format(self.endX, self.endY) if not (
                                                                        self.endX == self.startX and 
                                                                        self.endY == self.startY) 
                                                                        else ""))

        return 0

    def __str__(self):
        return self.compile()

# Represents a rotate command.
class Rotate(Event):
    def __init__(self, startTime, endTime, startRotate, endRotate="", *, easing=0):
        super().__init__(startTime=startTime, endTime=endTime, easing=easing)
        # osu!-specific parameters.
        self.startRotate = startRotate
        self.endRotate = endRotate

    def init_check(self, lineNum):
        errors = Event.init_check(self, lineNum)
        # TODO: Add checks for scale event.
        return errors

    def compile(self):
        check = super().compile()
        if check:
            return check

        with open("output.txt", "a") as file:
            file.write((' R,{},{},{},{}{}\n').format(self.easing, self.startTime, self.endTime,
                                                     self.startRotate,
                                                     # If endFade is the same as startFade
                                                     # Then it's fine to omit the last parameter.
                                                     ",{}".format(self.endRotate) if not (
                                                                  self.endRotate == self.startRotate) 
                                                                  else ""))

        return 0

    def __str__(self):
        return self.compile()
