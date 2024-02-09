import unittest
import sys
import os
# While I am ware that there is a better way of doing this, i simply dont care enough to do it as it would require reformating the entire application.
sys.path.append(str(os.getcwd()).replace("/tests", ""))
import SteamHandler

class test_requests(unittest.TestCase):

    def test_should_success(self):
        self.assertEqual(1, 1)

    def test_should_fail(self):
        self.assertEqual(1,2)




if __name__ == '__main__':
    unittest.main()
