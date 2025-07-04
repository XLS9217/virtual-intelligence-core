from openai import OpenAI
from .llm_interface import LLMInterface

class LLMAdapter_OpenAI(LLMInterface):
    
    def  __init__(self, api_key, base_url, model):
        #self.api_key = api_key
        self.model = model
        self.client = OpenAI(
            api_key = api_key, 
            base_url = base_url,
        )

    def get_response(self, user_input, system_prompt = "do short response in user's language") -> str:
        user_input = str(user_input)
        #print(user_input)
        response = self.client.chat.completions.create(
            model= self.model ,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input},
            ],
        )
        return response.choices[0].message.content
    
    def memory_response(self, message_list) -> str:
        response = self.client.chat.completions.create(
            model= self.model ,
            messages=message_list
        )
        return response.choices[0].message.content