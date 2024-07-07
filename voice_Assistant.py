import json
import subprocess
from urllib.request import urlopen
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os 
import smtplib
import pyjokes
import operator
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Initialize pyttsx3 engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speaker(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speaker("Good Morning!")
    elif 12 <= hour < 18:
        speaker("Good Afternoon!")
    else:
        speaker("Good Evening!")
    speaker("Hello I am Ruby. How may I help you?")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio)
        print(f"User said: {query}\n")
    except Exception as e:
        logging.error(f"Error: {e}")
        speaker("Sorry, I couldn't understand that. Can you please repeat?")
        return "None"
    return query 

def calculate(op1, oper, op2):
    return {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,  # Changed to truediv for floating point division
        '%': operator.mod,
        '^': operator.xor,
    }[oper](op1, op2)  # Fixed invocation of the operator function

def answer(op1, oper, op2):
    op1, op2 = int(op1), int(op2)
    return calculate(op1, oper, op2)

def sendMail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('youremail@gmail.com', 'your-password')
    server.sendmail('youremail@gmail.com', to, content)
    server.close()

def get_weather():
    try:
        response = urlopen('http://api.openweathermap.org/data/2.5/weather?q=London,uk&appid=YOUR_API_KEY')
        data = json.load(response)
        logging.info(f"Current weather in London: {data['weather'][0]['description']}")
        speaker(f"The current weather in London is {data['weather'][0]['description']}.")
    except Exception as e:
        logging.error(f"Error: {e}")
        speaker("Sorry, I couldn't get the weather information.")

def show_notes():
    try:
        with open('monju.txt', 'r') as file:
            notes = file.read()
            logging.info(f"Showing notes: {notes}")
            speaker(f"Here are your notes: {notes}")
    except FileNotFoundError:
        logging.info("No notes found.")
        speaker("Sorry, you don't have any notes.")

def main():
    wishMe()
    while True:
        query = takeCommand().lower()
        
        if 'wikipedia' in query:
            speaker('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            result = wikipedia.summary(query, sentences=2)
            speaker("According to Wikipedia")
            print(result)
            speaker(result)
            
        elif 'open youtube' in query:
            webbrowser.open("https://www.youtube.com")
            
        elif 'today news' in query:
            try:
                response = urlopen('https://newsapi.org/v1/articles?source=the-times-of-india&sortBy=top&apiKey=YOUR_API_KEY')
                data = json.load(response)
                logging.info(f"Showing top news from The Times of India.")
                speaker("Here are some top news from The Times of India.")
                for item in data['articles']:
                    print(f"{item['title']}\n")
                    speaker(f"{item['title']}\n")
            except Exception as e:
                logging.error(f"Error: {e}")
                speaker("Sorry, I couldn't get the news.")
                
        elif 'open google' in query:
            webbrowser.open("https://www.google.com")

        elif 'open maps' in query:
            webbrowser.open("https://www.google.com/maps")
        
        elif 'shutdown system' in query:
            speaker("Hold On a Sec Your system is on its way to shut down")
            subprocess.call('shutdown /p /f')
        
        elif 'joke' in query:
            speaker(pyjokes.get_joke())
            
        elif 'calculate' in query:
            speaker("Please provide the expression (e.g., 2 plus 3)")
            expression = takeCommand().split()
            if len(expression) != 3:
                speaker("Invalid expression. Please try again.")
            else:
                op1, oper, op2 = expression
                result = answer(op1, oper, op2)
                speaker(f"The result is {result}")
        
        elif "write notes" in query:
            speaker("What should I write for you?")
            note = takeCommand()
            with open('monju.txt', 'a') as file:
                file.write(note + '\n')
            speaker("Note written successfully.")
        
        elif "show note" in query:
            show_notes()
        
        elif 'current weather' in query:
            get_weather()
        
        elif 'what is the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speaker(f"The current time is {strTime}")
        
        elif 'exit' in query:
            speaker("Thank you for using Ruby. Have a great day!")
            exit()
        
        else:
            print("No query matched.")

if __name__ == "__main__":
    main()
