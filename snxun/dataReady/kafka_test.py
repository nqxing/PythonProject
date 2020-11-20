import datetime
import json
import time
from kafka import KafkaProducer
from dataReady.init import *

# producer=KafkaProducer(bootstrap_servers='116.62.126.139:9092')
#
# usernames = Rname(1)
# mylist = []
# for i,u in enumerate(usernames):
#     bloodtype = Bloodtype[random.randint(0, len(Bloodtype) - 1)]
#     age = random.randint(20, 50)
#     religion = Religion[random.randint(0, len(Religion) - 1)]
#     nplace = Nplace[random.randint(0, len(Nplace) - 1)]
#     schoolname = Schoolname[random.randint(0, len(Schoolname) - 1)]
#     phone = '{}{}'.format(phoneNum[random.randint(0, len(phoneNum) - 1)], random.randint(100000000, 999999999))
#     occupation = Occupation[random.randint(0, len(Occupation) - 1)]
#     major = Major[random.randint(0, len(Major) - 1)]
#     majorintroduce = Majorintroduce[random.randint(0, len(Majorintroduce) - 1)]
#     dict = {
#             "username": u,
#             "bloodtype": bloodtype,
#             "age": age,
#             "religion": religion,
#             "nplace": nplace,
#             "schoolname": schoolname,
#             "phone": phone,
#             "occupation": occupation,
#             "major": major,
#             "majorintroduce": majorintroduce,
#             "time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#             }
#     mylist.append(dict)
#
#
# for m in mylist:
#     future = producer.send('kafka_test', json.dumps(m).encode(), partition=0)
#     record_metadata = future.get(timeout=10)
#     print(record_metadata, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
#     # time.sleep(3)


from kafka import KafkaConsumer

consumer = KafkaConsumer('kafka_test', bootstrap_servers=['116.62.126.139:9092'], auto_offset_reset='earliest')

for i,message in enumerate(consumer):
    print(message)
    print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                         message.offset, message.key,
                                         message.value))
    print('-----------------{}---------------------'.format(i))