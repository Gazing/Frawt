from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from .dbmanager import DatabaseManager as dbm
from .timeslot import TimeSlot as ts
from .serializers import *
import datetime
from datetime import date
import calendar

database = dbm("/")

def index(request):
    return HttpResponse("There's nothing here. Yet.")

def find_current(request):
    current = datetime.datetime.now()
    curr_hour = current.hour
    next_hour = curr_hour+1
    week_day = calendar.day_name[date.today().weekday()]
    print("Querying database for current available api")
    res = gen_ava_query(week_day, curr_hour, next_hour)
    rooms = [ts("", "", "", room[0], False) for room in res]
    serializer = RoomSerializer(rooms, many=True)
    print("Sending JSON response to "+request.META["REMOTE_ADDR"])
    return JSONResponse(serializer.data)

def get_server_time(request):
    serializer = TimeSerializer(TimeNow())
    return JSONResponse(serializer.data)

def find_available(request):
    if ("HTTP_START" not in request.META.keys() and "HTTP_END" not in request.META.keys()
        and "HTTP_DAY" not in request.META.keys()):
        return find_current(request)
    start = request.META["HTTP_START"] if (len(request.META["HTTP_START"]) > 4) else "0"+request.META["HTTP_START"]
    end = request.META["HTTP_END"] if (len(request.META["HTTP_END"]) > 4) else "0"+request.META["HTTP_END"]
    day = request.META["HTTP_DAY"] if "HTTP_DAY" in request.META.keys() else calendar.day_name[date.today().weekday()]

    if (not is_time(start) or not is_time(end) or request.method == "POST"
        or start >= end or day not in calendar.day_name):
        return JSON400Response()
    
    res = gen_ava_query(day, start.split(":")[0],
                        end.split(":")[0])
    rooms = [ts("", "", "", room[0], False) for room in res]
    serializer = RoomSerializer(rooms, many=True)
    return JSONResponse(serializer.data)

def gen_ava_query(day, start, end):
    res = database.selectOp("select * from (select distinct room_name from time_slots) as t1 natural left join"
                            " (select distinct room_name from time_slots where date = %s"
                            " and (start < %s and end > %s)) as t2 WHERE"
                            " t2.room_name is NULL;",
                            (day,
                             str(end)+":00",
                             str(start)+":00"))
    return res

def is_time(time_str):
    try:
        datetime.datetime.strptime(time_str, "%H:%M")
        return True
    except:
        return False

def get_schedule(request, room_name, day):
    actual_name = (room_name[:2]+" "+room_name[2:]).upper()
    if (day == ""):
        return HttpResponse("ALL SCHEDULES")
    if (day not in calendar.day_name):
        return JSON400Response()
    slots = query_schedule(actual_name, day)
    serializer = ScheduleSerializer(slots, many=True)
    return JSONResponse(serializer.data)

def query_all_sched(name):
    res = database.selectOp("select * from time_slots where room_name = %s", (name))
    return res

def query_schedule(name, day):
    res = database.selectOp("select start,end,date from time_slots where room_name = %s and date = %s", (name, day))
    slots = [ts(room[2], ':'.join(str(room[0]).split(':')[:2]),
                ':'.join(str(room[1]).split(':')[:2]), "", False) for room in res]
    return slots

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

class JSON400Response(JSONResponse):
    def __init__(self, msg="Invalid API arguments", **kwargs):
        serializer = MessageSerializer(ApiMessage(msg, 400))
        super(JSON400Response, self).__init__(serializer.data, status=400, **kwargs)

class TimeNow():
    def __init__(self):
        self.time = datetime.datetime.now().strftime("%H:%M")
        self.day = calendar.day_name[date.today().weekday()]