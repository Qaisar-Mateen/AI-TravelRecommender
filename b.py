import requests

prompt = 'i like a place with beautiful nature and culture and some food and i also like places with beaches and nice and warm weather and my budegt perday is 152'#input('Prompt: ')


def askAI():
    response = requests.post('https://fumes-api.onrender.com/llama3',
    json={
    'prompt': f"""{{
    'systemPrompt': 'You have to analyse the user prompt and suggest them countries based on their preferences. you only have to suggest them countries based on their preferences. You Have to Folloe
    a specific format to suggest them countries in all cases no exception. The format is: [country Name1, Country Name2, Country Name3...]',
    'user': '{prompt}',
    }}""",
      "temperature":0.2,
      "topP":0.3,
      "lengthPenality":0.3,
       "maxTokens": 2000
    }, stream=True)
      # str = response.text
      # print(str)
    text = ''
    for chunk in response.iter_content(chunk_size=1024):  
        if chunk:
            text += chunk.decode('utf-8')
    #print(text)
    return text

#while True:
#try:
text = askAI()

print('Llama3:\n', text)