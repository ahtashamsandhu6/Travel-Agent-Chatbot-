import mysql.connector

my_db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="pia_flights_information"
)


f = open("3663328647073043.txt", "r")
user_entered_info = f.read().splitlines()
user_entered_info = user_entered_info.split("\n")
dep = user_entered_info[0]
arr = user_entered_info[1]
date = user_entered_info[-1]

print(dep)
print(arr)
print(date)


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
