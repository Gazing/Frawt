from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from .dbmanager import DatabaseManager as dbm
from .timeslot import TimeSlot as ts
from .serializers import *
import datetime
from datetime import date
import calendar

database = dbm("root", "63577477", "127.0.0.1", "roomfinder")

def index(request):
    return HttpResponse("Hello welcome to the API index. At some point I will release and document the API calls so that"
                        " you can use it too.")

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

def not_found(request):
    return HttpResponse("401: NOT FOUND")

def get_server_time(request):
    return HttpResponse(datetime.datetime.now().strftime("%H:%M"))

def find_available(request):
    if ("HTTP_START" not in request.META.keys() and "HTTP_END" not in request.META.keys()):
        return find_current(request)
    start = request.META["HTTP_START"] if (len(request.META["HTTP_START"]) > 4) else "0"+request.META["HTTP_START"]
    end = request.META["HTTP_END"] if (len(request.META["HTTP_END"]) > 4) else "0"+request.META["HTTP_END"]
    if (not is_time(start) or not is_time(end) or request.method == "POST"
        or start >= end):
        serializer = MessageSerializer(ApiMessage("Invalid API arguments", "400"))
        return JSONResponse(serializer.data, status=400)
    res = gen_ava_query(calendar.day_name[date.today().weekday()], start.split(":")[0],
                        end.split(":")[0])
    rooms = [ts("", "", "", room[0], False) for room in res]
    serializer = RoomSerializer(rooms, many=True)
    return JSONResponse(serializer.data)

def gen_ava_query(day, start, end):
    res = database.selectOp("select * from (select distinct room_name from time_slots) as t1 natural left join"
                            " (select distinct room_name from time_slots where date = %s"
                            " and start >= %s and end <= %s) as t2 WHERE t2.room_name is NULL;",
                            (day,
                             str(start)+":00",
                             str(end)+":00"))
    return res

def is_time(time_str):
    try:
        datetime.datetime.strptime(time_str, "%H:%M")
        return True
    except:
        return False

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)