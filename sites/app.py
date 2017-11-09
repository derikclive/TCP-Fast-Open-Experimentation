from flask import Flask, render_template, json, request
import os
from flask import  redirect, url_for
from werkzeug.utils import secure_filename
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

mysql = MySQL()
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'Project'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/homepage')
def homepage():
    return render_template('initial.html')

@app.route('/')
def main():
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/user')
def user():
    return render_template('user.html')

@app.route('/userHistory')
def user_history():
    return render_template('history.html')

@app.route('/user-cart')
def user_cart():
    return render_template('user-cart.html')


@app.route('/admin-dashboard')
def admin_dashboard():
    return render_template('admin-items.html')

@app.route('/adminSignIn', methods=['POST','GET'])
def adminSignIn():
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT CmID from CanteenManager where Username='" + _email + "' and Password='" + _password + "'")
    data = cursor.fetchone()
    if data is not None:
        print('\nLogged in successfully')
        return json.dumps({'success':True}),200
    else:
        print('\nUsername or Password is wrong')
        return json.dumps({'error':True}),400


@app.route('/signIn',methods=['POST','GET'])
def signIn():
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT Password from Student where EmailID='" + _email + "'")
    data = cursor.fetchone()
    # print(data)
    if data is not None and check_password_hash(data[0], _password):
        print('\nLogged in successfully')
        return json.dumps({'success':True}), 200, {'message':'Logged in successfully'}
    else:
        print('\nUsername or Password is wrong')
        return json.dumps({'success':False}), 400, {'error':'Username or Password is wrong'}


@app.route('/signUp',methods=['POST','GET'])
def signUp():

    _firstName = request.form['inputFirstName']
    _lastName = request.form['inputLastName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
    _roomNo = request.form['roomNo']
    _floor = request.form['floor']
    _hostelName = request.form['hostelName']
    _phoneNumber = request.form['Pnumber']
    # validate the received values
    if _firstName and _lastName and _email and _password and _roomNo and _floor and _hostelName and _phoneNumber:
        conn = mysql.connect()
        cursor = conn.cursor()
        _hashed_password = generate_password_hash(_password)
        cursor.callproc('sign_up',(_firstName,_lastName, _email, _hashed_password, _roomNo, _floor, _hostelName, _phoneNumber))
        data = cursor.fetchall()

        if len(data) is 0:
            conn.commit()
            return json.dumps({'success':True}), 200, {'message':'User created successfully !'}
        else:
            return json.dumps({'success':False}), 400, {'error':str(data[0])}

    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})

@app.route('/add-item', methods=['POST', 'GET'])
def add_item():
    _item = request.form['item']
    _price = request.form['price']
    if request.method == 'POST':
        # check if the post request has the file part
        _file = request.files['file_photo']
    _preparationTime = request.form['prepTime']
    _availability = request.form['availability']
    _cemail = request.form['cemail']
    _category = request.form['category']


    if _item and _price and _file and _preparationTime and _availability and _cemail:
        conn = mysql.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT CmID from CanteenManager where username = '" + _cemail + "'")
        _CmID = cursor.fetchone()
        _CmID = _CmID[0]
        print(_CmID)
        cursor.callproc('add_item', (_item, _price, _availability, UPLOAD_FOLDER + '/' + _file.filename, _preparationTime, _CmID, _category))
        data = cursor.fetchone()
        filename = secure_filename(_file.filename)
        _file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        if data is None:
            conn.commit()
            return json.dumps({'success':True})
        else:
            return json.dumps({'success':False}), 400, {'error':str(data[0])}
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})
    # return json.dumps({'success':True})

@app.route('/delete-item', methods=['POST', 'GET'])
def delete_item():
    _itemId = request.form['id'];
    if _itemId:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('delete_item', (_itemId , ))
        data = cursor.fetchone()

        if data is None:
            conn.commit()
            return json.dumps({'success':True}), 200, {'message':'Item deleted successfully !'}
        else:
            return json.dumps({'success':False}), 400, {'error':str(data[0])}
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})

@app.route('/display-item', methods=['POST', 'GET'])
def display_item():
    _cemail = request.form['cemail']
    conn = mysql.connect()
    cursor = conn.cursor()
    print("hi")
    cursor.execute("SELECT CmID from CanteenManager where username = '" + _cemail + "'")
    _CmID = cursor.fetchone()
    _CmID = str(_CmID[0])
    print(_CmID)
    cursor.execute("SELECT * FROM FoodItem where CmID = " + _CmID)
    data = cursor.fetchall()
    return json.dumps(data),200

