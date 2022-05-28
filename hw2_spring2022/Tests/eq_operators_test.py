import unittest
import Solution
from Utility.Status import Status
from Tests.abstractTest import AbstractTest
from Business.File import File
from Business.RAM import RAM
from Business.Disk import Disk

print(File(1, "jpeg", 12) == File(1, "jpeg", 12))
print(Disk(1, 'comp', 2, 3, 4) == Disk(1, 'comp', 2, 3, 4))
print(RAM(1, 'comp', 2) == RAM(1, 'comp', 2))

