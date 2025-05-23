
from .asr_interface import ASRInterface
import requests
import ffmpeg
import io


def convert_audio_with_ffmpeg(input_path, target_sample_rate=16000):
    out, _ = (
        ffmpeg
        .input(input_path)
        .output("pipe:", format="wav", ac=1, ar=target_sample_rate, sample_fmt="s16")
        .run(capture_stdout=True, capture_stderr=True)
    )
    return io.BytesIO(out)


class NlsASR_Adapter(ASRInterface):

    def  __init__(self , app_key, token, api_url):
        self.app_key = app_key
        self.token = token
        self.api_url = api_url
        pass

    def transcribe_path(self, audio_file_path) -> str:

        converted_audio_io = convert_audio_with_ffmpeg(audio_file_path, 16000)

        params = {
            "appkey": self.app_key,
            "format":"wav",
            "sample_rate": 16000,
            "enable_punctuation_prediction": "true",
            "enable_inverse_text_normalization": "true",
        }

        headers = {
            "X-NLS-Token": self.token,
            "Content-Type": "application/octet-stream",
        }

        response = requests.post(self.api_url, headers=headers, params=params, data=converted_audio_io.read())

        if response.status_code == 200:
            result = response.json()
            print(result)
            if result.get("status") == 20000000:
                print(f"Recognition succeeded! Result: {result.get('result')}")
                return result.get('result')
            else:
                print(f"Recognition failed. Message: {result.get('message')}")
                return result.get('message')
        else:
            print(f"Request failed. HTTP status: {response.status_code}, Error: {response.text}")

        return "Failed"