@app.route('/display-item-by-nc', methods=['POST', 'GET'])
def display_item_by_nc():
    name = request.form['name']
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT NcID from NightCanteen where Name = '" + name + " ';")
    NcID = cursor.fetchone()
    NcID = str(NcID[0])
    cursor.execute("SELECT CmID from CanteenManager where NcID = " + NcID + ";")
    CmID = cursor.fetchone()
    CmID = str(CmID[0]);
    command ="SELECT * FROM FoodItem where CmID = " + CmID + " and Availability=1;"
    cursor.execute(command)
    data = cursor.fetchall()
    return json.dumps(data)

@app.route('/display-cart', methods=['POST', 'GET'])
def display_from_temp():
    username = request.form['username']
    username = username.split('@')[0]
    conn = mysql.connect()
    cursor = conn.cursor()
    command = "SELECT * FROM " + username + ", FoodItem where FoodItem.FoodID=" + username +".FoodID"
    cursor.execute(command)
    data = cursor.fetchall()
    return json.dumps(data),200

@app.route('/create_temp_table', methods=['POST', 'GET'])
def create_temp_table():
    username = request.form['username']
    username = username.split('@')[0]
    conn = mysql.connect()
    cursor = conn.cursor()
    command = "SELECT COUNT(*) FROM information_schema.`tables` WHERE table_schema = 'Project' and table_name = '" + username + "'"
    cursor.execute(command)
    data = cursor.fetchone()
    print(data)
    if data[0] == 0:
        command = "create table " + username + " (FoodID int not null Primary Key, Quantity int not null);"
        cursor.execute(command)
        conn.commit()
    return json.dumps({'success':True}), 200

@app.route('/delete_temp_table', methods=['POST', 'GET'])
def delete_temp_table():
    username = request.form['username']
    username = username.split('@')[0]
    conn = mysql.connect()
    cursor = conn.cursor()
    command = "SELECT COUNT(*) FROM information_schema.`tables` WHERE table_schema = 'Project' and table_name = '" + username + "'"
    cursor.execute(command)
    data = cursor.fetchone()
    if data[0] >= 0:
        cursor.execute("drop table "+ username + " ")
        conn.commit()
    return json.dumps({'success':True}), 200

@app.route('/add_to_temp', methods=['POST', 'GET'])
def add_to_temp():
    Quantity = request.form['Quantity']
    FoodID = request.form['FoodID']
    username = request.form['username']
    username = username.split('@')[0]
    conn = mysql.connect()
    cursor = conn.cursor()
    command = "SELECT COUNT(*) FROM information_schema.`tables` WHERE table_schema = 'Project' and table_name = '" + username + "'"
    cursor.execute(command)
    data = cursor.fetchone()
    if data[0] >= 0:
        command = "INSERT INTO " + username + " values (" + str(FoodID) + ", " + str(Quantity) + ")"
        print(command)
        cursor.execute(command)
        conn.commit()
    return json.dumps({'success':True}), 200

@app.route('/delete_from_temp', methods=['POST', 'GET'])
def delete_from_temp():
    FoodID = request.form['FoodID']
    username = request.form['username']
    username = username.split('@')[0]
    conn = mysql.connect()
    cursor = conn.cursor()
    command = "SELECT COUNT(*) FROM information_schema.`tables` WHERE table_schema = 'Project' and table_name = '" + username + "'"
    cursor.execute(command)
    data = cursor.fetchone()
    if data[0] >= 0:
        cursor.execute("DELETE FROM " + username + " WHERE FoodID = '" + str(FoodID) + "'")
        conn.commit()
    return json.dumps({'success':True}), 200

@app.route('/query', methods=['POST', 'GET'])
def search():
    name_nc = request.form['name_nc']
    query = request.form['query']
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT NcID from NightCanteen where Name = '" + name_nc + "';")
    NcID = cursor.fetchone()
    NcID = str(NcID[0])
    cursor.execute("SELECT CmID from CanteenManager where NcID = " + NcID)
    CmID = cursor.fetchone()
    CmID = str(CmID[0])
    command ="SELECT * FROM FoodItem where Name like '%" + query + "%' and CmID = "+ CmID +";"
    print(command)
    cursor.execute(command)
    data = cursor.fetchall()
    return json.dumps(data)

