
import os, sys, requests, json, re
from flask import Flask, request, jsonify



app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAAn77QeHlcMBAPN2ARPqZAxXtbEJUjLNE1vDkxitksxeuRIq8DixWsUUx4YrsZBVrOSnrKQPzauZBeZBMKlTEeVI7dAB7L81Ujfrk9eQgYSAngg4ylZB5r0PEZBdEMyaXcaGY2zoSouaxrn34aFM3ZBSNBu5URiqRu9uCEPRrHctml0ZA7ToZCyy0ZBvb9VycVcF4ZD"



token_dict = {"access_token": PAGE_ACCESS_TOKEN}
# to send message, quick replies and galleries etc. we call the facebook graph messages API.
fb_api = "https://graph.facebook.com/v6.0/me/messages"
# to get the user's details, such as name, profile picture, location etc. we use facebook graph messenger profile API.
profile_api = "https://graph.facebook.com/v6.0/me/messenger_profile"
# this is a generic link for facebook graph API. It is useless as it is. I have concetenated links with it to use for myself in the code.
psid_url = "https://graph.facebook.com/"
 
departure_city = ''
destination_city = ''
date = ''
ticket_type = ''
ticket_class = ''

carousel_json = {"message":{"attachment":{"type":"template","payload":{"template_type":"generic","elements":[{"title":"Lahore to Istanbul US$1,426 ","image_url":"https://aromatravel.com/wp-content/uploads/2015/05/PIA.jpg","subtitle":"→ Thu 30 Apr, 15:50 • 21h (2 stops)\n← Sun 10 May, 11:30 • 12h (1 stop)"},{"title":"Freelancing","image_url":"https://i.ibb.co/WgphLjx/freelance.jpg","subtitle":"This section will tell you the scope of Freelancing after any course\n👇👇👇","buttons":[{"type":"postback","title":"Scope of Courses?","payload":"freelance.scope"},{"type":"postback","title":"How can I get Work?","payload":"freelance.work"},{"type":"postback","title":"Do you Offer Jobs?","payload":"freelance.jobs"}]}]}}}}


welcome_message = "ASSALAM-U-ALAIKUM 🙂\n\n"

@app.route('/', methods=['GET'])
def verify():
    # Web verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello World", 200


