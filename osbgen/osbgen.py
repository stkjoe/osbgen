from .object import Sprite, Animation, Audio
from .writer import Writer

# Represents a Storyboard.
class Storyboard:
    def __init__(self, *, diffSpecific=False):
        self.diffSpecific = diffSpecific
        self.background = ""
        self.backgroundLayer = []
        self.failLayer = []
        self.passLayer = []
        self.foregroundLayer = []
        self.overlayLayer = []
        self.soundLayer = []

    # Compile the entire storyboard into output.txt
    def compile(self):

        # pre-sort lists to z-index
        for x in [self.backgroundLayer, self.failLayer, self.passLayer, 
                  self.foregroundLayer, self.overlayLayer]:
            if len(x) > 0:
                x.sort(key=lambda y: y.z)

        writer = Writer()

        writer.write('[Events]\n')
        writer.write('//Background and Video events\n')
        if self.background != "":
            writer.write('0,0,{},0,0\n'.format(self.background))
        if self.diffSpecific:
            writer.write('//Break Periods\n')

        # Write all Background sprites.
        writer.write('//Storyboard Layer 0 (Background)\n')
        for obj in self.backgroundLayer:
            obj.compile(writer)

        # Write all Fail sprites.
        writer.write('//Storyboard Layer 1 (Fail)\n')
        for obj in self.failLayer:
            obj.compile(writer)

        # Write all Pass sprites.
        writer.write('//Storyboard Layer 2 (Pass)\n')
        for obj in self.passLayer:
            obj.compile(writer)

        # Write all Foreground sprites.
        writer.write('//Storyboard Layer 3 (Foreground)\n')
        for obj in self.foregroundLayer:
            obj.compile(writer)

        # Write all Overlay sprites.
        # Only valid for .osb files (not diff-specific).
        if not self.diffSpecific:
            writer.write('//Storyboard Layer 4 (Overlay)\n')
            for obj in self.overlayLayer:
                obj.compile(writer)

        # Write all Sound sprites.
        writer.write('//Storyboard Sound Samples\n')
        for obj in self.soundLayer:
            obj.compile(writer)

        return 0

    # Add a background to the Storyboard.
    def addBackground(self, path):
        self.background = path

    # Add a Sprite to the Storyboard.
    def addSprite(self, path, *, layer="Foreground", origin="Centre", posX=320, posY=240):
        sprite = Sprite(path, layer, origin, posX, posY)
        if layer == "Background":
            self.backgroundLayer.append(sprite)
        elif layer == "Pass":
            self.passLayer.append(sprite)
        elif layer == "Fail":
            self.failLayer.append(sprite)
        elif layer == "Foreground":
            self.foregroundLayer.append(sprite)
        elif layer == "Overlay":
            if self.diffSpecific:
                print("Error: You cannot add to the Overlay layer for a diff-specific storyboard.")
                return 1
            self.overlayLayer.append(sprite)
        else:
            return 1
        return sprite

    # Add an Animation to the Storyboard.
    def addAnimation(self, path, frameCount, frameDelay, *, layer="Foreground", origin="Centre", posX=320, posY=240, loopType="LoopForever"):
        animation = Animation(path, layer, origin, posX, posY, frameCount, frameDelay, loopType)
        if layer == "Background":
            self.backgroundLayer.append(animation)
        elif layer == "Pass":
            self.passLayer.append(animation)
        elif layer == "Fail":
            self.failLayer.append(animation)
        elif layer == "Foreground":
            self.foregroundLayer.append(animation)
        elif layer == "Overlay":
            if self.diffSpecific:
                print("Error: You cannot add to the Overlay layer for a diff-specific storyboard.")
                return 1
            self.overlayLayer.append(animation)
        else:
            return 1
        return animation

    # Add an Audio sample to the Storyboard.
    def addAudio(self, path, time, *, layer="Foreground", volume=100):
        audio = Audio(path, time, layer, volume)
        self.soundLayer.append(audio)
        return audio