@app.route('/submit-order', methods=['POST', 'GET'])
def submitOrder():
    username = request.form['username']
    name = request.form['nc_name']
    total = request.form['total']

    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT NcID from NightCanteen where Name = '" + name + "'")
    NcID = cursor.fetchone()[0]

    cursor.execute("SELECT CmID from CanteenManager where NcID = " + str(NcID))
    CmID = cursor.fetchone()[0]

    cursor.execute("SELECT SID from Student where EmailID = '" + username + "'")
    SID = cursor.fetchone()[0]
    cursor.callproc('create_order', (total, SID, CmID))

    conn.commit()

    cursor.execute("SELECT Max(OrderID) FROM Orders")
    OrderID = cursor.fetchone()[0]
    cursor.callproc('add_student_order', (SID, OrderID))

    username = username.split('@')[0]
    command ="SELECT * FROM " + username
    cursor.execute(command)
    data = cursor.fetchall()
    for item in data:
        cursor.callproc('add_order_item', (OrderID, item[0], item[1]))
    conn.commit()
    return json.dumps(data),200

# delivery boy

@app.route('/add-delivery-boy', methods=['POST', 'GET'])
def add_delivery_boy():
    username = request.form['username']
    name = request.form['DBoy']
    regno = request.form['regno']
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT CmID from CanteenManager where Username = '" + username + "'")
    CmID = cursor.fetchone()[0]
    cursor.execute('insert into DeliveryBoy(Name, RegNo, CmID) values("' + name + '", ' + str(regno) + ', ' + str(CmID) + ')')
    conn.commit()
    return json.dumps({'success':True}),200

@app.route('/get-dboys-list', methods=['POST', 'GET'])
def get_dboys_list():
    username = request.form['username']
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT CmID from CanteenManager where Username = '" + username + "'")
    CmID = cursor.fetchone()[0]
    cursor.execute("select * from DeliveryBoy where CmID = " + str(CmID))
    dboys = cursor.fetchall()
    return json.dumps(dboys),200

@app.route('/admin-display-orders', methods=['POST', 'GET'])
def admin_display_orders():
    username = request.form['username']
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT CmID from CanteenManager where Username = '" + username + "'")
    CmID = cursor.fetchone()[0]
    command = "select * from Orders where CmID = " + str(CmID) + " and Status not in ('Prepared', 'Rejected')"
    cursor.execute(command)
    data = cursor.fetchall()
    return json.dumps(data),200

@app.route('/get-order-details', methods=['POST', 'GET'])
def get_order_details():
    OrderID = request.form['OrderID']
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('select UserID from Orders where OrderID=' + OrderID)
    userID = cursor.fetchone()[0]
    command = 'select P.*, Q.FoodID, Q.Quantity from Orders P, Items Q where P.OrderID=Q.OrderID and P.OrderID = ' + str(OrderID)
    command2 = 'select FoodItem.Name, FoodItem.Price, A.Quantity from FoodItem, (' + command + ') as A where FoodItem.FoodID=A.FoodID'
    cursor.execute(command2)
    data = cursor.fetchall()
    return json.dumps(data)

@app.route('/get-order-details-2', methods=['POST', 'GET'])
def get_order_details_2():
    OrderID = request.form['OrderID']
    conn = mysql.connect()
    cursor = conn.cursor()
    command = 'select * from Orders where OrderID = ' + str(OrderID) + ' LIMIT 1'
    command2 = 'select A.OrderID, A.ODate, A.Total, CONCAT(B.FirstName, " ", B.LastName) as Name, CONCAT(RoomNo, " " , Floor, " ", BlockName) as Address from (' + command + ') as A, Student B where A.UserID=B.SID'
    cursor.execute(command2)
    data = cursor.fetchall()
    return json.dumps(data)

@app.route('/remove-delivery-boy', methods=['POST', 'GET'])
def remove_delivery_boy():
    name = request.form['DBoy']
    regno = request.form['regno']
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('delete from DeliveryBoy where Name="' + name + '" and RegNo = ' + regno)
    conn.commit()
    return json.dumps({'success':True}),200

@app.route('/accept-reject', methods=['POST', 'GET'])
def accept_reject():
    accrej = request.form['accorrej']
    OrderID = request.form['OrderID']
    dBoy = request.form['dBoy']
    conn = mysql.connect()
    cursor = conn.cursor()
    if accrej == "0":
        command = 'update Orders set Status="Rejected" where OrderID=' + OrderID
        cursor.execute(command)
    else:
        command = 'update Orders set Status="Prepared" where OrderID=' + OrderID
        cursor.execute(command)
        command = 'update Orders set DBoy="' + dBoy + '" where OrderID=' + OrderID
        cursor.execute(command)
    conn.commit()
    return json.dumps({'success':True}),200

