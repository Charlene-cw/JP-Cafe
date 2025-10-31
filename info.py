import flask
from flask import render_template,request
import sqlite3

##Web app 
app = flask.Flask(__name__)

#read file function
def read_data():
    connection = sqlite3.connect('records.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Inventory")
    rows = cursor.fetchall()
    ItemID = []
    Name = [] 
    Desc = []
    Price = []
    Qty = []
    Pic = [] 
    for row in rows:
        ItemID += [row[0]]
        Name += [row[1]]
        Desc += [row[2]]
        Price += [row[3]]
        Qty += [row[4]]
        Pic += [row[5]]
            
    return ItemID, Name, Desc, Price, Qty, Pic
    
#Home function
@app.route('/', methods = ['GET', 'POST'])
def home():
    ItemID, Name, Desc, Price, Qty, Pic = read_data()
    return render_template('home.html', Name=Name, Desc=Desc, Price=Price, Qty=Qty, Pic=Pic)

#sign up
@app.route('/register', methods = ['GET','POST'])
def signup():
    return render_template('signup.html')

#sign up successful
@app.route('/register-successful', methods=['POST'])
def register():
    connection = sqlite3.connect('records.db')
    data = request.form
    if 'newmemName' and 'newmemEmail' and 'newmemPassword' in data:
        connection.execute('INSERT INTO Member VALUES(?,?,?,?)', (data['newmemName'], data['newmemEmail'], data['newmemPassword'], 0))
        connection.commit()
        
    return render_template('successful.html')

#Order Confirmation
@app.route('/calculate', methods=['POST'])
def calculate():
    total = 0
    data = request.form
    ItemID, Name, Desc, Price, Qty, Pic = read_data()
    cusname = data['cusname']
    qtyordered = []
    finalqty = []
    pp = []
    iordered = []
    itemID = []
    
    for item in data:
        if data[item].isdigit():
            qtyordered.append(int(data[item]))
    for i in range(10):
        if qtyordered[i] != 0:
            itemID.append(ItemID[i])
            iordered.append(Name[i])
            finalqty.append(qtyordered[i])
            pp.append(Price[i])
            total += qtyordered[i] * float(Price[i])

    #length of order
    length = len(iordered)
            
    #Check whcih button pressed
    discount = False
    is_mem = 0
    if 'mem' in data and data['mem'] == 'Member login and Order':
        discount = True
        is_mem = 1
        totalp = total * 0.9
    elif 'action' in data and data['action'] == 'Order as guest':
        totalp = total

    ##update quantity
    connection = sqlite3.connect('records.db')
    
    for i in range(10):
        new = int(Qty[i]) - qtyordered[i]
        connection.execute("UPDATE Inventory SET Quantity = ? WHERE ItemID = ?", (new, i+1) )
        connection.commit()
    for i in range(len(itemID)):
        ##update ItemOrdered table
        connection.execute("INSERT INTO ItemOrdered VALUES(?,?,?) ",(i+1, itemID[i],finalqty[i]) ) 
        connection.commit()
        ##update Order table
        #connection.execute("INSERT INTO Orders VALUES(?,?,?,?,?)",(i+1, cusname,'14/3/2023', is_mem, totalp))
        connection.commit()
    connection.close()

    #record transaction log
    with open('transactionlog.txt', 'r') as file:
        num = []
        lines = file.readlines()[1:]
        for line in lines:
            line = line.strip().split(',')
            if line[0].isdigit():
                num += [line[0]]

    with open('transactionlog.txt', 'a') as file:
        file.write(str(int(num[len(num)-1]) + 1) + ',' + cusname + ',' + '14/3/2023')
        for i in range(len(iordered)):
            file.write(',' + str(iordered[i]) + ',' + str(finalqty[i]))
        file.write('\n')
        
    return render_template('Confirmation.html', iordered = iordered, finalqty = finalqty, total=total, totalp=totalp, cusname=cusname, length=length, pp=pp, discount=discount, itemID=itemID)

if __name__=='__main__':
    app.run(port =2345)
        

