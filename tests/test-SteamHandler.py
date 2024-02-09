import unittest
import sys
sys.path.append('../Gamekit')
import GameKit.SteamHandler
 
# importing
from parentdirectory.geeks import geek_method

class test_requests(unittest.TestCase):

    def should_fail(self):
        self.assertEqual(1,2)



if __name__ == '__main__':
    unittest.main()
