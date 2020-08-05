
import os, sys, requests, json, re
from flask import Flask, request, jsonify
from datetime import date

currentDate = str(date.today())


# Database Connection Start

import mysql.connector

my_db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="pia_flights_information"
)

print(my_db)
my_cursor = my_db.cursor()

# Database Connection End



app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAAn77QeHlcMBAPN2ARPqZAxXtbEJUjLNE1vDkxitksxeuRIq8DixWsUUx4YrsZBVrOSnrKQPzauZBeZBMKlTEeVI7dAB7L81Ujfrk9eQgYSAngg4ylZB5r0PEZBdEMyaXcaGY2zoSouaxrn34aFM3ZBSNBu5URiqRu9uCEPRrHctml0ZA7ToZCyy0ZBvb9VycVcF4ZD"


token_dict = {"access_token": PAGE_ACCESS_TOKEN}
# to send message, quick replies and galleries etc. we call the facebook graph messages API.
fb_api = "https://graph.facebook.com/v6.0/me/messages"
# to get the user's details, such as name, profile picture, location etc. we use facebook graph messenger profile API.
profile_api = "https://graph.facebook.com/v6.0/me/messenger_profile"
# this is a generic link for facebook graph API. It is useless as it is. I have concetenated links with it to use for myself in the code.
psid_url = "https://graph.facebook.com/"

carousel_json = {"message":{"attachment":{"type":"template","payload":{"template_type":"generic","elements":[{"title":"Lahore to Istanbul US$1,426 ","image_url":"https://aromatravel.com/wp-content/uploads/2015/05/PIA.jpg","subtitle":"→ Thu 30 Apr, 15:50 • 21h (2 stops)\n← Sun 10 May, 11:30 • 12h (1 stop)"},{"title":"Freelancing","image_url":"https://i.ibb.co/WgphLjx/freelance.jpg","subtitle":"This section will tell you the scope of Freelancing after any course\n👇👇👇","buttons":[{"type":"postback","title":"Scope of Courses?","payload":"freelance.scope"},{"type":"postback","title":"How can I get Work?","payload":"freelance.work"},{"type":"postback","title":"Do you Offer Jobs?","payload":"freelance.jobs"}]}]}}}}


welcome_message = "ASSALAM-U-ALAIKUM 🙂\n\n"

@app.route('/', methods=['GET'])
def verify():
    # Web verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Token Verified", 200



def scraping_script(sender_id):
    
    print("Here come the live scraping script once the Flights Data will be available:")
    

@app.route('/', methods=['POST'])

