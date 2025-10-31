import sqlite3

connection = sqlite3.connect('records.db')

##Inventory file
file1 = open('inventory.csv', 'r')
data = file1.readlines()
for line in data:
    line = line.split(',')
    connection.execute('INSERT INTO Inventory Values(?,?,?,?,?,?)', (line[0], line[1], line[2], line[3], line[4], line[5]))

connection.commit()

file1.close()

##Members file
file2 = open('member.csv', 'r')
data = file2.readlines()
for line in data:
    line = line.split(',')
    connection.execute('INSERT INTO Member Values(?,?,?,?)', (line[0], line[1], line[2],0))

connection.commit()
connection.close()
file2.close()
