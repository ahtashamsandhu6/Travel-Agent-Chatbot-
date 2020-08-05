from wit import Wit

access_token = "E64TH2ZX2EXC6VN26ORIZRD6LQ3VHYA4"
client = Wit(access_token = access_token)

message_text = "i want to go to Paris"

resp = client.message(message_text)
print(resp)