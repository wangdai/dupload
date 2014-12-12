import unittest
import random
import sys

from dupload.utils import splitext, judgecat, obfuscate, clarify

class UtilityTestCase(unittest.TestCase):

    def test_splitext(self):
        self.assertEqual(('dupload', '.tar.gz'), splitext('dupload.tar.gz'))
        self.assertEqual(('lCupboard', '.png'), splitext('lCupboard.png'))
    
    def test_judgecat(self):
        self.assertEqual('other', judgecat(''))
        self.assertEqual('other', judgecat('.deb'))
        self.assertEqual('pack', judgecat('.tar.gz'))
        self.assertEqual('music', judgecat('.mp3'))
        self.assertEqual('doc', judgecat('.txt'))
    
    def test_obfuscat_clarify(self):
        self.assertEqual(0, clarify(obfuscate(0)))
        self.assertEqual(1, clarify(obfuscate(1)))
        for i in range(200):
            ri = random.randrange(2, 1000000)
            self.assertEqual(ri, clarify(obfuscate(ri)))

