import pymongo
client = pymongo.MongoClient(host='localhost',port=27017)
db = client.test
collection = db.students
student = {
    'id':'20170101',
    'name':'Jordan',
    'age':20,
    'gender':'male',
    'abc':'45555'
}
student1 = {
    'id':'356568',
    'name':'Jordanss',
    'age':20,
    'gender':'malesss',
    'abc':'45555',
    'sss':'中文试试'
}
result = collection.insert([student,student1])
print(result)