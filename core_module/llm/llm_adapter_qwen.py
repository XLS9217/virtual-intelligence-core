from openai import OpenAI
from .llm_interface import LLMInterface

class LLMAdapter_Qwen(LLMInterface):

    def  __init__(self, api_key):
        self.api_key = "sk-1258fc610e334f29b81724c11f012bb0"
        self.client = OpenAI(
            api_key = self.api_key, 
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )
        pass

    def get_response(self, user_input) -> str:
        user_input = str(user_input)
        #print(user_input)
        response = self.client.chat.completions.create(
            model="qwen-plus",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input},
            ],
        )
        return response.choices[0].message.content