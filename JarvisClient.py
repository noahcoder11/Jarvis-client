import snowboydecoder
import speech_recognition as sr
import requests
import pyttsx3

class JarvisClient:

    def __init__(self, server):
        self.server = server
        self.recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)

        self.detector = snowboydecoder.HotwordDetector('./resources/models/jarvis.umdl', sensitivity=[0.8, 0.8], audio_gain=2)
        self.engine = pyttsx3.init()

    def main(self, callback):
        self.wait_for_hotword(callback)

    def run_cycle(self):
        self.detector.terminate()
        
        while True:
            message = self.run_speech_recognition()
            if len(message) == 0:
                return
            
            response = self.send_to_server(message)
            
            self.say(response.json()["text"])
            

    def wait_for_hotword(self, callback):
        self.detector.start(detected_callback=callback)
    
    def run_speech_recognition(self):
        with sr.Microphone() as source:
            audio = self.recognizer.listen(source)

            try:
                text = self.recognizer.recognize_google(audio)
                return text

            except:
                return ""
    
    def send_to_server(self, message):
        response = requests.post(self.server + "/query", data={
            "message": message
        })

        return response

    def say(self, text):    
        self.engine.say(text)
        self.engine.runAndWait()
