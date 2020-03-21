import os, sys
from flask import Flask, request
from wit import Wit
from pymessenger import Bot



access_token = "E64TH2ZX2EXC6VN26ORIZRD6LQ3VHYA4"

client = Wit(access_token = access_token)
# message_text = "i want sport news "

def wit_response(message_text):
    resp = client.message(message_text)
    entity = None
    value = None

    try:
        entity = List(resp['entities'])[0]
        value = resp['entities'][entity][0]['value']

    except:
        pass

    return (entity, value)



app = Flask(__name__)

PAGE_ACCESS_TOKEN="EAAn77QeHlcMBAPN2ARPqZAxXtbEJUjLNE1vDkxitksxeuRIq8DixWsUUx4YrsZBVrOSnrKQPzauZBeZBMKlTEeVI7dAB7L81Ujfrk9eQgYSAngg4ylZB5r0PEZBdEMyaXcaGY2zoSouaxrn34aFM3ZBSNBu5URiqRu9uCEPRrHctml0ZA7ToZCyy0ZBvb9VycVcF4ZD"

bot = Bot(PAGE_ACCESS_TOKEN)

@app.route('/',methods=['GET'])
def verify():
     # Web verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello World", 200

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    log(data)

    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:

                # IDs
                sender_id = messaging_event['sender']['id']
                recipient_id = messaging_event['recipient']['id']

                if messaging_event.get('message'):

                    if 'text' in messaging_event['message']:
                        messaging_text = messaging_event['message']['text']

                    else:
                        messaging_text = "no text"

                    response = None

                    entity, value = wit_response(messaging_text)

                    if entity == 'newstype':
                        response = 'Ok i am sending you {} news'.format(str(value))

                    elif entity == 'location':
                        response = 'Ok, you live in {0}. i will send you top headlines from {0}'.format(str(value))

                    if response == 'None':
                        response = "Sorry, i didn't understand!"

                    # ECHO
                    # response = messaging_text
                    bot.send_text_message(sender_id, response)
                    
    return "ok", 200

def log(message):
    print(message)
    sys.stdout.flush()

if __name__ == "__main__":
    app.run(debug = True, port = 80)