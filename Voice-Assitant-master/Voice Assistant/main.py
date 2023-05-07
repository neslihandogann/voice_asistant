import speech_recognition as sr # Recognize speech
import playsound   # Play an audio file
from gtts import gTTS # Google text to speech
import random 
import webbrowser

import os

class person:
    name = ""
    def setName(self, name):
        self.name = name

def there_exists(terms):
    for term in terms:
        if term in voice_data:
            return True

r = sr.Recognizer() # initialise a recognizer
# listen for audio and convert it to text
def record_audio(ask=False):
    with sr.Microphone() as source: # microphone as source
        if ask:
            speak(ask)
        audio = r.listen(source)
        voice_data = ""
        try:
            voice_data = r.recognize_google(audio) # Convert audio to text
        except sr.UnknownValueError: # error: recognizer does not understand
            speak("I did not get that")
        except sr.RequestError:
            speak("Sorry, the service is down") # error: recognizer is not connected
        print(f">> {voice_data.lower()}") # Print what the user said
        return voice_data.lower()     

# Get string and make an audio file to be played
def speak(audio_string):
    tts = gTTS(text=audio_string, lang="en") # text to speech(voice)
    r = random.randint(1,100)
    audio_file = "audio" + str(r) + ".mp3"
    tts.save(audio_file) # save as mp3
    playsound.playsound(audio_file) # play the audio file
    print(f"alexa: {audio_string}") # remove audio file

def respond(voice_data):
    # 1: greeting
    if there_exists(["hey", "hi", "hello"]):
        greetings = [f"hey, how can I help you {person_obj.name}",
        f"hey, what's up? {person_obj.name}", f"I'm listening {person_obj.name}"]
        greet = greetings[random.randint(0, len(greetings)-1)]
        speak(greet)  

    # 2: name
    if there_exists(["what is your name", "what's your name", "tell me your name"]):
        if person_obj.name:
            speak("my name is alexa")
        else:
            speak("my name is alexa. what's your name?")

    if there_exists(["my name is", "I am called"]):
        person_name = voice_data.split("is")[-1].strip()
        speak(f"okay, I will remember that{person_name}")
        person_obj.setName(person_name) # remember name in person object

    # 3: greeting
    if there_exists(["how are you", "how are you doing"]):
        speak(f"I'm very well, thanks for asking {person_obj.name}")
    
    # 4: search google
    if there_exists(["search for"]) and "youtube" not in voice_data:
        search_term = voice_data.split("for")[-1]
        url = f"https://google.com/search?q={search_term}"
        webbrowser.get().open(url)
        speak(f"Here is what I found for {search_term} on youtube")

    if there_exists(["exit", "quit", "goodbye"]):
        speak("going offline")
        exit()

person_obj = person()
while(1):
    voice_data = record_audio() # get the voice input
    respond(voice_data) # respond


