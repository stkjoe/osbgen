import unittest
from osbgen.osbgen import Storyboard

# These tests should be run every time before a push.
# python -m unittest tests/unittests.py
class TestModule(unittest.TestCase):

    # Prior set-up. Creates a storyboard object.
    # Also preloads with various sprites.
    def setUp(self):
        self.sb = Storyboard()
        self.sprite_0 = self.sb.addSprite("sprite.png")
        self.sprite_1 = self.sb.addSprite("sprite.png")
        self.animation = self.sb.addAnimation("animation.png", 10, 5)
        self.audio = self.sb.addAudio("audio.mp3", 0)

    def tearDown(self):
        del self.sb

    # Test the creation of a storyboard object.
    def testStoryboard(self):
        self.assertTrue(self.sb.__class__.__name__ == "Storyboard")
        # Sprites and audio was added in setup.
        self.assertEqual(len(self.sb.backgroundLayer), 0)
        self.assertEqual(len(self.sb.failLayer), 0)
        self.assertEqual(len(self.sb.passLayer), 0)
        self.assertEqual(len(self.sb.foregroundLayer), 3)
        self.assertEqual(len(self.sb.overlayLayer), 0)
        self.assertEqual(len(self.sb.soundLayer), 1)

    # Test the addition of a background sprite.
    def testStoryboardAddSpriteBackground(self):
        self.sb.addSprite("test.jpg", layer="Background")
        self.assertEqual(len(self.sb.backgroundLayer), 1)

    # Test the addition of a fail sprite.
    def testStoryboardAddSpriteFail(self):
        self.sb.addSprite("test.jpg", layer="Fail")
        self.assertEqual(len(self.sb.failLayer), 1)

    # Test the addition of a pass sprite.
    def testStoryboardAddSpritePass(self):
        self.sb.addSprite("test.jpg", layer="Pass")
        self.assertEqual(len(self.sb.passLayer), 1)

    # Test the addition of a foreground sprite.
    def testStoryboardAddSpriteForeground(self):
        self.sb.addSprite("test.jpg")
        self.assertEqual(len(self.sb.foregroundLayer), 4)

    # Test the addition of an overlay sprite.
    def testStoryboardAddSpriteOverlay(self):
        self.sb.addSprite("test.jpg", layer="Overlay")
        self.assertEqual(len(self.sb.overlayLayer), 1)

    # Test the addition of a background sprite.
    def testStoryboardAddAnimationBackground(self):
        self.sb.addAnimation("test.jpg", 10, 5, layer="Background")
        self.assertEqual(len(self.sb.backgroundLayer), 1)

    # Test the addition of a fail sprite.
    def testStoryboardAddAnimationFail(self):
        self.sb.addAnimation("test.jpg", 10, 5, layer="Fail")
        self.assertEqual(len(self.sb.failLayer), 1)

    # Test the addition of a pass sprite.
    def testStoryboardAddAnimationPass(self):
        self.sb.addAnimation("test.jpg", 10, 5, layer="Pass")
        self.assertEqual(len(self.sb.passLayer), 1)

    # Test the addition of a foreground sprite.
    def testStoryboardAddAnimationForeground(self):
        self.sb.addAnimation("test.jpg", 10, 5)
        self.assertEqual(len(self.sb.foregroundLayer), 4)

    # Test the addition of an overlay sprite.
    def testStoryboardAddAnimationOverlay(self):
        self.sb.addAnimation("test.jpg", 10, 5, layer="Overlay")
        self.assertEqual(len(self.sb.overlayLayer), 1)

    # Test the addition of an audio sprite.
    def testStoryboardAddAudio(self):
        self.sb.addAudio("sound.wav", 0)
        self.assertEqual(len(self.sb.soundLayer), 2)

if __name__ == "__main__":
    unittest.main()