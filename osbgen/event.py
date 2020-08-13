import inspect

# Base parent object to be inherited from.
# Under no circumstances is it to be used in scripting.
class Event:
    def __init__(self, eventType, startTime, endTime=None, *, easing=0):
        # osu!-specific parameters.
        self.eventType = eventType
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

# Represents a movement command.
class Move(Event):
    def __init__(self, eventType, startTime, endTime, startX, startY, *, endX=startX, endY=startY, easing):
        super().__init__(eventType=eventType, startTime=startTime, endTime=endTime, easing=easing)
        # osu!-specific parameters.
        self.startX = startX
        self.startY = startY
        self.endX = endX
        self.endY = endY

    def init_check(self, lineNum):
        errors = Event.init_check(self, lineNum)
        # TODO: Add checks for movement event.
        return errors

    def compile(self):
        check = super().compile()
        if check:
            return check

        with open("output.txt", "a") as file:
            # The base sprite line.
            file.write((' M,{},{},{},{},{}{}\n').format(self.easing, self.startTime, self.endTime,
                                                        self.startX, self.startY, 
                                                        # If endX and endY are the same as startX and startY,
                                                        # Then it's fine to omit the last two parameters.
                                                        ",{},{}".format(self.endX, self.endY) if not (
                                                                        self.endX == self.startX or 
                                                                        self.endY == self.startY) 
                                                                        else ""))

        return 0

    def __str__(self):
        return self.compile()
