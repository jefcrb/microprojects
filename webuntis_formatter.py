#This script is extremely barebones and serves as a PoC for a future project
import requests
import json


classes = []
helper = [[], [], [], []]

print("This script requires you to have a valid authentication method to access AP's instance of Webuntis")
cookies = {"JSESSIONID": "{}".format(input("Enter a valid webuntis session id: "))}
classId = input("Enter your class id (e.g. the id of class 1ITCSC1 is 13664): ")
date = input("Enter the date of which you want to see the tables, format yyyy-mm-dd (you'll see the table for this whole week): ")

r = requests.get(f"https://arche.webuntis.com/WebUntis/api/public/timetable/weekly/data?elementType=1&elementId={classId}&date={date}&formatId=2", cookies=cookies)

data = r.json()
classesData = data["data"]["result"]["data"]["elementPeriods"][str(classId)]
elementsData = data["data"]["result"]["data"]["elements"]


for e in elementsData:

    if e["type"] == 3:
        helper[2].append({"id": e["id"], "name": e["longName"], "short": e["name"]})
    
    if e["type"] == 4:
        helper[3].append({"id": e["id"], "classroom": e["name"]})


for c in classesData:
    lessonId = ""
    classroomId = ""
    lesson = ""
    classroom = ""
    for type in c["elements"]:

        if type["type"] == 3: #type 3 contains lesson info
            lessonId = type["id"]

        if type["type"] == 4: #type 4 contains classroom info
            classroomId = type["id"]
        
        for d in helper[2]: #grab name of lesson using lessonId
            if lessonId == d["id"]:
                lesson = d["name"]

        for d in helper[3]: #grab classroom using classroomId
            if classroomId == d["id"]:
                classroom = d["classroom"]
    
    classes.append({"lesson": lesson, "type": c["lessonText"], "start": c["startTime"], "end": c["endTime"], "date": c["date"], "classroom": classroom, "lessonId": lessonId, "classroomId": classroomId})


for c in classes:
    for c2 in classes:
        if c["end"] == c2["start"] and c["lessonId"] == c2["lessonId"] and c["date"] == c2["date"] and c["type"] == c2["type"]:
            c["end"] = c2["end"]
            classes.remove(c2)


classes = sorted(classes, key = lambda i: (i["date"], i["start"]))

print(json.dumps(classes, indent=2))