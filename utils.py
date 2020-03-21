from wit import Wit

access_token = "E64TH2ZX2EXC6VN26ORIZRD6LQ3VHYA4"

client = Wit(access_token = access_token)
# message_text = "i want sport news "

def wit_response(message_text):
    response = client.message(message_text)
    entity = None
    value = None

    try:
        entity = List(resp['entities'])[0]
        value = resp['entities'][entity][0]['value']

    except:
        pass

    return (entity, value)

# print(response)