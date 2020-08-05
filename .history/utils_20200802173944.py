from wit import Wit
access_token = "E64TH2ZX2EXC6VN26ORIZRD6LQ3VHYA4"
client = Wit(access_token)

resp = client.message('to lahore')

intent = resp["intents"][0]["name"]
entity = resp["entities"]["wit$location:location"][0]["name"]
value = resp["entities"]["wit$location:location"][0]["resolved"]["values"][0]["name"]

print(intent)
print(entity)
print(value)

############################################# Wit.ai Api Calling URL #################################################
"https://api.wit.ai/message?v=20200729&access_token=E64TH2ZX2EXC6VN26ORIZRD6LQ3VHYA4&q=I%20want%20to%20go%20to%20turkey"