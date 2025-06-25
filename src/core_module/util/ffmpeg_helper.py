import io

import ffmpeg


class FFmpegHelper:

    @staticmethod
    def convert_audio_to_wav_io(input_stream: io.BytesIO, target_sample_rate=16000) -> io.BytesIO:
        out, _ = (
            ffmpeg
            .input('pipe:0')
            .output('pipe:', format='wav', ac=1, ar=target_sample_rate, sample_fmt='s16')
            .run(input=input_stream.read(), capture_stdout=True, capture_stderr=True, quiet=True)
        )
        return io.BytesIO(out)