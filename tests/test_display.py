import unittest


class DisplayTest(unittest.TestCase):
    
    def setUp(self):
        """Set up the tests"""
        print("DisplayTest:setUp_:begin")
        # do stuff
        # let's instance some ShipGrids and
        # pre-populate them
        print("DisplayTest:setUp_:end")

    def tearDown(self):
        """Clean up after the test"""
        print("DisplayTest:tearDown_:begin")
        # do stuff
        print("DisplayTest:tearDown_:end")