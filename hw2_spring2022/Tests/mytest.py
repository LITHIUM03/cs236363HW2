import unittest
import Solution
from Utility.Status import Status
from Tests.abstractTest import AbstractTest
from Business.File import File
from Business.RAM import RAM
from Business.Disk import Disk


class Test(AbstractTest):
    """DO NOT add irrelevant tests to already existing test_functions. This messes up the git"""

    def test_Create(self) -> None:
        pass

    def test_Disk(self) -> None:
        self.assertEqual(Status.OK, Solution.addDisk(Disk(1, "DELL", 10, 10, 10)), "Should work")
        self.assertEqual(Status.OK, Solution.addDisk(Disk(2, "ASUS", 2, 5, 20)), "Should work")
        disk = Solution.getDiskByID(1)
        # disk.__str__()
        self.assertEqual(Status.OK, Solution.deleteDisk(1), "Should work")
        self.assertEqual(Status.NOT_EXISTS, Solution.deleteDisk(3), "Should throw exception")
        self.assertEqual(Status.ALREADY_EXISTS, Solution.addDisk(Disk(2, "ASUS", 10, 10, 10)), "Should throw exception")
        pass

    def test_file(self) -> None:
        def test_add() -> None:
            self.assertEqual(Status.BAD_PARAMS, Solution.addFile(File(0, "wav", 10)),
                             "Should throw exception")  # zero id
            self.assertEqual(Status.OK, Solution.addFile(File(1, "wav", 10)), "Should work")
            self.assertEqual(Status.ALREADY_EXISTS, Solution.addFile(File(1, "wav", 22)),
                             "Should throw exception")  # ALREADY_EXISTS
            self.assertEqual(Status.OK, Solution.addFile(File(2, "kax", 10)), "Should work")

        def test_delete() -> None:
            self.assertEqual(Status.OK, Solution.deleteFile(File(12, "wav", 10)),
                             "Should work")  # does not exist, yet should work
            self.assertEqual(Status.OK, Solution.deleteFile(File(0, "wav", 10)),
                             "Should work")  # does not exist, yet should work
            self.assertEqual(Status.OK, Solution.deleteFile(File(1, "wav", 10)),
                             "Should work")
            self.assertEqual(Status.OK, Solution.addFile(File(1, "wav", 10)), "Should work")
            self.assertEqual(Status.OK, Solution.deleteFile(File(1, "wav", 10)),
                             "Should work")

        def test_get() -> None:
            self.assertEqual(File.badFile(), Solution.getFileByID(123), "Should work")
            self.assertEqual(File(2, "kax", 10), Solution.getFileByID(2), "Should work")
            pass

        test_add()
        test_delete()
        test_get()
        pass

    def test_ram(self) -> None:
        self.assertEqual(Status.OK, Solution.addRAM(RAM(1, "DELL", 10)), "Should work")
        self.assertEqual(Status.OK, Solution.addRAM(RAM(2, "ASUS", 2)), "Should work")
        ram = Solution.getRAMByID(1)
        # ram.__str__()
        self.assertEqual(Status.OK, Solution.deleteRAM(1), "Should work")
        self.assertEqual(Status.NOT_EXISTS, Solution.deleteRAM(3), "Should throw exception")
        self.assertEqual(Status.ALREADY_EXISTS, Solution.addRAM(RAM(2, "ASUS", 10)), "Should throw exception")
        pass

    def test_add_file_to_disk(self) -> None:
        self.assertEqual(Status.OK, Solution.addFile(File(1, "DELL", 11)),
                         "Should work")
        self.assertEqual(Status.OK, Solution.addDisk(Disk(1, "DELL", 2, 50, 20)),
                         "Should work")
        self.assertEqual(Status.OK, Solution.addFileToDisk(File(1, "DELL", 11), 1),
                         "Should work")
        self.assertEqual(Status.NOT_EXISTS, Solution.addFileToDisk(File(2, "DELL", 9), 1),
                         "Should work")
        self.assertEqual(Status.NOT_EXISTS, Solution.addFileToDisk(File(1, "DELL", 9), 2),
                         "Should work")
        self.assertEqual(Status.ALREADY_EXISTS, Solution.addFileToDisk(File(1, "DELL", 9), 1),
                         "Should work")
        self.assertEqual(Status.OK, Solution.addFile(File(2, "DELL", 11)),
                         "Should work")
        self.assertEqual(Status.BAD_PARAMS, Solution.addFileToDisk(File(2, "DELL", 50), 1),
                         "Should work")
    pass

    def test_remove_file_from_disk(self) -> None:
        self.assertEqual(Status.OK, Solution.addFile(File(1, "DELL", 11)),
                         "Should work")
        self.assertEqual(Status.OK, Solution.addDisk(Disk(1, "DELL", 2, 50, 20)),
                     "Should work")
        self.assertEqual(Status.OK, Solution.addDisk(Disk(2, "DELL", 2, 50, 20)),
                         "Should work")
        self.assertEqual(Status.OK, Solution.addFileToDisk(File(1, "DELL", 11), 1),
                     "Should work")
        self.assertEqual(Status.OK, Solution.removeFileFromDisk(File(1, "DELL", 11), 1),
                         "Should work")
        self.assertEqual(Status.OK, Solution.removeFileFromDisk(File(2, "DELL", 11), 1),
                         "Should work")
        self.assertEqual(Status.OK, Solution.removeFileFromDisk(File(1, "DELL", 11), 2),
                         "Should work")
        self.assertEqual(Status.OK, Solution.addFileToDisk(File(1, "DELL", 11), 2),
                         "Should work")
        self.assertEqual(Status.OK, Solution.removeFileFromDisk(File(1, "DELL", 11), 1),
                         "Should work")
    pass

    def test_avg_file_size_on_disk(self) -> None:
        self.assertEqual(Status.OK, Solution.addFile(File(1, "DELL", 11)),
                         "Should work")
        self.assertEqual(Status.OK, Solution.addFile(File(2, "ASUS", 5)),
                         "Should work")
        self.assertEqual(Status.OK, Solution.addFile(File(3, "WD", 8)),
                         "Should work")
        self.assertEqual(Status.OK, Solution.addDisk(Disk(1, "DELL", 2, 50, 20)),
                         "Should work")
        self.assertEqual(Status.OK, Solution.addFileToDisk(File(1, "DELL", 11), 1),
                         "Should work")
        self.assertEqual(Status.OK, Solution.addFileToDisk(File(2, "ASUS", 5), 1),
                         "Should work")
        self.assertEqual(Status.OK, Solution.addFileToDisk(File(3, "WD", 8), 1),
                         "Should work")
        self.assertEqual(8, Solution.averageFileSizeOnDisk(1),
                         "Should work")
        self.assertEqual(0, Solution.averageFileSizeOnDisk(2),
                         "ID does not exists")
        self.assertEqual(Status.OK, Solution.addDisk(Disk(2, "DELL", 5, 50, 20)),
                         "Should work")
        self.assertEqual(0, Solution.averageFileSizeOnDisk(2),
                         "Division by zero")
    pass

# *** DO NOT RUN EACH TEST MANUALLY ***
if __name__ == '__main__':
    Solution.dropTables()
    unittest.main(verbosity=2, exit=False)
