import ffmpeg
from .tts_interface import TTSInterface

import requests
import json





class TTSAdapter_NLS(TTSInterface):

    def  __init__(self , app_key, token, api_url):
        self.app_key = app_key
        self.token = token
        self.api_url = api_url
        pass

    def get_tts_wav(self, user_input):

        # Construct request headers
        headers = {
            "X-NLS-Token": self.token,
            "Content-Type": "application/json"
        }

        # Construct request payload
        payload = {
            "appkey": self.app_key,
            "text": user_input,
            "format": "wav",
            "sample_rate": 16000,
            "voice": "xiaoyun"
        }

        # Send POST request
        response = requests.post(self.api_url, headers=headers, data=json.dumps(payload))

        # Process response
        if response.status_code == 200:
            content_type = response.headers.get("Content-Type", "")
            if "audio" in content_type:  # Successfully returned binary audio data

                raw_wav = response.content

                # Process raw WAV bytes in memory with FFmpeg
                converted_path = "output_audio.wav"
                (
                    ffmpeg
                    .input('pipe:0')
                    .output(
                            converted_path, 
                            format='wav', 
                            ac=1, 
                            ar=16000, 
                            sample_fmt='s16'
                        )
                    .run(input=raw_wav, overwrite_output=True)
                )

                print("Speech synthesis succeeded! Audio file saved as output_audio.wav")
                return converted_path
            else:  # Returned JSON error message
                result = response.json()
                print(f"Speech synthesis failed! Error message: {result.get('message')}")
        else:
            print(f"Request failed! HTTP status code: {response.status_code}, Error message: {response.text}")
