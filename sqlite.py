import sqlite3

##Connect sqlite
connection = sqlite3.connect("student.db")


## Create a cursor object to insert record, create tables

cursor = connection.cursor()

##Create the table
table_info="""
CREATE TABLE IF NOT EXISTS STUDENT(NAME VARCHAR(25), CLASS VARCHAR(25),
SECTION VARCHAR(25), MARKS INT, GRADE VARCHAR(25));
    

"""

cursor.execute(table_info)

##Insert more records

cursor.execute('''Insert into STUDENT values('Benedict', 'Data Science', 'A', 120, 'Distinction')''')
cursor.execute('''Insert into STUDENT values('Dagogo', 'Data Science', 'B', 90, 'Distinction')''')
cursor.execute('''Insert into STUDENT values('Charity', 'Data Science', 'A', 45, 'Fail')''')
cursor.execute('''Insert into STUDENT values('Erics', 'Data Science', 'A', 50, 'Credit')''')
cursor.execute('''Insert into STUDENT values('Ifeanyi', 'Data Engineer', 'A', 49, 'Fail')''')
cursor.execute('''Insert into STUDENT values('Tom', 'Data Analysis', 'A', 60, 'Good')''')
cursor.execute('''Insert into STUDENT values('Theophilus', 'Psychology', 'A', 55, 'Credit')''')
cursor.execute('''Insert into STUDENT values('Michael', 'Data Cloud', 'C', 70, 'Distinction')''')

##Display all the reports
print("The inserted records are")
data=cursor.execute('''Select * from STUDENT''')

for row in data:
    print(row)
    
    
##Commit your changes in the database
connection.commit()
connection.close()