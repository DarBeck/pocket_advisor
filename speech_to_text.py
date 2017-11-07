import asyncio
import websockets
import json
import requests
import pyaudio


class SpeechToText:
    def __init__(self):
        # Variables to use for recording audio
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 2
        self.RATE = 16000

        # Initialize auth_token
        self.auth_token = None

        self.transcript = "No audio was received"

        self.p = pyaudio.PyAudio()

        # Opens the stream to start recording from the default microphone
        self.stream = self.p.open(format=self.FORMAT,
                                  channels=self.CHANNELS,
                                  rate=self.RATE,
                                  input=True,
                                  output=True,
                                  frames_per_buffer=self.CHUNK)

        self.record_voice()

        # This is the language model to use to transcribe the audio
        self.model = "en-US_BroadbandModel"

        # These are the urls we will be using to communicate with Watson
        self.default_url = "https://stream.watsonplatform.net/speech-to-text/api"
        self.token_url = "https://stream.watsonplatform.net/authorization/api/v1/token?" \
                         "url=https://stream.watsonplatform.net/speech-to-text/api"
        self.url = "wss://stream.watsonplatform.net/speech-to-text/api/v1/recognize?model=en-US_BroadbandModel"

        # Params to use for Watson API
        self.params = {
            "word_confidence": True,
            "content_type": "audio/l16;rate=16000;channels=2",
            "action": "start",
            "interim_results": False
        }

    def record_voice(self):

        # Starts recording of microphone
        print("* READY *")

        frames = []

        for i in range(0, int(self.RATE / self.CHUNK * 5)):
            data = self.stream.read(self.CHUNK)
            frames.append(data)

        print("* FINISH *")

        # Stop the stream and terminate the recording
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

        self.audio_feed = b''.join(frames)

    def get_auth(self):

        # BlueMix app credentials
        username = "fd87dd64-847e-4e0b-b511-e22d07f898a4"
        password = "dPEw4c62KirQ"

        # Send a request to get an authorization key
        r = requests.get(self.token_url, auth=(username, password))
        self.auth_token = r.text
        self.token_header = {"X-Watson-Authorization-Token": self.auth_token}

        print("Authorization was requested")

    async def send_audio(self, audio, ws):
        if not audio:
            await ws.send(json.dumps({'action': 'stop'}))

        await ws.send(audio)
        await ws.send(json.dumps({'action': 'stop'}))

    async def speech_to_text(self, audio, auth_token):
        self.auth_token = auth_token
        self.token_header = {"X-Watson-Authorization-Token": self.auth_token}
        if self.auth_token is None:
            self.get_auth()
        async with websockets.connect(self.url, extra_headers=self.token_header) as conn:
            # Send request to watson and waits for the listening response
            send = await conn.send(json.dumps(self.params))
            rec = await conn.recv()
            print(rec)
            asyncio.ensure_future(self.send_audio(audio, conn))

            # Keeps receiving transcript until we have the final transcript
            while True:
                try:
                    rec = await conn.recv()
                    parsed = json.loads(rec)
                    self.transcript = parsed["results"][0]["alternatives"][0]["transcript"]
                    print(self.transcript)
                    # print(parsed)
                    if "results" in parsed:
                        if len(parsed["results"]) > 0:
                            if "final" in parsed["results"][0]:
                                if parsed["results"][0]["final"]:
                                    conn.close()
                                    return False
                                    pass
                except KeyError:
                    conn.close()
                    return False

    # Starts the application loop
    def run(self, auth_token):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.speech_to_text(self.audio_feed, auth_token))
        return self.transcript, self.auth_token


if __name__ == "__main__":
    app = SpeechToText()
    result = app.run()
    print(result)
