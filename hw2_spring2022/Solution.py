from typing import List
import Utility.DBConnector as Connector
from Utility.Status import Status
from Utility.Exceptions import DatabaseException
from Business.File import File
from Business.RAM import RAM
from Business.Disk import Disk
from psycopg2 import sql
table_mapping={"disk":Disk,"ram":RAM,"file":File}


def delete(ID,table_type):
    conn = None
    res = Status.OK
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("DELETE FROM " + table_type + " WHERE id={0}").format(sql.Literal(ID))
        rows_effected, _ = conn.execute(query)
        if not rows_effected:
            raise DatabaseException.CHECK_VIOLATION('')
        conn.commit()
    except DatabaseException.ConnectionInvalid as e:
        res = Status.ERROR
        print(e)
    except DatabaseException.CHECK_VIOLATION as e:
        res = Status.NOT_EXISTS
        print(e)
    except Exception as e:
        res = Status.ERROR
        print(e)
    finally:
        conn.close()
        return res

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
        print(e)
    except DatabaseException.CHECK_VIOLATION as e:
        res = Status.BAD_PARAMS
        print(e)
    except DatabaseException.NOT_NULL_VIOLATION as e:
        res = Status.BAD_PARAMS
        print(e)
    except DatabaseException.UNIQUE_VIOLATION as e:
        res = Status.ALREADY_EXISTS
    except Exception as e:
        res = Status.ERROR
        print(e)
    finally:
        conn.close()
    return res


def getDiskByID(diskID: int) -> Disk:
    conn = None
    rows_effected, result = 0, Connector.ResultSet()
    try:
        conn = Connector.DBConnector()
        rows_effected, result = conn.execute(sql.SQL("SELECT * FROM Disk WHERE id={0}").format(sql.Literal(diskID)))
        if rows_effected:
            diskID, company, speed, free_space, cost=result.rows[0]
            result=Disk(diskID, company, speed, free_space, cost)
        else:
            result= Disk.badDisk()
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        conn.close()
        return result


def deleteDisk(diskID: int) -> Status:
    result=delete(diskID,table_type="disk")
    return result


def addRAM(ram: RAM) -> Status:
    conn = None
    res = Status.OK

    try:
        conn = Connector.DBConnector()
        query = sql.SQL("INSERT INTO RAM(id, company,size) VALUES({ramID}, {company}, {size})").format(ramID=sql.Literal(ram.getRamID()),
                                                                         company=sql.Literal(ram.getCompany()),
                                                                         size=sql.Literal(ram.getSize()))
        rows_effected, _ = conn.execute(query)
        conn.commit()
    except DatabaseException.ConnectionInvalid as e:
        res = Status.ERROR
        print(e)
    except DatabaseException.CHECK_VIOLATION as e:
        res = Status.BAD_PARAMS
        print(e)
    except DatabaseException.NOT_NULL_VIOLATION as e:
        res = Status.BAD_PARAMS
        print(e)
    except DatabaseException.UNIQUE_VIOLATION as e:
        res = Status.ALREADY_EXISTS
    except Exception as e:
        res = Status.ERROR
        print(e)
    finally:
        conn.close()
        return res

def getRAMByID(ramID: int) -> RAM:
    conn = None
    rows_effected, result = 0, Connector.ResultSet()
    try:
        conn = Connector.DBConnector()
        rows_effected, result = conn.execute(sql.SQL("SELECT * FROM RAM WHERE id={0}").format(sql.Literal(ramID)))
        if rows_effected:
            ramID, company, size=result.rows[0]
            result=RAM(ramID, company, size)
        else:
            result= RAM.badRAM()
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        conn.close()
        return result


def deleteRAM(ramID: int) -> Status:
    result=delete(ramID,table_type="ram")
    return result


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
