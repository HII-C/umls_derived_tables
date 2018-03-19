import pymysql

connection = pymysql.connect(user='hiic', passwd='greenes2018',host='db01.healthcreek.org', port=3306, database='mysql')   
print("success")
cursor = connection.cursor()
query = ("SELECT * FROM derived.isa_helper")
cursor.execute(query)
result = cursor.fetchone()
print(result)

