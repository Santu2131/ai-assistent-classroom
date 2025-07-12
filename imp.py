import openai
import speech_recognition as sr
import pyttsx3
import webbrowser
import requests
import io
from PIL import Image

# ✅ Set your OpenAI API key
openai.api_key = "sk-...s-cA"  # Replace with your OpenAI API key


class LearningAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.tts = pyttsx3.init()
        self.tts.setProperty('rate', 150)

    def speak(self, text):
        print("Assistant:", text)
        self.tts.say(text)
        self.tts.runAndWait()

    def listen(self):
        with sr.Microphone() as source:
            print("🎤 Listening...")
            audio = self.recognizer.listen(source)
        try:
            query = self.recognizer.recognize_google(audio)
            print("You said:", query)
            return query
        except sr.UnknownValueError:
            self.speak("Sorry, I could not understand.")
            return None
        except sr.RequestError:
            self.speak("Network error.")
            return None

    def get_answer(self, query):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": query}]
        )
        return response.choices[0].message.content

    def generate_image(self, prompt):
        response = openai.Image.create(prompt=prompt, n=1, size="512x512")
        image_url = response['data'][0]['url']
        img_data = requests.get(image_url).content
        img = Image.open(io.BytesIO(img_data))
        img.show()

    def play_video(self, topic):
        search_query = topic.replace(" ", "+")
        url = f"https://www.youtube.com/results?search_query={search_query}"
        self.speak("Opening YouTube...")
        webbrowser.open(url)

    def handle_query(self, query):
        query = query.lower()
        if "show image of" in query:
            prompt = query.replace("show image of", "").strip()
            self.speak(f"Generating image of {prompt}")
            self.generate_image(prompt)

        elif "play video" in query:
            topic = query.replace("play video", "").strip()
            self.play_video(topic)

        else:
            answer = self.get_answer(query)
            self.speak(answer)

    def run(self):
        self.speak("AI Classroom Assistant is ready. Ask your questions.")
        while True:
            query = self.listen()
            if query:
                if "exit" in query.lower():
                    self.speak("Goodbye!")
                    break
                self.handle_query(query)


# Run the assistant
if __name__ == "__main__":
    assistant = LearningAssistant()
    assistant.run()
