import requests
import re
from openai import OpenAI

prompt = 'i like a place with high skyscrappers and culture and some food and i also like places with beaches and nice and warm weather and my budegt perday is 152'


def askAI():
    response = requests.post('https://fumes-api.onrender.com/llama3',
    json={
    'prompt': f"""{{
    'systemPrompt': 'You have to analyse the user prompt and suggest them countries based on their preferences. you only have to suggest them countries based on their preferences. You Have to Folloe
    a specific format to suggest them countries in all cases no exception. The format is: [country Name1, Country Name2, Country Name3...]',
    'user': '{prompt}',
    }}""",
      "temperature":0.5,
      "topP":0.3,
      "lengthPenality":0.3,
       "maxTokens": 2000
    }, stream=True)
    text = ''
    for chunk in response.iter_content(chunk_size=1024):  
        if chunk:
            text += chunk.decode('utf-8')
    return text

def extract_data(text):
    matches = re.findall(r'\[([^]]*)\]', text)
    countries = [country.strip() for country in matches[0].split(',')]
    return countries
def ask():
        import pickle

        api_key =None

        with open('OpenAI_API.bin', 'rb') as f:
            api_key = pickle.load(f)

        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You have to analyse the user prompt and suggest them more than 5 countries based on their preferences. you only have to suggest them countries based on their preferences and write the standand Name for the countries. You Have to Follow a specific format to suggest them countries in all cases no exception. The format is: [country Name1, Country Name2, Country Name3, ...., country Name N]"},
            {"role": "user", "content": f"{prompt}"}
        ])
  
        text = response.choices[0].message.content
        print('\n GPT:\n', text)

        matches = re.findall(r'\[([^]]*)\]', text)
        if matches:
            countries = [country.strip() for country in matches[0].split(',')]
        else:
            countries = []

        print(countries)


text = ask()
#data = extract_data(text)
#print('Llama3:\n', text, '\nExtracted Data:\n', data)