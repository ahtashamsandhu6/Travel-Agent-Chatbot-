import mysql.connector

my_db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="pia_flights_information"
)

f = open(sender_id + ".txt", "r")
user_entered_info = f.read()
user_entered_info = user_entered_info.split("\n")
dep = user_entered_info[0]
arr = user_entered_info[1]
# date = user_entered_info[2]
# t_type = user_entered_info[3]
f.close()

f = open(sender_id + ".txt", "r")
user_entered_info = f.read().splitlines()
date = user_entered_info[-2]
t_type = user_entered_info[-1]
f.close()

f = open(sender_id + "ticketClass.txt", "r")
t_class = f.read()

# my_cursor.execute("SELECT * FROM flight_info where departure_city = " +"'"+dep+"'"+ " AND destination_city = " +"'"+arr+"'"+ " AND departure_date = " +"'"+date+"'"+ " AND ticket_class = " + "'"+t_class+"'")
my_cursor.execute("SELECT * FROM flight_info where departure_city = " +"'"+dep+"'"+ " AND destination_city = " +"'"+arr+"'"+ " AND departure_date = " +"'"+date+"'" + " AND ticket_type = " +"'"+t_type+"'")

myresult = my_cursor.fetchall()


# print(my_db)
# my_cursor = my_db.cursor()

# dep = 'Lahore'
# arr = 'Manchester'
# ticket_type = 'One Wa'
# user_entered_date = '2020-05-15'

# dep = "Lahore"
# arr = "Istanbul"

# my_cursor.execute("SELECT DISTINCT departure_date FROM flight_info where departure_city = " +"'"+dep+"'"+ " AND destination_city = " +"'"+arr+"'")
# myresult = my_cursor.fetchall()

# available_dates = list()
# dd = ''
# for date in myresult:
#     dd = dd + "\n   " +  str(date[0])


# print("{ Available Dates:" + dd + " }")

# mylist = list()
# mylist.append("2020-12-11")
# mylist.append(2)
# mylist.append(3)
# print(mylist)

# flag = False
# try:
#     if myresult:
#         flag = True
# except Exception:
    # print("no flights available for date, you entered")