@app.route('/rate-food-item', methods=['POST', 'GET'])
def rate_food_item():
    rating = request.form['rating']
    FoodID = request.form['FoodID']
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('select num_rating, Ratings from FoodItem where FoodID = ' + str(FoodID))
    data = cursor.fetchone()
    cur_rating = data[1]
    num_ratings = data[0]
    new_rating = int((int(cur_rating) * int(num_ratings) + (num_ratings + 1)*int(rating)) / (int(num_ratings) + 1))
    num_ratings += 1
    print('update FoodItem set Ratings = ' + str(new_rating) + ', num_rating = ' + str(num_ratings) + ' where FoodID=' + str(FoodID))
    cursor.execute('update FoodItem set Ratings = ' + str(new_rating) + ', num_rating = ' + str(num_ratings) + ' where FoodID=' + str(FoodID))
    conn.commit()
    return json.dumps({'success':True}),200

@app.route('/order-history', methods=['POST', 'GET'])
def order_history():
    username = request.form['username']
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT SID from Student where EmailID = '" + username + "'")
    SID = cursor.fetchone()[0]
    cursor.execute('select OrderID, ODate, Status, Total from Orders where UserID = ' + str(SID) + ' order by ODate')
    data = cursor.fetchall()
    conn.commit()
    return json.dumps(data)

@app.route('/display-item-by-category', methods=['POST', 'GET'])
def display_item_by_category():
    name = request.form['name']
    category = request.form['category']
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT NcID from NightCanteen where Name = '" + name + " ';")
    NcID = cursor.fetchone()
    NcID = str(NcID[0])
    cursor.execute("SELECT CmID from CanteenManager where NcID = " + NcID + ";")
    CmID = cursor.fetchone()
    CmID = str(CmID[0]);
    command ="SELECT * FROM FoodItem where CmID = " + CmID + " and Category = '" + category + "' and Availability=1"
    cursor.execute(command)
    data = cursor.fetchall()
    return json.dumps(data)

