import unittest
import Solution


class AbstractTest(unittest.TestCase):
    # before each test, setUp is executed
    def setUp(self) -> None:
        # print("~~~~~~~~~~~~~~AbstractTest setUp~~~~~~~~~~~~~~")
        Solution.createTables()

    # after each test, tearDown is executed
    def tearDown(self) -> None:
        # print("~~~~~~~~~~~~~~AbstractTest tearDown~~~~~~~~~~~~~~")
        Solution.dropTables()
        pass
