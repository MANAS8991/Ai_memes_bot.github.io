import requests

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
headers = {"Authorization": "Bearer YOUR_HF_API_KEY"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Example usage
if __name__ == "__main__":
    prompt = {
        "inputs": "Question: Create a funny and sassy meme text from the following description: 'A cat sitting on a couch looking unimpressed.' Answer: "
    }
    output = query(prompt)
    print(output[0]["generated_text"])