@app.route('/', methods=['POST'])
def webhook(departure_city):
    # this print statement checks what input has been placed by the user. It is here for debugging purposes only.
    print(request.data)

    # this line of code extracts the json out of the user input.
    data = request.get_json()
    get_started_json = {"get_started": {"payload": "some bitch clicked the get started button"}}
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
                    if messaging_event['postback'].get('payload') == 'some bitch clicked the get started button':
                        requests.post(fb_api, params=token_dict, json={"message": {"text": welcome_message + user_name + " Nice to meet you. 😊\nTravel Agent Chatbot at your service 🤖"}, "recipient": {"id": sender_id},"notification_type": "REGULAR","messaging_type": "RESPONSE"})
                        requests.post(fb_api, params=token_dict,json={"recipient": {"id": sender_id}, "messaging_type": "RESPONSE","message": {"text": "🏠 Where are you flying from?.","quick_replies": [{"content_type": "text", "title": "Islamabad","payload": "Islamabad"},{"content_type": "text", "title": "Lahore","payload": "Lahore"}]}})
                        return "ok", 200
                elif messaging_event.get('message'):
                    if messaging_event['message'].get('quick_reply'):
                        # Handling 'next' quick_reply
                        if messaging_event['message']['quick_reply'].get('payload') == 'Islamabad' or messaging_event['message']['quick_reply'].get('payload') == 'Lahore':
                            departure_city = messaging_event['message']['quick_reply'].get('payload')
                            requests.post(fb_api, params=token_dict,json={"recipient": {"id": sender_id}, "messaging_type": "RESPONSE","message": {"text": "🛬 What's your destination?", "quick_replies": [{"content_type": "text", "title": "Manchester","payload": "Manchester"},{"content_type": "text", "title": "Toronto", "payload": "Toronto"},{"content_type": "text", "title": "Istanbul","payload": "Istanbul"}]}})
                            return "ok", 200
                        elif messaging_event['message']['quick_reply'].get('payload') == 'Istanbul' or messaging_event['message']['quick_reply'].get('payload') == 'Manchester' or messaging_event['message']['quick_reply'].get('payload') == 'Toronto':
                            destination_city = messaging_event['message']['quick_reply'].get('payload')
                            requests.post(fb_api, params=token_dict, json={"message": {"text": "📅 When do you want to fly? Say dates like: May 15 "},"recipient": {"id": sender_id},"notification_type": "REGULAR","messaging_type": "RESPONSE"})
                            return "ok", 200
                        elif messaging_event['message']['quick_reply'].get('payload') == 'Return' or messaging_event['message']['quick_reply'].get('payload') == 'One Way' or messaging_event['message']['quick_reply'].get('payload') == 'Both':
                            ticket_type = messaging_event['message']['quick_reply'].get('payload')
                            requests.post(fb_api, params=token_dict,json={"recipient": {"id": sender_id}, "messaging_type": "RESPONSE","message": {"text": "🙂 Please select a ticket class ", "quick_replies": [{"content_type": "text", "title": "Economy","payload": "Economy"},{"content_type": "text", "title": "Business", "payload": "Business"},{"content_type": "text", "title": "First Class","payload": "First Class"},{"content_type": "text", "title": "Any","payload": "Any"}]}})
                            return "ok", 200
                        elif messaging_event['message']['quick_reply'].get('payload') == 'Economy' or messaging_event['message']['quick_reply'].get('payload') == 'Business' or messaging_event['message']['quick_reply'].get('payload') == 'First Class' or messaging_event['message']['quick_reply'].get('payload') == 'Any':
                            ticket_class = messaging_event['message']['quick_reply'].get('payload')
                            requests.post(fb_api, params=token_dict,json={"recipient": {"id": sender_id}, "messaging_type": "RESPONSE","message": {"attachment": {"type": "image", "payload": {"url": "https://www.freevector.com/uploads/vector/preview/18653/CartoonAirplane_01_Preview.jpg","is_reusable": True}}}})
                            requests.post(fb_api, params=token_dict, json={"message": {"text": "⌛🙂 I’m looking for the best prices now and will be back in a moment!"},"recipient": {"id": sender_id},"notification_type": "REGULAR","messaging_type": "RESPONSE"})
                            # requests.post(fb_api, params=token_dict, json={"recipient":{"id":sender_id},"message":{"attachment":{"type":"template","payload":{"template_type":"generic","elements":[{"title": "'" + departure_city + " to " + destination_city + "PKR 20,000" + "'","image_url":"https://aromatravel.com/wp-content/uploads/2015/05/PIA.jpg","subtitle":"→ Thu 30 Apr, 15:50 • 21h (2 stops)\n← Sun 10 May, 11:30 • 12h (1 stop)"}]}}}})
                            requests.post(fb_api, params=token_dict, json={"recipient":{"id":sender_id},"message":{"attachment":{"type":"template","payload":{"template_type":"generic","elements":[{"title":"'" + str(departure_city) + "'" + "to islambad PKR 20,000","image_url":"https://aromatravel.com/wp-content/uploads/2015/05/PIA.jpg","subtitle":"→ Thu 30 Apr, 15:50 • 21h (2 stops)\n← Sun 10 May, 11:30 • 12h (1 stop)"}]}}}})
                            return "ok", 200
                    elif messaging_event['message'].get('text'):
                        if re.search("[a-zA-Z]+ +[0-9]",messaging_event['message'].get('text')):
                            date = messaging_event['message'].get('text')
                            requests.post(fb_api, params=token_dict,json={"recipient": {"id": sender_id}, "messaging_type": "RESPONSE","message": {"text": "🙂 Please select a ticket type ", "quick_replies": [{"content_type": "text", "title": "Return","payload": "Return"},{"content_type": "text", "title": "One Way", "payload": "One Way"},{"content_type": "text", "title": "Both","payload": "Both"}]}})
                            return "ok", 200




    return "ok", 200





if __name__ == "__main__":
    app.run(debug=True, port=80)



#requests.post(fb_api, params=token_dict,json={"message": {"text": destination_city}, "recipient": {"id": sender_id},"notification_type": "REGULAR", "messaging_type": "RESPONSE"})