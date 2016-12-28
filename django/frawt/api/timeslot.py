
date_map = {"MO":"Monday", "TU":"Tuesday", "WE":"Wednesday", "TH":"Thursday", "FR":"Friday"}

class TimeSlot():
    def __init__(self, date, start, end, room, isAbb):
        self.date = date_map.get(date) if isAbb else date
        self.start = start
        self.end = end
        self.room_name = room

    def __str__(self):
        return self.room_name+" in use on: "+self.date+", from: "+self.start+" TO "+self.end

    def get_date(self):
        return self.date

    def get_room(self):
        return self.room_name

    def get_end(self):
        return self.end

    def get_start(self):
        return self.start

def test_object():
    return TimeSlot("MO", "12:00", "13:00", "SW 128", True)