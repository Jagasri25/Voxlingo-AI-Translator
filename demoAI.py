"""
Note : Cant use Speak(audio) in this package
    Return the string we want to say aloud to demoApp.py then use speak(audio) by importing method.
    Speed Test Intallation = pip install speedtest-cli
        from speedtest import *
        stObj = SpeedTest()
        print(st.download(), st.upload())
    1. Add more songs in Static File and select random songs using random module
    2. use try except block
    3. implement Amazon, Youtube, Search Query 
"""

import datetime
from bs4.builder import HTML
from pyttsx3 import *
import speech_recognition as sr
import wikipedia
from bs4 import *
import webbrowser
import wolframalpha
import random
import requests
import json
import os

appId = "ad2706636ddfcf6579b8e07d682d9e68"
clientObj = wolframalpha.Client("QAY9L8-W7G3WGJ875")  # Wolframe API Key
e1 = Engine("sapi5")
e1.setProperty("voice", e1.getProperty("voices")[0].id)


def speak(audio):
    e1.say(audio)
    e1.runAndWait()


def greet(name):
    getTime = datetime.datetime.now().hour
    if getTime >= 0 and getTime < 12:
        return f"Good Morning {name}"

    elif getTime >= 12 and getTime < 18:
        return f"Good Afternoon {name}"

    else:
        return f"Good Evening {name}"


def takeCommand():  
    # It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.8  # default is 0.8
        r.energy_threshold = 200  # default is 300
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query}\n")

    except Exception:   #in any case of On Internet
        # print(e)
        print("Say that again please...")
        return "None"

    return query


