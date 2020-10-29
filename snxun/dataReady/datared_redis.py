import redis
from dataReady.init import *

conn = redis.Redis(host="116.62.126.139", port=6379, password="nieaaa")

usernames = Rname(15000)
mylist = []
for i,u in enumerate(usernames):
    bloodtype = Bloodtype[random.randint(0, len(Bloodtype) - 1)]
    age = random.randint(20, 50)
    religion = Religion[random.randint(0, len(Religion) - 1)]
    nplace = Nplace[random.randint(0, len(Nplace) - 1)]
    schoolname = Schoolname[random.randint(0, len(Schoolname) - 1)]
    phone = '{}{}'.format(phoneNum[random.randint(0, len(phoneNum) - 1)], random.randint(100000000, 999999999))
    occupation = Occupation[random.randint(0, len(Occupation) - 1)]
    major = Major[random.randint(0, len(Major) - 1)]
    majorintroduce = Majorintroduce[random.randint(0, len(Majorintroduce) - 1)]
    dict = {
            "username": u,
            "bloodtype": bloodtype,
            "age": age,
            "religion": religion,
            "nplace": nplace,
            "schoolname": schoolname,
            "phone": phone,
            "occupation": occupation,
            "major": major,
            "majorintroduce": majorintroduce,
            "time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
    mylist.append(dict)
# conn.set("x1","hello",ex=5) # ex代表seconds，px代表ms
conn.set('test', '{}'.format(mylist))
# val = conn.get("x1")
# print(val)