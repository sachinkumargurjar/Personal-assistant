import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import phonenumbers
import os
from googlesearch import search
import pyaudio
import webbrowser
import ety
from PyDictionary import PyDictionary
import sys
from nltk.corpus import wordnet


listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_command():
    cmd = sr.Recognizer()
    with sr.Microphone() as source:
        cmd.adjust_for_ambient_noise(source)
        print('Hearing..')
        audio = cmd.listen(source)
        try:
            query = cmd.recognize_google(audio, language='en-in')
            print('User: ' + query + '\n')
        except sr.UnknownValueError:
            talk('Sorry could not get that. Could you please type that ?')
            query = str(input('Command: '))
    return query


def greeting():
    cH = int(datetime.datetime.now().hour)
    if cH >= 0 and cH < 12:
        talk('Good Morning')
    if cH >= 12 and cH < 17:
        talk('Good Afternoon')
    if cH >= 17 and cH < 24:
        talk('Good Evening')


def playMusic():
    song = command.replace('play', '')
    talk('playing' + song)
    pywhatkit.playonyt(song)


def whatsappmsg():
    talk('tell me the number on which you want to sent the msg')
    number = take_command()
    print(number)
    while not (len(number) == 12):
        talk('number is invalid tell the number again')
        number = take_command()
        print(number)
    talk('tell the msg that you want to send')
    msg = take_command()
    print(msg)
    talk('tell me the time at which you want to send')
    time = take_command()
    print(time)
    number1 = '+91'
    for i in range(len(number)):
        if not (number[i] == ' '):
            number1 += number[i]

    hour = ''
    minute = ''
    if time[2] == ':':
        hour += time[0:2]
        minute += time[3:5]
    elif time[1] == ':':
        hour += time[0:1]
        minute += time[2:4]
    hour = int(hour)
    minute = int(minute)
    if 'p.m.' in time:
        if hour <= 11:
            hour += 12
    pywhatkit.sendwhatmsg(number1, msg, hour, minute)


def find(name, path):
    for root, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


def searchOnGoogle(query, outputList):
    talk('The top 5 search results from Google are..')
    for output in search(query, tld="co.in", num=10, stop=5, pause=2):
        print(output)
        talk(output)
        outputList.append(output)
    return outputList


def openLink(outputList):
    talk("Here's the 1st link.")
    webbrowser.open(outputList[0])


def getCompleteInfo(word):
    dictionary = PyDictionary()
    mean = {}
    mean = dictionary.meaning(word)
    synonyms = []
    antonyms = []

    talk("Alright. Here is the information you asked for.")

    for key in mean.keys():
        talk("When " + str(word) + " is used as a " + str(key) + " then it has the following meanings")
        for val in mean[key]:
            print(val)
            talk(val)

    talk("The possible synonyms and antonyms of " + str(word) + " is.")
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            if l.name() not in synonyms:
                synonyms.append(l.name())
            if l.antonyms() and l.antonyms()[0].name() not in antonyms:
                antonyms.append(l.antonyms()[0].name())

    print("Synonyms: ", end=" ")
    print(' '.join(synonyms), end=" ")
    print("\n")
    print("Antonyms: ", end=" ")
    print(' '.join(antonyms), end=" ")
    print("\n")

    ori = ety.origins(word)
    if len(ori) > 0:
        talk("There are " + str(len(ori)) + " possible origins found.")
        for origin in ori:
            talk(origin)
    else:
        talk("I'm sorry. No data regarding the origin of " + str(word) + " was found.")


greeting()
talk('Alex here.')
talk('What would you like me to do for you ?')
if _name_ == '_main_':
    while True:
        command = take_command()

        if 'play' in command:
          playMusic()

        if 'time' in command:
          time = datetime.datetime.now().strftime('%I:%M %p')
          talk(time)

        if 'wikipedia' in command:
          person = command.replace('wikipedia', '')
          info = wikipedia.summary(person, 1)
          print(info)
          talk(info)

        if 'date' in command:
          talk('I am busy')

        if 'jokes' in command:
          talk(pyjokes.get_joke())
          print(pyjokes.get_joke())

        if 'send whatsapp message' in command:
          whatsappmsg()

        if 'find file' in command:
          talk('What is the name of the file that I should find ?')
          query = command()
          filename = query
          print(filename)
          talk('What would be the extension of the file ?')
          query = command()
          query = query.lower()
          extension = query
          print(extension)
          fullname = str(filename) + '.' + str(extension)
          print(fullname)
          path = r'D:\\'
          location = find(fullname, path)
          talk('the location is')
          talk(location)
          print(location)

        if 'search' in command:
           outputList = []
           talk('What should I search for ?')
           query = command()
           searchOnGoogle(query, outputList)
           talk('Should I open up the first link for you ?')
           query = command()
           if 'yes' in query or 'sure' in query:
               openLink(outputList)
           if 'no' in query:
               talk('Alright.')

        if 'open dictionary' in query or 'dictionary' in command:
           talk('What word should I look up for ?')
           word = command()
           getCompleteInfo(word)

        if 'that would be all' in command or 'that is it' in query or 'bye Alex' in command:
               talk('Alright. Have a nice day')
               sys.exit()

        else:
          talk('I can not understand repeat it again')
