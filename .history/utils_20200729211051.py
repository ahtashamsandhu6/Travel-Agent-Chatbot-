# access_token = "E64TH2ZX2EXC6VN26ORIZRD6LQ3VHYA4"
# client = Wit(access_token = access_token)

# message_text = "i want to go to Paris"

# resp = client.message(message_text)
# print(resp)
import requests

access_token = "E64TH2ZX2EXC6VN26ORIZRD6LQ3VHYA4"

ans = requests.get("https://api.wit.ai/message?v=20200729&access_token={{access_token}}&q=I%20want%20to%20go%20to%20turkey").json()
print(ans)