def working(query):     #user input will be compare by each task

    if "time" in query:  # Test Status : Working
        strTime = datetime.datetime.now().strftime("%H hours & %M minute")
        # speak(f"the time is {strTime}")
        return f"Hey There the time is {strTime}"

    elif "date" in query:
        Year = datetime.datetime.now().date().year
        Month = datetime.datetime.now().date().month
        Date = datetime.datetime.now().date().day
        # speak(f"Today's Date is {Date} {Month} {Year}")
        return f"Today's Date is {Date} {Month} {Year}"

    elif "how are you" in query:
        # speak("I am Fine, How are you there")
        return "I am Fine, How are you there"

    elif "wikipedia" in query:  # Test Status : Working
        try:
            # speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "", 1)
            lis = BeautifulSoup(HTML, features="html.parser").find_all("li")
            results = wikipedia.summary(query, sentences=2)
            # speak("According to Wikipedia")
            # print(results)
            # speak(results)
            return f"According to Wikipedia. {results}"

        except wikipedia.wikipedia.WikipediaException as e:
            return f'The Term "{query}" may refer to one or more similar terms. Please Describe it more specifically.'

    elif "youtube" in query:       #test = 
        if "open youtube"in query:
            webbrowser.open("www.youtube.in")
            return f"Opening youtube please Hold a second"
        else:
            newQuery = query.replace("youtube", "")
            youtubeLink = "https://www.youtube.com/results?search_query="
            newUrl = youtubeLink+newQuery.replace(" ", "+").rstrip("+")
            webbrowser.open(newUrl)
            return f"Opening youtube with search query as {newQuery}"

    elif "open stack overflow" in query:
        webbrowser.open("www.stackoverflow.com")
        return f"Opening stack overflow please Hold a second"

    elif "amazon" in query:     #test = working
        if "open amazon"in query:
            webbrowser.open("www.amazon.in")
            return f"Opening amazon please Hold a second"
        else:
            newQuery = query.replace("amazon", "")
            amazonLink = "https://www.amazon.in/s?k="
            newUrl = amazonLink+newQuery.replace(" ", "+").rstrip("+")
            webbrowser.open(newUrl)
            return f"Opening Amazon with search query as {newQuery}"

    elif "open spotify" in query:   
        webbrowser.open("https://www.spotify.com/in-en/")
        return f"Opening Spotify please Hold a second"

    elif (query.split("for ")[0]) == "search " in query:  # query = Search for <keyword / s>
        keyWord = query.split("for ")[1]
        webbrowser.open("https://www.google.com/search?q=" + keyWord)
        return f"This what I found for {keyWord}"

    elif "play recorded audio" in query:
        music_dir = "" #recorded audios can be listened
        audio = os.listdir(music_dir)
        i = random.randint(0,7)
        os.startfile(os.path.join(music_dir, audio[i]))
        return f"Playing {audio[i]} audio"

    elif "weather" in query:  # test Status : Null
        baseUrl = "http://api.openweathermap.org/data/2.5/weather?"
        try:
            city = query.replace("weather", "")  # Nandurbar
            res = requests.get(baseUrl+"appid="+appId+"&q="+city)
            data = res.json()
            Celius = data["main"]["temp"] - 273.15
            windSpeed = data["wind"]["speed"]

            # rest = "weather of " + query
            # res = clientObj.query(rest)
            return f"Hey, The Current Temperature is {round(Celius, 2)}°C and Wind Speed is {windSpeed} miles per second"
        except Exception:
            return "Sorry, No Such City"

    elif "recall the remember task" in query:
        readFile = open(
            file=r"C:\Users\Jagasri_25\Documents\PROJECT CODE\Voxlingo AI Translator\Source Code\static",
            mode="r+",
        )
        reading = readFile.read()
        
        # check if file has content to read or not
        if readFile.tell() == 0:  
            print("No task To Remember")
            return "No task to remember"

        else:
            readFile.truncate(0)
            readFile.close()
            return "You said me to remember that" + reading

    elif "remember" in query: 
        save = query.replace("remember", "", 1)
        openFile = open(
            file=r"C:\Users\Jagasri_25\Documents\PROJECT CODE\Voxlingo AI Translator\Source Code\static",
            mode="a",
        )
        openFile.write(save + "\n")  # to save new text on new line
        openFile.close()
        return "Ok there, I will remember this"
    
    elif "History" in query: 
        save = query.replace("History", "", 1)
        openFile = open(
            file=r"C:\Users\Jagasri_25\Documents\PROJECT CODE\Voxlingo AI Translator\Source Code\static",
            mode="a",
        )
        openFile.write(save + "\n")  # to save new text on new line
        openFile.close()
        return "Hey there am read your history you are PEC IT student attending the meeting"
    
    elif "calculate" in query:
        res = clientObj.query(query)
        return f"Your answer is {next(res.results).get('subpod').get('plaintext')}"
    elif "explain about you" in query:
        return "As a fresher, I'm excited to introduce myself. My name is [Your Name], and I recently graduated from [Your University/College] with a degree in [Your Major]. I'm passionate about [mention your interests or field of study], and I'm eager to begin my professional journey in this field. During my academic years, I developed a strong foundation in [mention relevant skills or knowledge areas], and I'm enthusiastic about applying this knowledge in a real-world setting. I've also had the opportunity to work on several projects, including [briefly describe a relevant project or experience], which allowed me to gain practical experience and enhance my problem-solving abilities.I'm a highly motivated and quick learner, always eager to take on new challenges and expand my skills. I'm a team player and believe in effective communication and collaboration to achieve common goals. I'm also open to constructive feedback and constantly strive for self-improvement. I am genuinely excited about the opportunity to contribute and grow within a professional setting. I'm looking forward to being a part of a dynamic team where I can learn and contribute to the best of my abilities. Thank you for considering my application, and I'm eager to discuss how I can be a valuable addition to your organization."
    elif "Why are you interested in this role" in query:
        return "I am interested in this role because it aligns perfectly with my academic background and career goals. I've always been fascinated by [specific aspect of the role], and I believe that working here will provide me with the chance to learn and grow in a dynamic and innovative environment"
    elif "what is your strength" in query:
        return "As a fresher, I believe my strengths lie in my enthusiasm, adaptability, and my strong foundation in the skills I've gained through my academic journey"
    elif "what is your weakness" in query:
        return "As a fresher, I recognize that I have limited professional experience, and this could be considered a potential weakness. However, I view this as an opportunity for growth and improvement. I am eager to overcome this by seeking mentorship, being receptive to feedback, and continuously learning from experienced colleagues. Another area where I am working on improving is my public speaking and presentation skills. While I have gained knowledge in my field of study, I understand that effective communication is essential in any job. To address this, I have already started taking courses and workshops to enhance my presentation abilities, and I am committed to becoming a more confident and articulate communicator. Ultimately, I believe that weaknesses are areas for growth and development. I'm enthusiastic about building upon my skills and experiences as I embark on my professional journey, and I'm open to learning from every opportunity and challenge that comes my way."
    elif "What do you know about our company" in query:
        return "I have researched your company and found that you're known for [mention a key achievement or aspect]. I appreciate your commitment to [mention a company value or goal]. It's exciting to see how your innovative solutions have made a significant impact in the industry"
    elif "Why should we hire you" in query:
        return "You should hire me because I bring a combination of technical skills, a strong work ethic, and a passion for continuous learning. I'm enthusiastic about contributing to your team and helping [company name] achieve its goals."
    elif "What motivates you" in query:
        return "I am motivated by the opportunity to make a positive impact and solve real-world problems. I find fulfillment in using my skills to create innovative solutions and contribute to a better future"
    elif "Do you have any specific career goals in mind" in query:
        return "My short-term goal is to excel in this role and contribute to the success of the team. In the long term, I aspire to take on more leadership responsibilities and continue advancing in my career"
    elif "What is your preferred coding language or technology stack" in query:
        return "I'm proficient in [mention languages or technologies], but I'm adaptable and enjoy learning new ones. My choice depends on the project's requirements and goals"
    elif "Tell me about your favorite project or assignment during your studies" in query:
        return "My favorite project was [mention project] where I had the chance to [describe the project's scope and what you found particularly engaging]. It provided me with valuable insights and hands-on experience"
    
    else:
        return "Sorry I didn't get that \n I'm Still Learning New Stuff"



