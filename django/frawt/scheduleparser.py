import re
from api.timeslot import TimeSlot as ts
from api.dbmanager import DatabaseManager as dbm
import pymysql as mysql
import requests as req
import sys

def filterSemester(text, semesterFlag):
    pattern = re.compile("<tr.*?</tr>", re.DOTALL)
    filtered = ""
    trs = []
    reIter = re.finditer(pattern, text)
    for match in reIter:
        trs.append(match.group(0))
    i = 0
    while (i < len(trs)):
        if ("H3"+semesterFlag not in trs[i]):
            i += 1
            if (i >= len(trs)):
                continue
            while ("<tr>" not in trs[i]):
                i += 1
                if (i >= len(trs)):
                    continue
            continue
        else:
            i += 1
            while ("<tr>" not in trs[i]):
                filtered += (trs[i])
                i += 1
                if (i >= len(trs)):
                    continue
            continue
    return filtered

def parseFromText(html):
        pattern = re.compile("<td>([A-Z][A-Z])</td><td>([0-2][0-9]:[0-5][0-9])</td>"
                             "<td>([0-2][0-9]:[0-5][0-9])</td><td>([A-Z][A-Z].*?)</td>")
        schedules = []
        for match in re.finditer(pattern, html):
            room_name = match.group(4)
            timeSlot = ts(match.group(1), match.group(2), match.group(3), re.sub('\s+', ' ', room_name).strip(), True)
            schedules.append(timeSlot)
        return schedules

def getRawHtml():
    r = req.request("POST",
                    "http://www.utsc.utoronto.ca/~registrar/scheduling/timetable",
                    data="sess=year&course=DISPLAY_ALL&submit=Display+by+Discipline&course2=",
                    headers={"Referer":"http://www.utsc.utoronto.ca/~registrar/scheduling/timetable",
                             "Content-Type":"application/x-www-form-urlencoded",
                             "User-Agent":"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)"})
    return r.text

def getTimeSlots():
    html = getRawHtml()
    s = filterSemester(html, "S")
    slots = parseFromText(s)
    return slots

def add_all_ts(timeSlots):
    for slot in timeSlots:
        dbmanager.add_schedule(slot)

if __name__ == '__main__':
        try:
            dbmanager = dbm("/")
            # file = open("test.html")
            # slots = parseFromText(filterSemester(file.read(), "F"))
            slots = getTimeSlots()
            add_all_ts(slots)
            dbmanager.close()
        except mysql.Error as err:
            print(err)
