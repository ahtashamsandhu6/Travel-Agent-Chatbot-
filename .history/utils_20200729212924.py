from wit import Wit
access_token = "E64TH2ZX2EXC6VN26ORIZRD6LQ3VHYA4"
client = Wit(access_token)
client.message('set an alarm tomorrow at 7am')

resp = client.message('what is the weather in London?')
# print('Yay, got Wit.ai response: ' + str(resp))


print(resp["intents"][0]["id"])