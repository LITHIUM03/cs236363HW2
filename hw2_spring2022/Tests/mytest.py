import unittest
import Solution
from Utility.Status import Status
from Tests.abstractTest import AbstractTest
from Business.File import File
from Business.RAM import RAM
from Business.Disk import Disk


class Test(AbstractTest):
    """DO NOT add irrelevant tests to already existing functions. This messes up the git"""

    def test_Create(self) -> None:
        pass

    def test_Disk(self) -> None:
        self.assertEqual(Status.OK, Solution.addDisk(Disk(1, "DELL", 10, 10, 10)), "Should work")
        self.assertEqual(Status.OK, Solution.addDisk(Disk(2, "ASUS", 2, 5, 20)), "Should work")
        disk = Solution.getDiskByID(1)
        disk.__str__()
        self.assertEqual(Status.OK, Solution.deleteDisk(1), "Should work")
        self.assertEqual(Status.NOT_EXISTS, Solution.deleteDisk(3), "Should throw exception")
        self.assertEqual(Status.ALREADY_EXISTS, Solution.addDisk(Disk(2, "ASUS", 10, 10, 10)), "Should throw exception")
        pass

    def test_addfile(self) -> None:
        self.assertEqual(Status.OK, Solution.addFile(File(1, "wav", 10)), "Should work")
        pass

    def test_ram(self) -> None:
        self.assertEqual(Status.OK, Solution.addRAM(RAM(1, "DELL", 10)), "Should work")
        self.assertEqual(Status.OK, Solution.addRAM(RAM(2, "ASUS", 2)), "Should work")
        ram = Solution.getRAMByID(1)
        ram.__str__()
        self.assertEqual(Status.OK, Solution.deleteRAM(1), "Should work")
        self.assertEqual(Status.NOT_EXISTS, Solution.deleteRAM(3), "Should throw exception")
        self.assertEqual(Status.ALREADY_EXISTS, Solution.addRAM(RAM(2, "ASUS", 10)), "Should throw exception")
        pass


# *** DO NOT RUN EACH TEST MANUALLY ***
if __name__ == '__main__':
    Solution.dropTables()
    unittest.main(verbosity=2, exit=False)
