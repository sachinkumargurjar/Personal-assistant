import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import phonenumbers

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()
def take_command():
 try:
    with sr.Microphone() as source:

        print ('listening..')
        voice = listener.listen(source)
        command = listener.recognize_google(voice)
        command = command.lower()
        if 'alexa' in command:
            command = command.replace('alexa' , '')
            print(command)


 except:
    pass
 return command

def run_alexa():
    command = take_command()
    if 'play' in command:
        song = command.replace('play', '')
        talk('playing' + song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk(time)
    elif 'wikipedia' in command:
        person = command.replace('wikipedia', '')
        info = wikipedia.summary(person, 1)
        print(info)
        talk(info)
    elif 'date' in command:
        talk('I am busy')
    elif 'jokes' in command:
        talk(pyjokes.get_joke())
        print(pyjokes.get_joke())
    elif 'send whatsapp message' in command:
        talk('tell me the number on which you want to sent the msg')
        number = take_command()
        print(number)
        while not(len(number) == 12):
            talk('number is invalid tell the number again')
            number = take_command()
            print (number)
        talk('tell the msg that you want to send')
        msg = take_command()
        print(msg)
        talk('tell me the time at which you want to send')
        time = take_command()
        print(time)
        number1='+91'
        for i in range(len(number)):
            if not (number[i] == ' '):
                number1+= number[i]

        hour =''
        minute =''
        if time[2]==':':
             hour+=time[0:2]
             minute+=time[3:5]
        elif time[1]==':':
            hour+=time[0:1]
            minute+=time[2:4]
        hour = int(hour)
        minute = int(minute)
        if 'p.m.' in time:
            if hour<=11:
              hour+=12
        pywhatkit.sendwhatmsg(number1, msg, hour,minute)

    else:
        talk('I can not understand repeat it again')

run_alexa()
