from .tts_interface import TTSInterface

import requests
import json





class NlsTTS_Adapter(TTSInterface):

    def  __init__(self , app_key, token, api_url):
        self.app_key = app_key
        self.token = token
        self.api_url = api_url
        pass

    def get_tts_wav(self, user_input):

        # 构造请求头
        headers = {
            "X-NLS-Token": self.token,
            "Content-Type": "application/json"
        }

         # 构造请求体
        payload = {
            "appkey": self.app_key,
            "text": user_input,
            "format": "wav",
            "sample_rate": 16000,
            "voice": "xiaoyun"
        }

        # 发送 POST 请求
        response = requests.post(self.api_url, headers=headers, data=json.dumps(payload))

        # 处理响应结果
        if response.status_code == 200:
            content_type = response.headers.get("Content-Type", "")
            if "audio" in content_type:  # 成功返回二进制音频数据
                with open("output_audio.wav", "wb") as audio_file:
                    audio_file.write(response.content)
                print("语音合成成功！音频文件已保存为 output_audio.wav")
                return response.content
            else:  # 返回 JSON 格式的错误信息
                result = response.json()
                print(f"语音合成失败！错误信息：{result.get('message')}")
        else:
            print(f"请求失败！HTTP状态码：{response.status_code}, 错误信息：{response.text}")