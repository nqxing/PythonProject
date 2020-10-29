from dataReady.init import *

usernames = Rname(15000)
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
    txt = "{},{},{},{},{},{},{},{},{},{},{},{}\n".format(i+1,u,bloodtype,age,religion,nplace,schoolname,phone,occupation,major,majorintroduce,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    with open("test.txt", "a", encoding='utf-8') as f:
        f.write(txt)
    print("已写入{}条数据~".format(i+1))