from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from .dbmanager import DatabaseManager as dbm
from .timeslot import TimeSlot as ts
from .serializers import RoomSerializer
import datetime
from datetime import date
import calendar

database = dbm("???", "???", "???", "???")

def index(request):
    return HttpResponse("Hello welcome to the API index. At some point I will release and document the API calls so that"
                        " you can use it too.")

def find_current(request):
    current = datetime.datetime.now()
    curr_hour = current.hour
    next_hour = curr_hour+1
    week_day = calendar.day_name[date.today().weekday()]
    print("Querying database for current available api")
    res = database.selectOp("select * from (select distinct room_name from time_slots) as t1 natural left join"
                            " (select distinct room_name from time_slots where date = %s"
                            " and start = %s and end = %s) as t2 WHERE t2.room_name is NULL;",
                            (week_day,
                             str(curr_hour)+":00",
                             str(next_hour)+":00"))
    rooms = [ts("", "", "", room[0], False) for room in res]
    serializer = RoomSerializer(rooms, many=True)
    print("Sending JSON response to "+request.META["REMOTE_ADDR"])
    return JSONResponse(serializer.data)

def not_found(request):
    return HttpResponse("401: NOT FOUND")

def get_server_time(request):
    return HttpResponse(datetime.datetime.now().strftime("%H:%M"))

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)
