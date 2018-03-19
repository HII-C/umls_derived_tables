# umls_derived_tables
A series of derived tables from UMLS to aid in NLP/ML development. Written in MySQL.

To connect to database, there are two steps of authentication:
1. Connect to the server that holds the database
2. Connect to the database (with pymysql) that is password protected

Steps (w/.pem private key):
1. ssh -l student -i ~/.ssh/hii-c-student.pem general.healthcreek.org
2. cd joseph_briones
3. python3 test.py

This will test a connection to the mysql database. Within the test.py, the username + password for the database is specified.

If not working:
1. Make sure mysql is running on the server
2. Make sure you are using python3 and not python
3. Check documentaiton for specifics on pymysql


Wentao Zhou
Joseph Briones

