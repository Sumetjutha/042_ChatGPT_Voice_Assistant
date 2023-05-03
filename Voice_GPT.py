import openai
import pyttsx3
import speech_recognition as sr
from env import API_KEY

# Set your OpenAI API key
openai.api_key = API_KEY

# initialize the text-to-speech engine
engine = pyttsx3.init()

def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        print('Skipping unknown error')

def generate_response(prompt):
    response = openai.Completion.create(
        engine = "text-davinci-003",
        prompt = prompt,
        max_tokens = 4000,
        n = 1,
        stop = None,
        tempareture = 0.5
    )
    
def speak_text(text):
    engine.say(text)
    engine.runAndWait()
    
def main():
    while True:
        # wait for uset to say "John Tik"
        print("Hello 'John Tik' to start record your question...")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                if transcription.lower() == "john tik":
                    # Record audio
                    filename = "input.wav"
                    print("Say your question...")
                    with sr.Microphone() as source:
                        recognizer = sr.Recognizer()
                        source.pause_threshold = 1
                        audio = recognizer.listen(source, phrase_time_limit=None, timout=None)
                        with open(filename, "wb") as f:
                            f.write(audio.get_wav_data())
                            
                        # Transcript audio to text
                        text = transcribe_audio_to_text(filename)
                        if text:
                            print(f"You said: {text}")
                            
                            # Generate response using GPT
                            response = generate_response(text)
                            print(f"Chat GPT says: {response}")
                            
                            # Read response using text-to-speech
                            speak_text(response)
            except Exception as e:
                print("An error occured: {}".format(e))