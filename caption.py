import requests

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
headers = {"Authorization": "Bearer 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"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
	
output = query({
	"inputs": "Question: which is the largest country in the world? Answer: ",
})
print(output[0]["generated_text"])