def webhook():
    # this print statement checks what input has been placed by the user. It is here for debugging purposes only.
    print(request.data)

    # this line of code extracts the json out of the user input.
    data = request.get_json()
    get_started_json = {"get_started": {"payload": "get started button"}}
    requests.post(profile_api, params=token_dict, data=json.dumps(get_started_json), headers={'Content-Type': 'application/json'})

    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:

                # IDs
                sender_id = messaging_event['sender']['id']
                recipient_id = messaging_event['recipient']['id']
                # using a GET request to extract the user's information. In the below lines of code, we get the name of the user. Now, we can call the user by his name.
                response = requests.get(psid_url + sender_id + "?fields=name&access_token=" + PAGE_ACCESS_TOKEN)
                user_json = json.loads(response.content)
                user_name = user_json["name"]

                if messaging_event.get('postback'):

                    # Handling get_started response
                    if messaging_event['postback'].get('payload') == 'get started button':
                        
                        requests.post(fb_api, params=token_dict, json={"recipient":{"id":sender_id},"sender_action":"typing_on"})
                        requests.post(fb_api, params=token_dict, json={"message": {"text": welcome_message + user_name + " Nice to meet you. 😊\nTravel Agent Chatbot at your service 🤖"}, "recipient": {"id": sender_id},"notification_type": "REGULAR","messaging_type": "RESPONSE"})
                        requests.post(fb_api, params=token_dict,json={"recipient": {"id": sender_id}, "messaging_type": "RESPONSE","message": {"text": "🏠 Where are you flying from?.","quick_replies": [{"content_type": "text", "title": "Islamabad","payload": "Islamabad"},{"content_type": "text", "title": "Lahore","payload": "Lahore"}]}})
                        return "ok", 200

                    elif messaging_event['postback'].get('payload') == 'Economy' or messaging_event['postback'].get('payload') == 'Executive Economy' or messaging_event['postback'].get('payload') == 'Business':

                        ticket_class = messaging_event['postback'].get('payload')
                      
                        f = open(sender_id + "ticketClass.txt", "w")
                        f.write(ticket_class)
                        f.close()

                        f = open(sender_id + ".txt", "r")
                        user_entered_info = f.read()
                        user_entered_info = user_entered_info.split("\n")
                        dep = user_entered_info[0]
                        arr = user_entered_info[1]
                        date = user_entered_info[2]
                        t_type = user_entered_info[3]

                        f = open(sender_id + "ticketClass.txt", "r")
                        t_class = f.read()
                        
                        # my_cursor.execute("SELECT * FROM flight_info where departure_city = " +"'"+dep+"'"+ " AND destination_city = " +"'"+arr+"'"+ " AND departure_date = " +"'"+date+"'"+ " AND ticket_class = " + "'"+t_class+"'")
                        my_cursor.execute("SELECT * FROM flight_info where departure_city = " +"'"+dep+"'"+ " AND destination_city = " +"'"+arr+"'"+ " AND departure_date = " +"'"+date+"'" + " AND ticket_type = " +"'"+t_type+"'")

                        myresult = my_cursor.fetchall()

                        try: 

                            departure_city = myresult[0][1]
                            destination_city = myresult[0][2]
                            departure_date = myresult[0][3]
                            departure_day = myresult[0][4]
                            ticket_type = myresult[0][5]
                            ticket_class = myresult[0][6]
                            departure_time = myresult[0][7]
                            departure_flightNo = myresult[0][8]
                            departure_flight_info = myresult[0][9]
                                
                            ticket_price = ''

                            if t_class == 'Economy':
                                departure_economy_ticket_price = myresult[0][10]
                                ticket_price = departure_economy_ticket_price

                            if t_class == 'Executive Economy':
                                departure_executive_economy_ticket_price = myresult[0][11]
                                ticket_price = departure_executive_economy_ticket_price

                            if t_class == 'Business':
                                departure_business_ticket_price = myresult[0][12]
                                ticket_price = departure_business_ticket_price

                            flight_details = "Departure_city: " + departure_city + "\nDestination_city: " + destination_city + "\nDeparture_date: " + str(departure_date) + "\nTicket_type: " + ticket_type + "\nTicket_class: " + t_class + "\nDeparture_time: " + str(departure_time) + "\nDeparture_flightNo: " + departure_flightNo + "\nTicket_price: " + ticket_price + "\nDeparture_flight_info: " + departure_flight_info 
                            
                            # requests.post(fb_api, params=token_dict,json={"recipient": {"id": sender_id}, "message":{"attachment":{"type":"template","payload":{"template_type":"button","text": flight_details, "buttons": [{"type": "web_url","url": "https://www.google.com","title": "Book Now"},{"type":"postback","payload":"Search Again","title":"Search Again"}]}}}})
                            requests.post(fb_api, params=token_dict, json={"recipient":{"id":sender_id},"sender_action":"typing_on"})
                            requests.post(fb_api, params=token_dict, json={"message": {"text": flight_details},"recipient": {"id": sender_id},"notification_type": "REGULAR","messaging_type": "RESPONSE"})
                            requests.post(fb_api, params=token_dict, json={"recipient":{"id":sender_id},"sender_action":"typing_on"})
                            requests.post(fb_api, params=token_dict,json={"recipient": {"id": sender_id}, "message":{"attachment":{"type":"template","payload":{"template_type":"button","text": "What do you want to do now? ", "buttons": [{"type": "web_url","url": "https://www.piac.com.pk/","title": "Book Now"},{"type":"postback","payload":"Search Again","title":"Search Again"}]}}}})
                            return "ok", 200    

                        except Exception:
                            # requests.post(fb_api, params=token_dict, json={"message": {"text": "📅 Sorry we couldn't find any Flight details for information you have entered! "},"recipient": {"id": sender_id},"notification_type": "REGULAR","messaging_type": "RESPONSE"})
                            requests.post(fb_api, params=token_dict,json={"recipient": {"id": sender_id}, "message":{"attachment":{"type":"template","payload":{"template_type":"button","text": "Sorry we couldn't find any Flight details for information you have entered!", "buttons": [{"type":"postback","payload":"Search Again","title":"Search Again"}]}}}})

                            return "ok", 200

                    elif messaging_event['postback'].get('payload') == 'Available Dates': 
                        requests.post(fb_api, params=token_dict, json={"recipient":{"id":sender_id},"sender_action":"typing_on"})

                        f = open(sender_id + ".txt", "r")
                        user_entered_info = f.read()
                        user_entered_info = user_entered_info.split("\n")
                        dep = user_entered_info[0]
                        arr = user_entered_info[1]

                        my_cursor.execute("SELECT DISTINCT departure_date FROM flight_info where departure_city = " +"'"+dep+"'"+ " AND destination_city = " +"'"+arr+"'")
                        myresult = my_cursor.fetchall()
                        
                        available_dates = ''
                        for date in myresult:
                            available_dates = available_dates + "\n 📅" +  str(date[0])


                        print("{ Available Dates:" + available_dates + " }")

                        requests.post(fb_api, params=token_dict,json={"recipient": {"id": sender_id}, "messaging_type": "RESPONSE","message": {"text": "These are available dates for the information you entered!! " + available_dates}})
                        requests.post(fb_api, params=token_dict, json={"message": {"text": "📅 When do you want to fly? (Format: yyyy-mm-dd) "},"recipient": {"id": sender_id},"notification_type": "REGULAR","messaging_type": "RESPONSE"})
                        return "ok", 200    
                    
                    elif messaging_event['postback'].get('payload') == 'Search Again': 
                        requests.post(fb_api, params=token_dict, json={"recipient":{"id":sender_id},"sender_action":"typing_on"})
                        requests.post(fb_api, params=token_dict,json={"recipient": {"id": sender_id}, "messaging_type": "RESPONSE","message": {"text": "🏠 Where are you flying from?.","quick_replies": [{"content_type": "text", "title": "Islamabad","payload": "Islamabad"},{"content_type": "text", "title": "Lahore","payload": "Lahore"}]}})
                        return "ok", 200    

                elif messaging_event.get('message'):
                    if messaging_event['message'].get('quick_reply'):
                        # Handling 'next' quick_reply
                        if messaging_event['message']['quick_reply'].get('payload') == 'Islamabad' or messaging_event['message']['quick_reply'].get('payload') == 'Lahore':
                            departure_city = messaging_event['message']['quick_reply'].get('payload')
                          
                            f = open(sender_id + ".txt", "w")
                            f.write(departure_city + "\n")
                            f.close()
                         
                            requests.post(fb_api, params=token_dict, json={"recipient":{"id":sender_id},"sender_action":"typing_on"})
                            requests.post(fb_api, params=token_dict,json={"recipient": {"id": sender_id}, "messaging_type": "RESPONSE","message": {"text": "🛬 What's your destination?", "quick_replies": [{"content_type": "text", "title": "Manchester","payload": "Manchester"},{"content_type": "text", "title": "Toronto", "payload": "Toronto"},{"content_type": "text", "title": "Istanbul","payload": "Istanbul"}]}})
                            return "ok", 200

                        elif messaging_event['message']['quick_reply'].get('payload') == 'Istanbul' or messaging_event['message']['quick_reply'].get('payload') == 'Manchester' or messaging_event['message']['quick_reply'].get('payload') == 'Toronto':
                            destination_city = messaging_event['message']['quick_reply'].get('payload')

                            f = open(sender_id + ".txt", "a")
                            f.write(destination_city + "\n")
                            f.close()
                            
                            requests.post(fb_api, params=token_dict, json={"recipient":{"id":sender_id},"sender_action":"typing_on"})
                            requests.post(fb_api, params=token_dict, json={"message": {"text": "📅 When do you want to fly? (Format: yyyy-mm-dd) "},"recipient": {"id": sender_id},"notification_type": "REGULAR","messaging_type": "RESPONSE"})
                            return "ok", 200

                        elif messaging_event['message']['quick_reply'].get('payload') == 'Return' or messaging_event['message']['quick_reply'].get('payload') == 'One Way':
                            ticket_type = messaging_event['message']['quick_reply'].get('payload')

                            f = open(sender_id + ".txt", "a")
                            f.write(ticket_type + "\n")
                            f.close()

                            # requests.post(fb_api, params=token_dict,json={"recipient": {"id": sender_id}, "messaging_type": "RESPONSE","message": {"text": "🙂 Please select a ticket class ", "quick_replies": [{"content_type": "text", "title": "Economy","payload": "Economy"},{"content_type": "text", "title": "Business", "payload": "Business"},{"content_type": "text", "title": "First Class","payload": "First Class"}]}})
                            
                            requests.post(fb_api, params=token_dict, json={"recipient":{"id":sender_id},"sender_action":"typing_on"})
                            requests.post(fb_api, params=token_dict,json={"recipient": {"id": sender_id}, "messaging_type": "RESPONSE","message": {"attachment": {"type": "image", "payload": {"url": "https://www.freevector.com/uploads/vector/preview/18653/CartoonAirplane_01_Preview.jpg","is_reusable": True}}}})
                            requests.post(fb_api, params=token_dict, json={"message": {"text": "⌛🙂 I’m looking for the best prices now and will be back in a moment!"},"recipient": {"id": sender_id},"notification_type": "REGULAR","messaging_type": "RESPONSE"})

                            f = open(sender_id + ".txt", "r")
                            user_entered_info = f.read()
                            user_entered_info = user_entered_info.split("\n")
                            dep = user_entered_info[0]
                            arr = user_entered_info[1]
                            date = user_entered_info[2]

                            my_cursor.execute("SELECT * FROM flight_info where departure_city = " +"'"+dep+"'"+ " AND destination_city = " +"'"+arr+"'"+ " AND departure_date = " +"'"+date+"'")
                            myresult = my_cursor.fetchall()

                            try: 
                                departure_city = myresult[0][1]

                                title  = dep + " to " + arr 
                                requests.post(fb_api, params=token_dict, json={"recipient":{"id":sender_id},"sender_action":"typing_on"})
                                requests.post(fb_api, params=token_dict, json={"recipient":{"id":sender_id},"message":{"attachment":{"type":"template","payload":{"template_type":"generic","elements":[{"title":title ,"image_url":"https://aromatravel.com/wp-content/uploads/2015/05/PIA.jpg","subtitle":"Departure Date: " + date ,"buttons":[{"type":"postback","payload":"Economy","title":"Economy"}]},{"title":title ,"image_url":"https://aromatravel.com/wp-content/uploads/2015/05/PIA.jpg","subtitle":"Departure Date: " + date ,"buttons":[{"type":"postback","payload":"Executive Economy","title":"Executive Economy"}]},{"title":title ,"image_url":"https://aromatravel.com/wp-content/uploads/2015/05/PIA.jpg","subtitle":"Departure Date: " + date ,"buttons":[{"type":"postback","payload":"Business","title":"Business"}]}]}}}})  
                                return "ok", 200

                            except Exception:
                                # requests.post(fb_api, params=token_dict, json={"message": {"text": "📅 Sorry we couldn't find any Flight details for information you have entered! "},"recipient": {"id": sender_id},"notification_type": "REGULAR","messaging_type": "RESPONSE"})
                                requests.post(fb_api, params=token_dict,json={"recipient": {"id": sender_id}, "message":{"attachment":{"type":"template","payload":{"template_type":"button","text": "Sorry we couldn't find any Flight details for information you have entered!", "buttons": [{"type":"postback","payload":"Search Again","title":"Search Again"}]}}}})
                                return "ok", 200

                            
                    elif messaging_event['message'].get('text'):
                        
                        if re.match("^[\d]{4}-[\d]{2}-[\d]{2}$",messaging_event['message'].get('text')):
                            
                            date = messaging_event['message'].get('text')
                            
                            currentDateChecker = currentDate.split("-")
                            currentYear = currentDateChecker[0]
                            currentMonth = currentDateChecker[1]
                            currentDay = currentDateChecker[2]

                            dateCheck = date.split("-")
                            year = dateCheck[0]
                            month = dateCheck[1]
                            day = dateCheck[2]

                            if int(month) <= 00 or int(month) > 12:
                                print("wrong month") 
                                requests.post(fb_api, params=token_dict, json={"message": {"text": "📅 You have entered incorrect month. Please enter valid month to proceed! "},"recipient": {"id": sender_id},"notification_type": "REGULAR","messaging_type": "RESPONSE"})
                                return "ok", 200
                            
                            elif ( month == '01' or month == '03' or month == '05' or month == '07' or month == '08' or month == '10' or month == '12' ) and ( int(day) <= 00 or int(day) > 31 ):
                                print("wrong day 1") 
                                requests.post(fb_api, params=token_dict, json={"message": {"text": "📅 You have entered incorrect day for 'Month-" + month + "'. Please enter valid day between '01-31' to proceed! "},"recipient": {"id": sender_id},"notification_type": "REGULAR","messaging_type": "RESPONSE"})
                                return "ok", 200

                            elif ( month == '04' or month == '06' or month == '09' or month == '11') and ( int(day) <= 00 or int(day) > 30 ):
                                print("wrong day 2") 
                                requests.post(fb_api, params=token_dict, json={"message": {"text": "📅 You have entered incorrect day for 'Month-" + month + "'. Please enter valid day between '01-30' to proceed! "},"recipient": {"id": sender_id},"notification_type": "REGULAR","messaging_type": "RESPONSE"})
                                return "ok", 200

                            elif month == '02' and int(day) <= 00:
                                print("wrong day 3") 
                                requests.post(fb_api, params=token_dict, json={"message": {"text": "📅 You have entered incorrect day '00' for 'Month-" + month + "'. Please enter valid day to proceed! "},"recipient": {"id": sender_id},"notification_type": "REGULAR","messaging_type": "RESPONSE"})
                                return "ok", 200
                                

                            elif int(year) < int(currentYear) or ( int(year) <= int(currentYear) and int(month) < int(currentMonth) ) or ( int(year) <= int(currentYear) and int(month) <= int(currentMonth) and int(day) < int(currentDay) ):
                                print("You may entered old/previous date, please enter current or future date")
                                requests.post(fb_api, params=token_dict, json={"message": {"text": "📅 No Flights information is available for old dates like '" + date + "'. Although, you can check Flights status for current or future date! "},"recipient": {"id": sender_id},"notification_type": "REGULAR","messaging_type": "RESPONSE"})
                                return "ok", 200

                            else:

                                leapYear = False
                            
                                if (int(year) % 4) == 0:  
                                    if (int(year) % 100) == 0:  
                                        if (int(year) % 400) == 0:   
                                            leapYear = True  
                                    else:    
                                        leapYear = True


                                if leapYear == True and int(day) > 29:
                                    print("{0} is a leap year".format(year))
                                    requests.post(fb_api, params=token_dict, json={"message": {"text": "📅 You have entered incorrect day for 'Month-" + month + "'. That is leap year so you can enter day between '01-29' to proceed! "},"recipient": {"id": sender_id},"notification_type": "REGULAR","messaging_type": "RESPONSE"})
                                    return "ok", 200

                                elif leapYear == False and int(day) > 28:
                                    print("{0} is not a leap year".format(year)) 
                                    requests.post(fb_api, params=token_dict, json={"message": {"text": "📅 You have entered incorrect day for 'Month-" + month + "'. That is not a leap year so you can only enter day between '01-28' to proceed! "},"recipient": {"id": sender_id},"notification_type": "REGULAR","messaging_type": "RESPONSE"})
                                    return "ok", 200

                                else:
                                    print("success")

                                    f = open(sender_id + ".txt", "a")
                                    f.write(date + "\n")
                                    f.close()

                                    f = open(sender_id + ".txt", "r")
                                    user_entered_info = f.read()
                                    user_entered_info = user_entered_info.split("\n")
                                    dep = user_entered_info[0]
                                    arr = user_entered_info[1]
                                    

                                    f = open(sender_id + ".txt", "r")
                                    user_entered_info = f.read().splitlines()
                                    date = user_entered_info[-1]

                                    my_cursor.execute("SELECT * FROM flight_info where departure_city = " +"'"+dep+"'"+ " AND destination_city = " +"'"+arr+"'"+ " AND departure_date = " +"'"+date+"'")
                                    myresult = my_cursor.fetchall()

                                    try: 
                                        departure_city = myresult[0][1]

                                        requests.post(fb_api, params=token_dict, json={"recipient":{"id":sender_id},"sender_action":"typing_on"})
                                        requests.post(fb_api, params=token_dict,json={"recipient": {"id": sender_id}, "messaging_type": "RESPONSE","message": {"text": "🙂 Please select a ticket type ", "quick_replies": [{"content_type": "text", "title": "Return","payload": "Return"},{"content_type": "text", "title": "One Way", "payload": "One Way"}]}})
                                        return "ok", 200

                                    except Exception:
                                        requests.post(fb_api, params=token_dict,json={"recipient": {"id": sender_id}, "message":{"attachment":{"type":"template","payload":{"template_type":"button","text": "Sorry we couldn't find any Flight details for \n 📅" + date , "buttons": [{"type":"postback","payload":"Available Dates","title":"Show Available Dates"}]}}}})
                                        return "ok", 200


                        else:
                            print("wrong format")
                            requests.post(fb_api, params=token_dict, json={
                                "message": {
                                    "text": "📅 You have entered incorrect date fromat. Please enter date in valid format (yyyy-mm-dd) to proceed! "
                                    },
                                "recipient": {
                                    "id": sender_id
                                    },
                                "notification_type": "REGULAR",
                                "messaging_type": "RESPONSE"
                                })
                            return "ok", 200


    return "ok", 200


if __name__ == "__main__":
    app.run(debug=True, port=80)



#requests.post(fb_api, params=token_dict,json={"message": {"text": destination_city}, "recipient": {"id": sender_id},"notification_type": "REGULAR", "messaging_type": "RESPONSE"})