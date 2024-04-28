import requests

prompt = 'i like a place with beautiful nature and culture and some food and i also like places with beaches and nice and warm weather and my budegt perday is 152'#input('Prompt: ')

# keywords = ['europe', 'history', 'mountain', 'cold', 'skyscrapper', 'desert', 'beach',
#  'asia', 'hot', 'food', 'culture', 'island', 'northamerica', 'southamerica',
#  'africa', 'plain', 'wildlife', 'australia', 'forest']

response = requests.post('https://fumes-api.onrender.com/llama3',
 json={
 f'prompt': """{
   
 'systemPrompt': 'You have to analyse the user prompt and generate keywords for the following keywords that most accurately describes 
 users preferences for a travel destination. The keywords are: ['europe', 'history', 'mountain', 'cold', 'skyscrapper', 'desert', 'beach',
 'asia', 'hot', 'food', 'culture', 'island', 'northamerica', 'southamerica',
 'africa', 'plain', 'wildlife', 'australia', 'forest'].', 
 'Assistant': 'keyword1,keyword2,keyword3... - budget per day(if given)', 
 'user': 'i like a place with beautiful nature and culture and some food and i also like places with beaches and nice and warm weather and my budegt for 2 days is 152',
 }""",
#  "temperature":0.75,
#  "topP":0.9,
 "maxTokens": 6000
}, stream=True)
# str = response.text
# print(str)
text = ''
for chunk in response.iter_content(chunk_size=1024):  
 if chunk:
      text += chunk.decode('utf-8')
print(text)
try:
    # Split the text on the colon to separate the keywords and budget from the rest of the text
    _, keywords_and_budget = text.split(':')
except ValueError:
    print("Error: The text does not contain a colon.")
    keywords_and_budget = ""

try:
    # Split the keywords and budget on the dash to separate the keywords from the budget
    keywords, budget = keywords_and_budget.split('-')
except ValueError:
    print("Error: The text does not contain a dash.")
    keywords = keywords_and_budget
    budget = ""

# Remove leading and trailing whitespace from the keywords and budget
keywords = keywords.strip()
budget = budget.strip()

print(keywords)

