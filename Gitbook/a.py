from meta_ai_api import MetaAI

ai = MetaAI()
response = ai.prompt(message="Whats the weather in Ghaziabad, UP Today ? And what is the date?")
print(response)