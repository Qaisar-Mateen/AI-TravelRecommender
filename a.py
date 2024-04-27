import requests

prompt = ''#input('Prompt: ')

keywords = ['europe', 'history', 'mountain', 'cold', 'skyscrapper', 'desert', 'beach',
 'asia', 'hot', 'food', 'culture', 'island', 'northamerica', 'southamerica',
 'africa', 'plain', 'wildlife', 'australia', 'forest']

response = requests.post('https://fumes-api.onrender.com/llama3',
 json={
 f'prompt': """{
   
 'systemPrompt': 'You have to analyse the user prompt and generate keywords for the following keywords that most accurately describes 
 users preferences for a travel destination. The keywords are: ['europe', 'history', 'mountain', 'cold', 'skyscrapper', 'desert', 'beach',
 'asia', 'hot', 'food', 'culture', 'island', 'northamerica', 'southamerica',
 'africa', 'plain', 'wildlife', 'australia', 'forest'].', 
 'Assistant': 'write the most relevant keywords for the kewords list provided, only reply with the keywords that are in my given list', 
 'user': 'i like a place with beautiful nature and culture and some food and i also like places with beaches and nice and warm weather and my budegt perday is 152',
 }""",
#  "temperature":0.75,
#  "topP":0.9,
 "maxTokens": 6000
}, stream=True)

for chunk in response.iter_content(chunk_size=1024):  
 if chunk:
      print(chunk.decode('utf-8'))