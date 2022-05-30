from typing import List, Union
import Utility.DBConnector as Connector
from Utility.Status import Status
from Utility.Exceptions import DatabaseException
from Business.File import File
from Business.RAM import RAM
from Business.Disk import Disk
from psycopg2 import sql


def DeletediskORram(ID, table_name):
    """this function is good only for deleting ram or disk, since for those deleting an id that does not exist is
    illegal,and should throw. for file-shouldn't throw!"""
    conn = None
    res = Status.OK
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("DELETE FROM " + table_name + " WHERE id={0}").format(sql.Literal(ID))
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


def get(ID, table_name):
    """this function is good for all three tables."""
    #        query = sql.SQL("SELECT * FROM Files WHERE id={_id}").format(_id=fileID)

    conn = None
    res = Status.OK
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("SELECT * FROM " + table_name + " WHERE id={0}").format(sql.Literal(ID))
        rows_effected, result = conn.execute(query)
        if table_name == "Disk":
            if rows_effected:
                assert (rows_effected == 1)
                diskID, company, speed, free_space, cost = result.rows[0]
                result = Disk(diskID, company, speed, free_space, cost)
            else:
                result = Disk.badDisk()
        elif table_name == "File":
            if rows_effected:
                assert (rows_effected == 1)
                fileID, filetype, disk_size_needed = result.rows[0]
                result = File(fileID, filetype, disk_size_needed)
            else:
                result = File.badFile()
        elif table_name == "RAM":
            if rows_effected:
                assert (rows_effected == 1)
                ramID, size, company = result.rows[0]
                result = RAM(ramID, size, company)

            else:
                result = RAM.badRAM()
        else:
            assert ()
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        conn.close()
        return result


def createTables():
    conn = None
    try:
        conn = Connector.DBConnector()
        conn.execute(" BEGIN;\
                     CREATE TABLE IF NOT EXISTS File(id INTEGER PRIMARY KEY NOT NULL, \
                        type TEXT NOT NULL, disk_size_needed INTEGER NOT NULL,CHECK (id>=1));\
                     CREATE TABLE IF NOT EXISTS Disk(id INTEGER PRIMARY KEY NOT NULL, company TEXT NOT NULL,\
                        speed INTEGER NOT NULL, free_space INTEGER NOT NULL, cost INTEGER NOT NULL,CHECK (id>=1));\
                     CREATE TABLE IF NOT EXISTS RAM(id INTEGER PRIMARY KEY NOT NULL,size INTEGER NOT NULL, \
                        company TEXT NOT NULL,CHECK (id>=1));\
                     CREATE TABLE IF NOT EXISTS FileToDisk(did INTEGER NOT NULL,\
                        fid INTEGER NOT NULL, delta INTEGER NOT NULL,\
                        CHECK (delta>=0),\
                        FOREIGN KEY (did) REFERENCES Disk(id) ON DELETE CASCADE,\
                        FOREIGN KEY (fid) REFERENCES File(id) ON DELETE CASCADE, PRIMARY KEY (did, fid));\
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
                     DELETE IF EXISTS FROM FileToDisk;\
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
                     DROP TABLE IF EXISTS FileToDisk;\
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
        conn.close()
        return res


def getFileByID(fileID: int) -> File:
    result = get(fileID, "File")
    return result


def deleteFile(file: File) -> Status:
    conn = None
    res = Status.OK
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("DELETE FROM File" + " WHERE id={0}").format(sql.Literal(file.getFileID()))
        rows_effected, _ = conn.execute(query)
        conn.commit()
    except DatabaseException.ConnectionInvalid as e:
        res = Status.ERROR
        print(e)
    except Exception as e:
        res = Status.ERROR
        print(e)
    finally:
        conn.close()
        return res


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
    result = get(diskID, "Disk")
    return result


def deleteDisk(diskID: int) -> Status:
    result = DeletediskORram(diskID, table_name="disk")
    return result


def addRAM(ram: RAM) -> Status:
    conn = None
    res = Status.OK

    try:
        conn = Connector.DBConnector()
        query = sql.SQL("INSERT INTO RAM(id, company,size) VALUES({ramID}, {company}, {size})").format(
            ramID=sql.Literal(ram.getRamID()),
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
    result = get(ramID, "RAM")
    return result


def deleteRAM(ramID: int) -> Status:
    result = DeletediskORram(ramID, table_name="ram")
    return result


def addDiskAndFile(disk: Disk, file: File) -> Status:
    return Status.OK


def addFileToDisk(file: File, diskID: int) -> Status:
    conn = None
    res = Status.OK
    """insert into filetodisk(file,disk) \
    (select file.id , disk.id, disk.free_space - file.size as delta from file , disk where delta >= 0 and disk.id = diskID and file.id={fid}) 
    """
    """
    
    """
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("BEGIN; \
                                UPDATE Disk SET free_space = free_space - {fsize} WHERE id={did}; \
                                INSERT INTO FileToDisk(did, fid, delta) \
                                VALUES ({did}, {fid}, (SELECT free_space FROM Disk WHERE id={did}));\
                        END;").format(did=sql.Literal(diskID), fid=sql.Literal(file.getFileID()), fsize=sql.Literal(file.getSize()))
        rows_effected, result = conn.execute(query)
        conn.commit()
    except DatabaseException.UNIQUE_VIOLATION as e:
        res = Status.ALREADY_EXISTS
        conn.rollback()
        print(e)
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        res = Status.NOT_EXISTS
        conn.rollback()
        print(e)
    except DatabaseException.NOT_NULL_VIOLATION as e:
        res = Status.NOT_EXISTS
        conn.rollback()
        print(e)
    except DatabaseException.CHECK_VIOLATION as e:
        res = Status.BAD_PARAMS
        conn.rollback()
        print(e)
    except Exception as e:
        res = Status.ERROR
        conn.rollback()
        print(e)
    finally:
        conn.close()
        return res


def removeFileFromDisk(file: File, diskID: int) -> Status:
    conn = None
    res = Status.OK
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("BEGIN; \
                        UPDATE Disk SET free_space = free_space + {fsize} WHERE id={did}\
                        AND (SELECT COUNT(*) FROM FileToDisk WHERE did={did} AND fid={fid})>=1;\
                        DELETE FROM FileToDisk WHERE did={did} AND fid={fid};\
                        END;").format(did=sql.Literal(diskID), fid=sql.Literal(file.getFileID()), fsize=sql.Literal(file.getSize()))
        rows_effected, _ = conn.execute(query)
        conn.commit()
    except Exception as e:
        res = Status.ERROR
        conn.rollback()
        print(e)
    finally:
        conn.close()
        return res


def addRAMToDisk(ramID: int, diskID: int) -> Status:
    return Status.OK


def removeRAMFromDisk(ramID: int, diskID: int) -> Status:
    return Status.OK


def averageFileSizeOnDisk(diskID: int) -> float:
    conn = None
    res = 0.0
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("Select CAST(sum(file.disk_size_needed) as float)/CAST(count(file.id) as float) as avg_size from Disk\
                         inner join filetodisk as ftd on disk.id=ftd.did\
                         inner join file on ftd.fid=file.id\
                         WHERE {did} IN (Select did from Disk) and disk.id={did}\
                         group by disk.id").format(did=sql.Literal(diskID))
        rows_effected, result = conn.execute(query)
        if rows_effected:
            res = result.rows[0][0]
        conn.commit()
    except Exception as e:
        res = -1.0
        print(e)
    finally:
        conn.close()
        return res


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
