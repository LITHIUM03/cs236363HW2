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
        self.assertEqual(Status.OK, Solution.addRAM(RAM(3, "DELL", 10)), "Should work")
        self.assertEqual(Status.OK, Solution.addRAM(RAM(2, "ASUS", 2)), "Should work")
        ram = Solution.getRAMByID(1)
        # ram.__str__()
        self.assertEqual(Status.OK, Solution.deleteRAM(1), "Should work")
        self.assertEqual(Status.OK, Solution.deleteRAM(3), "Should throw exception")
        self.assertEqual(Status.ALREADY_EXISTS, Solution.addRAM(RAM(2, "ASUS", 10)), "Should throw exception")
        pass

    def test_add_disk_and_file(self) -> None:
        self.assertEqual(Status.OK, Solution.addDiskAndFile(Disk(111, "DELL", 10, 10, 10), File(111, "wav", 10)),
                         "Should work")
        self.assertEqual(Status.ALREADY_EXISTS, Solution.addDiskAndFile(Disk(111, "DELL", 10, 10, 10), \
                                                                        File(112, "wav", 10)), "Should throw")
        # checking file 112 was not inserted:
        self.assertEqual(File.badFile(), Solution.getFileByID(112), "Should work")

        self.assertEqual(Status.OK, Solution.addDiskAndFile(Disk(113, "DELL", 10, 10, 10), \
                                                            File(113, "wav", 10)), "Should work")
        self.assertEqual(Status.ALREADY_EXISTS, Solution.addDiskAndFile(Disk(114, "DELL", 10, 10, 10), \
                                                                        File(113, "wav", 10)), "Should throw")
        # checking disk 114 was not inserted:
        self.assertEqual(Disk.badDisk(), Solution.getDiskByID(114), "Should work")

    def test_ram_and_disk(self) -> None:
        """def addRAMToDisk(ramID: int, diskID: int) -> Status"""

        def f1():
            """tests addRAMToDisk and removeRAMFromDisk"""
            # add ram 2 to disk 2 should work
            self.assertEqual(Status.OK, Solution.addRAM(RAM(2, "DELL", 10)), "Should work")
            self.assertEqual(Status.OK, Solution.addRAM(RAM(3, "DELL", 10)), "Should work")
            self.assertEqual(Status.OK, Solution.addDisk(Disk(2, "ASUS", 2, 5, 20)), "Should work")
            self.assertEqual(Status.OK, Solution.addRAMToDisk(2, 2), "Should work")
            # add ram 3 to disk 140 should not work NOT_EXISTS
            self.assertEqual(Status.NOT_EXISTS, Solution.addRAMToDisk(3, 140), "Should throw")
            # add ram 142 to disk 2 should not work NOT_EXISTS
            self.assertEqual(Status.NOT_EXISTS, Solution.addRAMToDisk(142, 2), "Should throw")
            # add ram 2 to disk 2 should not work ALREADY_EXISTS
            self.assertEqual(Status.ALREADY_EXISTS, Solution.addRAMToDisk(2, 2), "Should work")
            # BY ##HERE## WE HAVE (2,2) in RAM_and_Disks

            # some removals of tuples that do not exist
            self.assertEqual(Status.NOT_EXISTS, Solution.removeRAMFromDisk(156, 2), "Should work")
            self.assertEqual(Status.NOT_EXISTS, Solution.removeRAMFromDisk(2, 156), "Should work")
            self.assertEqual(Status.NOT_EXISTS, Solution.removeRAMFromDisk(3, 2), "Should work")  # not part

            self.assertEqual(Status.OK, Solution.removeRAMFromDisk(2, 2), "Should work")
            self.assertEqual(Status.NOT_EXISTS, Solution.removeRAMFromDisk(2, 2), "Should work")

        def f2():
            """tests diskTotalRAM"""
            # add ram only. check return == 0
            self.assertEqual(Status.OK, Solution.addRAM(RAM(222, "DELL", 10)), "Should work")
            self.assertEqual(0, Solution.diskTotalRAM(25), "Should work")  # 0 due disk not found

            # add Disk . check return == 0
            self.assertEqual(Status.OK, Solution.addDisk(Disk(25, "ASUS", 2, 5, 20)), "Should work")
            self.assertEqual(0, Solution.diskTotalRAM(25), "Should work")  # 0 due disk not assigned rams

            # assign ram to Disk . check return == 10
            self.assertEqual(Status.OK, Solution.addRAMToDisk(222, 25), "Should work")
            self.assertEqual(10, Solution.diskTotalRAM(25), "Should work")  # 0 due disk not
            # print(1234567890)

            # add ram 30. assign ram to Disk 25 . check return == 20
            self.assertEqual(Status.OK, Solution.addRAM(RAM(30, "DELL", 10)), "Should work")
            self.assertEqual(Status.OK, Solution.addRAMToDisk(30, 25), "Should work")
            self.assertEqual(20, Solution.diskTotalRAM(25), "Should work")  # 0 due disk not

        # f1()
        # f2()
        pass
    #
    # def is_comp_exclusive(self):
    #     self.assertEqual(Status.OK, Solution.addDisk(Disk(132, "ASUS", 2, 5, 20)), "Should work")
    #     self.assertEqual(Status.OK, Solution.addRAM(RAM(1321, "ASUS", 10)), "Should work")
    #
    #     # no rams added yet. beofen rek
    #     self.assertEqual(True, Solution.isCompanyExclusive(132), "Should work")
    #
    #     # 1 ram add. company matches.
    #     self.assertEqual(Status.OK, Solution.addRAMToDisk(1321, 132), "Should work")
    #     self.assertEqual(True, Solution.isCompanyExclusive(132), "Should work")
    #
    #     self.assertEqual(Status.OK, Solution.addRAM(RAM(1322, "rororo", 10)), "Should work")
    #     self.assertEqual(False, Solution.isCompanyExclusive(132), "Should work")

        # pass


# *** DO NOT RUN EACH TEST MANUALLY ***
if __name__ == '__main__':
    Solution.dropTables()
    unittest.main(verbosity=4, exit=False)
