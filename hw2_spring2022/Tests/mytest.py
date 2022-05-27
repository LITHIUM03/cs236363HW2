import unittest
import Solution
from Utility.Status import Status
from Tests.abstractTest import AbstractTest
from Business.File import File
from Business.RAM import RAM
from Business.Disk import Disk

'''
    Simple test, create one of your own
    make sure the tests' names start with test_
'''


class Test(AbstractTest):
    def test_Create(self) -> None:
        self.assertEqual(Status.OK, Solution.addDisk(Disk(1, "DELL", 10, 10, 10)), "Should work")


# *** DO NOT RUN EACH TEST MANUALLY ***
if __name__ == '__main__':
    unittest.main(verbosity=2, exit=False)
