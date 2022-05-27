from typing import List
import Utility.DBConnector as Connector
from Utility.Status import Status
from Utility.Exceptions import DatabaseException
from Business.File import File
from Business.RAM import RAM
from Business.Disk import Disk
from psycopg2 import sql


def createTables():
    conn = None
    try:
        conn = Connector.DBConnector()
        conn.execute(" BEGIN;\
                     CREATE TABLE IF NOT EXISTS File(id INTEGER PRIMARY KEY NOT NULL, \
                     type TEXT NOT NULL, disk_size_needed INTEGER NOT NULL);\
                     CREATE TABLE IF NOT EXISTS Disk(id INTEGER PRIMARY KEY NOT NULL,\
                     company TEXT NOT NULL,speed INTEGER NOT NULL, free_space INTEGER NOT NULL, cost INTEGER NOT NULL);\
                     CREATE TABLE IF NOT EXISTS  RAM(id INTEGER PRIMARY KEY NOT NULL,size INTEGER NOT NULL, \
                     company TEXT NOT NULL);\
                     COMMIT;")
        conn.commit()
    except DatabaseException.ConnectionInvalid as e:
        print(e)
    except DatabaseException.NOT_NULL_VIOLATION as e:
        print(e)
    except DatabaseException.CHECK_VIOLATION as e:
        print(e)
    except DatabaseException.UNIQUE_VIOLATION as e:
        print(e)
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        print(e)
    except Exception as e:
        print(e)
    finally:
        # will happen any way after try termination or exception handling
        conn.close()


def clearTables():
    pass


def dropTables():
    conn = None
    try:
        conn = Connector.DBConnector()
        conn.execute('BEGIN;\
                     DROP TABLE IF EXISTS File;\
                     DROP TABLE IF EXISTS Disk;\
                     DROP TABLE IF EXISTS RAM;\
                     COMMIT;')
    except Exception as e:
        print(e)
    finally:
        conn.close()


def addFile(file: File) -> Status:
    return Status.OK


def getFileByID(fileID: int) -> File:
    return File()


def deleteFile(file: File) -> Status:
    return Status.OK


def addDisk(disk: Disk) -> Status:
    return Status.OK


def getDiskByID(diskID: int) -> Disk:
    return Disk()


def deleteDisk(diskID: int) -> Status:
    return Status.OK


def addRAM(ram: RAM) -> Status:
    return Status.OK


def getRAMByID(ramID: int) -> RAM:
    return RAM()


def deleteRAM(ramID: int) -> Status:
    return Status.OK


def addDiskAndFile(disk: Disk, file: File) -> Status:
    return Status.OK


def addFileToDisk(file: File, diskID: int) -> Status:
    return Status.OK


def removeFileFromDisk(file: File, diskID: int) -> Status:
    return Status.OK


def addRAMToDisk(ramID: int, diskID: int) -> Status:
    return Status.OK


def removeRAMFromDisk(ramID: int, diskID: int) -> Status:
    return Status.OK


def averageFileSizeOnDisk(diskID: int) -> float:
    return 0


def diskTotalRAM(diskID: int) -> int:
    return 0


def getCostForType(type: str) -> int:
    return 0


def getFilesCanBeAddedToDisk(diskID: int) -> List[int]:
    return []


def getFilesCanBeAddedToDiskAndRAM(diskID: int) -> List[int]:
    return []


def isCompanyExclusive(diskID: int) -> bool:
    return True


def getConflictingDisks() -> List[int]:
    return []


def mostAvailableDisks() -> List[int]:
    return []


def getCloseFiles(fileID: int) -> List[int]:
    return []
