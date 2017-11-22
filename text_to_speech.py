import pyaudio
import wave
from watson_developer_cloud import TextToSpeechV1


class TextToSpeech:
    def __init__(self, message):
        self.message = message
        self.get_voice()

    def get_voice(self):
        text_to_speech = TextToSpeechV1(
            username='<username>',
            password='<password>',
            x_watson_learning_opt_out=True)  # Optional flag

        with open("output.wav",
                  'wb') as audio_file:
            audio_file.write(
                text_to_speech.synthesize(self.message, accept='audio/wav',

                                          voice="en-US_AllisonVoice"))
        p = pyaudio.PyAudio()

        chunk = 1024

        audio_file = wave.open("output.wav", "rb")

        stream = p.open(format=p.get_format_from_width(audio_file.getsampwidth()),
                        channels=audio_file.getnchannels(),
                        rate=audio_file.getframerate(),
                        output=True)
        data = audio_file.readframes(chunk)

        # play stream
        while data:
            stream.write(data)
            data = audio_file.readframes(chunk)

        # stop stream
        stream.stop_stream()
        stream.close()

        # close PyAudio
        p.terminate()


