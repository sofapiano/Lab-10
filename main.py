import pyttsx3, pyaudio, vosk
import requests
import json
from googletrans import Translator

def translate(text):
        translator = Translator()
        result = translator.translate(text, dest='ru')
        return result.text

class VoiceAssistant:
    def __init__(self, model_path = "vosk-model-small-ru-0.22"):
        self.tts_engine = pyttsx3.init()
        self.model = vosk.Model(model_path)
        self.recognizer = vosk.KaldiRecognizer(self.model, 16000)
        self.mic = pyaudio.PyAudio()
        self.stream = self.mic.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=8192
        )
        self.in_dialog = False

    def say(self, text):
        print(f"ассистент: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
    
    def listen(self):
        print("говорите...")
        self.stream.start_stream()

        while True:
            data = self.stream.read(4096)
            if self.recognizer.AcceptWaveform(data):
                result = json.loads(self.recognizer.Result())
                command = result.get("text", "")
                print(f"вы сказали: {command}")
                return command.lower()
            
    def get_fact(self):
        url = "http://numbersapi.com/random/math"
        response = requests.get(url).json()

        if response.get('cod') != 200:
            return "не удалось получить информацию о погоде"
        
        fact = response
        return translate(fact)
    
    def run(self):
        self.say('ассистент запущен и готов к работе')
        facts = []

        while True:
            command = self.listen()

            print(command)

            if "привет болтушка" in command:
                self.say("хоп-хей-лалалей, чем помочь?")
                self.in_dialog = True

            if self.in_dialog:
                if "факт" in command:
                    fact = self.get_fact()
                    facts.append(fact)
                    self.say(fact)

                elif "следующий" in command:
                    fact = self.get_fact()
                    facts.append(fact)

                elif "повтори" in command:
                    self.say(facts[-1])

                elif "удали" in command:
                    facts.pop()
                
                elif "пока" in command:
                    self.say("пока!")
                    break

                else:
                    self.say("соре, не понял команду. повтори плез")
    
    def __del__(self):
        self.stream.stop_stream()
        self.stream.close()
        self.mic.terminate()


if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.run()