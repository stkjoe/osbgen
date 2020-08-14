from .object import Sprite, Animation, Audio

# Represents a Storyboard.
class Storyboard:
    def __init__(self, diffSpecific=False):
        self.diffSpecific = diffSpecific
        self.backgroundLayer = []
        self.failLayer = []
        self.passLayer = []
        self.foregroundLayer = []
        self.overlayLayer = []
        self.soundLayer = []

    # Compile the entire storyboard into output.txt
    def compile(self):
        with open("output.txt", "a") as file:
            file.write('[Events]\n')
            file.write('//Background and Video events\n')
            if self.diffSpecific:
                file.write('//Break Periods\n')

            # Write all Background sprites.
            file.write('Storyboard Layer 0 (Background)\n')
            for obj in self.backgroundLayer:
                obj.compile()

            # Write all Fail sprites.
            file.write('//Storyboard Layer 1 (Fail)\n')
            for obj in self.failLayer:
                obj.compile()

            # Write all Pass sprites.
            file.write('//Storyboard Layer 2 (Pass)\n')
            for obj in self.passLayer:
                obj.compile()

            # Write all Foreground sprites.
            file.write('//Storyboard Layer 3 (Foreground)\n')
            for obj in self.foregroundLayer:
                obj.compile()

            # Write all Overlay sprites.
            # Only valid for .osb files (not diff-specific).
            if not self.diffSpecific:
                file.write('//Storyboard Layer 3 (Foreground)\n')
                for obj in self.overlayLayer:
                    obj.compile()

            # Write all Sound sprites.
            file.write('//Storyboard Sound Samples\n')
            for obj in self.soundLayer:
                obj.compile()

        return 0

    # Add a Sprite to the Storyboard.
    def addSprite(self, path, layer, *, origin, posX, posY):
        sprite = Sprite(path, layer, origin=origin, posX=posX, posY=posY)
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
    def addAnimation(self, path, layer, *, origin, posX, posY, frameCount, frameDelay, loopType):
        animation = Animation(path, layer, origin=origin, posX=posX, frameCount=frameCount, frameDelay=frameDelay, loopType=loopType)
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
    def addAudio(self, path, layer, *, time, volume):
        audio = Audio(path, layer, time=time, volume=volume)
        self.soundLayer.append(audio)
        return audio