def create_database():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("""SELECT COUNT(DISTINCT `table_name`) FROM `information_schema`.`columns` WHERE `table_schema` = 'Project'""")
    data = cursor.fetchone()
    if data[0] == 0:
        cursor.execute("""create table Student(
                        SID int not null primary key auto_increment,
                        FirstName varchar(20) not null,
                        LastName varchar(20) not null,
                        PhoneNumber bigint unique,
                        EmailID varchar(20) not null unique,
                        RoomNo varchar(10) not null,
                        Floor varchar(10) not null,
                        BlockName varchar(30) not null,
			            Password longtext not null);
                        """)

        cursor.execute("""
                        CREATE DEFINER=`root`@`localhost` PROCEDURE `sign_up`(IN p_fname varchar(20), IN p_lname varchar(20), IN p_email varchar(20), IN p_password longtext, IN p_roomNo varchar(10), IN p_floor varchar(10), IN p_blockName varchar(30), IN p_phoneNumber bigint)
                        begin
                        if ( select exists (select 1 from Student where EmailID = p_email) ) THEN
                        select "Email aldready registered!";
                        else
                        insert into Student(FirstName, LastName, EmailID, Password, RoomNo, Floor, BlockName, PhoneNumber) values(p_fname, p_lname, p_email, p_password, p_roomNo, p_floor, p_blockName, p_phoneNumber);
                        end if;
                        end
                        """)

        cursor.execute("""create table NightCanteen(
                        NcID int not null primary key auto_increment,
                        Name varchar(40) not null,
                        Location varchar(100) not null,
                        StartTime time not null,
                        EndTime time not null);
                        """)

        cursor.execute("""create table NPhone(
                        NcID int not null,
                        PhoneNumber bigint not null,
                        primary key(NcID, PhoneNumber),
                        foreign key(NcID) references NightCanteen(NcID));
                        """)

        cursor.execute("""create table CanteenManager(
                        CmID int not null primary key auto_increment,
                        Name varchar(40) not null,
                        NcID int not null,
                        Username varchar(30) not null,
                        Password varchar(100) not null);
                        """)
        cursor.execute("INSERT INTO CanteenManager(Name, NcID, Username, Password) VALUES('ask', 1, 'ask@gmail.com', 'password1');")
        cursor.execute("INSERT INTO NightCanteen(NcID, Name, Location, StartTime, EndTime) VALUES(1,'3rd Block' , 'NITK' ,'00:00:00', '00:00:00');")
        cursor.execute("INSERT INTO NPhone(NcID, PhoneNumber) VALUES(1,12);")

        cursor.execute("INSERT INTO CanteenManager(Name, NcID, Username, Password) VALUES('derik', 2, 'derik@gmail.com', 'password2');")
        cursor.execute("INSERT INTO NightCanteen(NcID, Name, Location, StartTime, EndTime) VALUES(2,'8th Block' , 'NITK' ,'00:00:00', '00:00:00');")
        cursor.execute("INSERT INTO NPhone(NcID, PhoneNumber) VALUES(2,78);")

        cursor.execute("INSERT INTO CanteenManager(Name, NcID, Username, Password) VALUES('vilas', 3, 'vilas@gmail.com', 'password3');")
        cursor.execute("INSERT INTO NightCanteen(NcID, Name, Location, StartTime, EndTime) VALUES(3,'7th Block' , 'NITK' ,'00:00:00', '00:00:00');")
        cursor.execute("INSERT INTO NPhone(NcID, PhoneNumber) VALUES(3,56);")

        cursor.execute("INSERT INTO CanteenManager(Name, NcID, Username, Password) VALUES('sagar', 4, 'sagar@gmail.com', 'password4');")
        cursor.execute("INSERT INTO NightCanteen(NcID, Name, Location, StartTime, EndTime) VALUES(4,'Girls Block' , 'NITK' ,'00:00:00', '00:00:00');")
        cursor.execute("INSERT INTO NPhone(NcID, PhoneNumber) VALUES(4,34);")

        cursor.execute("""create table FoodItem
                        (FoodID int not null primary key auto_increment,
                        Name varchar(20) not null, Price int not null,
                        Availability int not null,
                        ImageURL varchar(100),
                        PreparationTime int not null,
                        CmID int,
                        Category varchar(50),
                        Ratings int,
                        num_rating int,
                        foreign key(CmID) references CanteenManager(CmID));
                        """)

        cursor.execute("""
                        CREATE DEFINER=`root`@`localhost` PROCEDURE `delete_item`(IN p_foodId int)
                        begin
                        if ( select not exists(select 1 from FoodItem where FoodID = p_foodId) )
                        THEN select "Food Item doesn't exist!";
                        else
                        delete from FoodItem where FoodID = p_foodId;
                        end if;
                        end
                        """)

        cursor.execute("""
                        CREATE DEFINER=`root`@`localhost` PROCEDURE `add_item`( IN p_name varchar(20), IN p_price int, IN p_availability int, IN p_imageUrl varchar(100), IN p_preparationTime int, IN p_cmID int, IN p_Category varchar(50))
                        begin
                        insert into FoodItem(Name, Price, Availability, ImageURL, PreparationTime, CmID, num_rating, Ratings, Category) values(p_name, p_price, p_availability, p_imageUrl, p_preparationTime, p_cmID, 0, 0, p_Category);
                        end
                        """)

        cursor.execute("""create table Items(
                        OrderID int not null,
                        FoodID int not null,
                        Quantity int not null,
                        primary key(OrderID,FoodID,Quantity));
                        """)

        cursor.execute("""create table StudentOrder(
                        SID int not null,
                        OrderID int not null,
                        primary key(SID,OrderID));
                        """)
        cursor.execute("""create table Orders
                        (OrderID int not null primary key auto_increment,
                        ODate date not null,
                        Total int not null,
                        UserID int not null,
                        Status enum ('Waiting Confirmation',  'Prepared', 'Accepted', 'Rejected', 'Delievered'),
                        CmID int,
                        DBoy varchar(50),
                        foreign key(CmID) references CanteenManager(CmID) );
                        """)

        cursor.execute("""
                        CREATE DEFINER=`root`@`localhost` PROCEDURE `add_order_item`( IN p_orderID int, IN p_foodID int, IN p_quantity int)
                        begin
                        insert into Items(OrderID, FoodID, Quantity) values(p_orderID, p_foodID, p_quantity);
                        end
                        """)

        cursor.execute("""
                        CREATE DEFINER=`root`@`localhost` PROCEDURE `add_student_order`( IN p_SID int, IN p_orderID int)
                        begin
                        insert into StudentOrder(SID, OrderID) values(p_SID, p_orderID);
                        end
                        """)

        cursor.execute("""
                        CREATE DEFINER=`root`@`localhost` PROCEDURE `create_order`(IN p_total int, IN p_userID int, IN p_cmID int)
                        begin
                        declare currentDate date;
                        select CURDATE() into currentDate;
                        insert into Orders(ODate, Total, UserID, CmID, Status) values(currentDate, p_total, p_userID, p_cmID, 'Waiting Confirmation');
                        end
                        """)

        cursor.execute("""create table DeliveryBoy(
                        Name varchar(30) not null,
                        RegNo varchar(30) not null,
                        CmID int not null,
                        primary key(Name, RegNo),
                        foreign key(CmID) references CanteenManager(CmID)
                        );
                        """)

if __name__ == "__main__":
    create_database()
    app.run(port=5000)
