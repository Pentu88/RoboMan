import unittest
from src.roboman import RoboMan

class TestRoboMan(unittest.TestCase):
    def setUp(self):
        print("Set up goes here")

    def test_liiku_palauttaa_suraavan_ruudun(self):
        game = RoboMan()

        # Alustetaan hirviö
        olio = {}
        olio['id'] = 5
        # olio['kuva'] = kuva
        olio['koordit'] = (1, 1) # (1, 7)
        olio['korjaus'] = (0, 0)
        olio['liike'] = (1, 0)
        # kuva ('hirvio', 0)
        # 'nimi' = 'hirvio'
        # 'koodi' = 1
        # 'e' = none
        
        self.assertEqual(game.liiku(olio), (2, 1))