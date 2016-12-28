import pymysql as mysql
from sqlalchemy import create_engine, exc
from .timeslot import TimeSlot as ts

CONNECTION = "mysql://{}:{}@{}/{}"

class DatabaseManager():
    def __init__(self, uname, password, host, dbname):
        self.engine = create_engine(str.format(CONNECTION, uname, password, host, dbname), echo=True)

    def add_schedule(self, schedule):
        query = "insert into time_slots (room_name, date, start, end) values (%s, %s, %s, %s)"
        data = (schedule.get_room(), schedule.get_date(), schedule.get_start(), schedule.get_end())
        try:
            with self.engine.connect() as conn:
                conn.execute(query, data)
        except exc.DBAPIError as err:
            print("ERROR: "+err.__str__())

    def selectOp(self, query, data):
        with self.engine.connect() as conn:
                response = conn.execute(query, data)
                result = response.fetchall()
        return result

    def close(self):
        return
