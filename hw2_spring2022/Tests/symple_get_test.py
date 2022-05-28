import unittest
import Solution
from Utility.Status import Status
from Tests.abstractTest import AbstractTest
from Business.File import File
from Business.RAM import RAM
from Business.Disk import Disk


a = Solution.get(2, 'RAM')
print(isinstance(a, RAM))

a = Solution.get(2, 'File')
print(isinstance(a, File))

a = Solution.get(2, 'Disk')
print(isinstance(a, Disk))

