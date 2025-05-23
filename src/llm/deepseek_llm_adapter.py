from openai import OpenAI
from .llm_interface import LLMInterface

class DeepseekLLM_Adapter(LLMInterface):

    def  __init__(self, api_key):
        self.api_key = api_key
        self.client = OpenAI(api_key = self.api_key, base_url="https://api.deepseek.com")
        pass

    def get_response(self, user_input) -> str:
        user_input = str(user_input)
        #print(user_input)
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "用中文回答我"},
                {"role": "user", "content": user_input},
            ],
            stream=False
        )
        return response.choices[0].message.content