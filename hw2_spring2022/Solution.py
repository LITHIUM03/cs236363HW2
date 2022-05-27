from typing import List
import Utility.DBConnector as Connector
from Utility.Status import Status
from Utility.Exceptions import DatabaseException
from Business.File import File
from Business.RAM import RAM
from Business.Disk import Disk
from psycopg2 import sql


# TODO ENFORCE id TO BE STRICTLY POSITIVE.


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
    conn = None
    try:
        conn = Connector.DBConnector()
        conn.execute('BEGIN;\
                     DELETE IF EXISTS FROM File;\
                     DELETE IF EXISTS FROM Disk;\
                     DELETE IF EXISTS FROM RAM;\
                     COMMIT;')
    except Exception as e:
        print(e)
    finally:
        conn.close()


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
    res = None
    conn = None
    try:
        conn = Connector.DBConnector()

        query = sql.SQL("INSERT INTO File(id, type, disk_size_needed) VALUES({id}, {type}, {disk_size_needed})"). \
            format(id=sql.Literal(file.getFileID()), type=sql.Literal(file.getType()), \
                   disk_size_needed=sql.Literal(file.getSize()))
        print("this is query:")
        # query = "INSERT INTO public.File(id, type, disk_size_needed) VALUES(12, 'wav', 145)"
        '''
        
         query = sql.SQL("INSERT INTO Users(id, name) VALUES({id}, {username})").format(id=sql.Literal(ID),
                                                                                       username=sql.Literal(name))
        '''
        print(query)
        rows_effected, _ = conn.execute(query)
        conn.commit()
        res = Status.OK
    except DatabaseException.ConnectionInvalid as e:
        res = Status.ERROR
        print(e)
    except DatabaseException.NOT_NULL_VIOLATION as e:
        res = Status.BAD_PARAMS
        print(e)
    except DatabaseException.CHECK_VIOLATION as e:
        res = Status.BAD_PARAMS
        print(e)
    except DatabaseException.UNIQUE_VIOLATION as e:
        res = Status.ALREADY_EXISTS
        print(e)
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        print(e)
    except Exception as e:
        print(e)
    finally:
        print("finally!")
        conn.close()
        return res


def getFileByID(fileID: int) -> File:
    rows_effected, res = 0, Connector.ResultSet()
    # ResultSet()
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("SELECT * FROM Files WHERE id={_id}").format(_id=fileID)
        rows_effected, res = conn.execute(query)
        if res.isEmpty:
            res = File.badFile()  # readability
        else:
            assert (res.size() == 1)
            res_dict = res.__getRow()
            print(type(res_dict))
    except DatabaseException.ConnectionInvalid as e:
        res = Status.ERROR
        print(e)
    except Exception as e:
        print(e)
    finally:
        conn.close()
        assert (isinstance(res, type(File())))
        return res


def deleteFile(file: File) -> Status:
    return Status.OK


def addDisk(disk: Disk) -> Status:
    conn = None
    res = Status.OK;
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("INSERT INTO Disk(id, company, speed, free_space, cost)\
         VALUES({id}, {company}, {speed}, {free_space}, {cost})").format(id=sql.Literal(disk.getDiskID()),
                                                                         company=sql.Literal(disk.getCompany()),
                                                                         speed=sql.Literal(disk.getSpeed()),
                                                                         free_space=sql.Literal(disk.getFreeSpace()),
                                                                         cost=sql.Literal(disk.getCost()))
        rows_effected, _ = conn.execute(query)
        conn.commit()
    except DatabaseException.ConnectionInvalid as e:
        res = Status.ERROR
    except DatabaseException.CHECK_VIOLATION as e:
        res = Status.BAD_PARAMS
    except DatabaseException.NOT_NULL_VIOLATION as e:
        res = Status.BAD_PARAMS
    except DatabaseException.UNIQUE_VIOLATION as e:
        res = Status.ALREADY_EXISTS
    except Exception as e:
        res = Status.ERROR
    finally:
        conn.close()
    return res


def getDiskByID(diskID: int) -> Disk:
    return Disk()


def deleteDisk(diskID: int) -> Status:
    conn = None
    rows_effected = 0
    res = Status.OK
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("DELETE FROM Disk WHERE id={0}").format(sql.Literal(diskID))
        rows_effected, _ = conn.execute(query)
        if rows_effected == 0:
            raise DatabaseException.CHECK_VIOLATION('')
        conn.commit()
    except DatabaseException.ConnectionInvalid as e:
        res = Status.ERROR
    except DatabaseException.CHECK_VIOLATION as e:
        res = Status.NOT_EXISTS
    except Exception as e:
        print(e)
    finally:
        conn.close()
    return res


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
