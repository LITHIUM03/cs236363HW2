from typing import List, Union
import Utility.DBConnector as Connector
from Utility.Status import Status
from Utility.Exceptions import DatabaseException
from Business.File import File
from Business.RAM import RAM
from Business.Disk import Disk
from psycopg2 import sql

conn = None
res = Status.OK
try:
    conn = Connector.DBConnector()
    query = sql.SQL(" BEGIN;\
    INSERT INTO Disk(id, company, speed, free_space, cost) VALUES(62, 'dog', 43, 1000, 1000); \
    INSERT INTO Disk(id, company, speed, free_space, cost) VALUES(662, 'dog', 43, 1000, 1000); ")
    rows_effected, res = conn.execute(query)
    conn.commit()
except DatabaseException.ConnectionInvalid as e:
    res = Status.ERROR
    # print(e)
except DatabaseException.UNIQUE_VIOLATION as e:
    res = Status.ALREADY_EXISTS
    conn.rollback()
    # print(e)
except Exception as e:
    res = Status.ERROR
    # print(e)
finally:
    conn.close()
    print(rows_effected, res)
