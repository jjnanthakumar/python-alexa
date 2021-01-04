import cv2
import speech_recognition as sr
import pyttsx3
import datetime
import pywhatkit
import wikipedia
import pyjokes
import urllib.request, json
import re, os, subprocess
from functools import reduce
import random
from word2number import w2n
import time
import webbrowser
import rotatescreen
import requests
import psutil

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')

engine.setProperty('voice', voices[1].id)


def openweathermap(serviceurl, api_key='paste your api keys or u can give ur keys in a function call also',
                   place='Madurai'):
    # get your api key here https://home.openweathermap.org/ and paste in that function
    payload = {'q': place, 'appid': api_key}
    url = 'https://' + serviceurl + urllib.parse.urlencode(payload)
    d = urllib.request.urlopen(url).read().decode()
    js = json.loads(d)
    return [js['weather'][0]['description'], js['main']['temp'], js['main']['pressure'], js['wind']['speed']]


def talk(text=''):
    if not text:
        engine.say('Hey, I am your Alexa!')
        time.sleep(1)
        engine.say('What can I do for you?')
    else:
        engine.say(text)
    engine.runAndWait()


def take_command():
    try:
        with sr.Microphone() as source:
            print("listening..")
            listener.adjust_for_ambient_noise(source)
            voice = listener.listen(source, timeout=2)
            command = listener.recognize_google(voice).lower()
            if 'alexa' in command:
                command = command.replace('alexa', '').strip()
            else:
                pass
    except:
        talk('I can\'t recognize your voice')
    return command


def calculate(num, op):
    print(num)
    check = {
        1: reduce(lambda x, y: x + y, num),
        2: reduce(lambda x, y: x - y, num),
        3: reduce(lambda x, y: x * y, num),
        4: reduce(lambda x, y: x / y, num),
        5: reduce(lambda x, y: x % y, num),
        6: reduce(lambda x, y: pow(x, y, 10 ** 9 + 7), num)
    }
    return check.get(op)


def run_alexa():
    command = take_command()

    if 'multiply' in command:
        numbers = map(int, re.findall(r'[0-9]+', command))
        talk("The answer is " + str(calculate(list(numbers), 3)))
    elif any(i in command for i in ['add', 'sum', 'plus', '+']):
        numbers = map(int, re.findall(r'[0-9]+', command))
        talk("The answer is " + str(calculate(list(numbers), 1)))
    elif any(i in command for i in ['minus', 'sub', 'subtract', '-']):
        numbers = map(int, re.findall(r'[0-9]+', command))
        talk("The answer is " + str(calculate(list(numbers), 2)))
    elif any(i in command for i in ['divide', 'div']):
        numbers = map(int, re.findall(r'[0-9]+', command))
        talk("The answer is " + str(calculate(list(numbers), 4)))
    elif any(i in command for i in ['modulus', 'mod']):
        numbers = map(int, re.findall(r'[0-9]+', command))
        talk("The answer is " + str(calculate(list(numbers), 5)))
    elif any(i in command for i in ['power', 'pow']):
        numbers = map(int, re.findall(r'[0-9]+', command))
        talk("The answer is " + str(calculate(list(numbers), 6)))
    elif 'game' in command:
        talk('Ok! I will guess a number between 1 to 10, Just find it.')
        r = random.randint(1, 10)
        num = take_command()
        try:
            n = w2n.word_to_num(num)
            n = int(n)
            if n == r:
                talk("Hurray! You won the game")
            else:
                talk("I won! Thanks for playing!")
        except:
            talk("Only numbers allowed! Thanks for playing!")
    elif 'play' in command:
        song = command.replace('play', '')
        talk('playing ' + song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time1 = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + time1)
    elif 'date' in command:
        date = datetime.datetime.now().strftime('%d:%B:%Y')
        talk('Today is ' + date)
    elif any(i in command for i in ['search', 'find', 'who', 'get']):
        data = wikipedia.summary(command, 3)
        talk(data)
    elif 'joke' in command:
        talk(pyjokes.get_joke())
    elif 'send' in command:
        number = re.findall(r'[0-9 ]+', command)
        num = [i.replace(' ', '') for i in number if len(i) > 1][0]
        if len(num) != 10:
            talk("Please provide a valid number !")
            return
        datet = datetime.datetime.now()
        pywhatkit.sendwhatmsg('+91' + num, 'Hii', int(datet.strftime('%H')), int(datet.strftime('%M')) + 1)
    elif 'cancel shut' in command:
        pywhatkit.cancelShutdown()
        talk('System Shutdown Cancelled!')
    elif 'shutdown' in command:
        pywhatkit.shutdown(100)
        talk('System is going to shutdown!')
    elif bool(re.search(r'\.[a-zA-Z0-9]{2,3}', command)):
        url = command.replace('open', '').strip()
        print(url)
        webbrowser.open_new_tab(url if 'http' in url else 'https://' + url)
        talk('Opening ' + url + 'in chrome ')
    elif 'open' in command:
        app = command.replace('open', '').strip()
        app = ''.join(app.split())
        if 'computer' in app:
            subprocess.Popen(r'explorer /select,"C:\"' + app, shell=True)
            talk('Opening ' + app)
            return
        elif any(i in app for i in ['whatsapp', 'msteams', 'spotify']):
            subprocess.Popen(r'start ' + app + ':', shell=True)
            talk("Opening  " + app)
            return
        elif 'camera' in app:
            cam = cv2.VideoCapture(0)
            talk('Opening Camera! To capture image press spacebar once!')
            while cam.isOpened():
                ret, frame = cam.read()
                cv2.imshow('Camera', frame)
                k = cv2.waitKey(50)
                if k == 32:
                    r = random.randint(10, 10000)
                    cv2.imwrite(f'captured{r}.png', frame)
                    talk(f'Image captured and saved as captured{r} into current directory!')
                if cv2.getWindowProperty('Camera', cv2.WND_PROP_VISIBLE) < 1:
                    break
            cam.release()
            cv2.destroyAllWindows()
            return
        elif 'python' in app:
            n = os.startfile('python.exe')
            if n:
                talk('Sorry! I cant Open ' + app)
                return
            talk('Opening ' + app)
            return
        elif 'chrome' in command:
            webbrowser.open_new_tab('https://google.com')
            talk("Opening  " + app)
            return
        try:
            n = subprocess.Popen(app, stderr=subprocess.PIPE)
            talk("Opening  " + app)
        except:
            talk("Sorry I can't open " + app)
    elif 'close' in command:
        app = command.replace('close', '').strip()
        app = ''.join(app.split())
        # print(app)
        flag = 0
        for process in (process for process in psutil.process_iter() if app in process.name().lower()):
            process.kill()
            flag = 1
        if flag:
            talk('Closing ' + app)

    elif any(i in command for i in ['count', 'startcounter', 'starttimer']):
        num = re.findall(r'[0-9]+', command)
        num = sorted(map(int, num))
        if num:
            for i in range(num[0], num[1] + 1):
                talk(i)
                time.sleep(1)
        else:
            for i in range(1, 11):
                talk(i)
                time.sleep(1)
    elif any(i in command for i in ['goodnight', 'sweetdreams', 'night']):
        talk('Good night! Sweet dreams and takecare!')
        return 1
    elif any(i in command for i in ['goodmorning', 'morning']):
        talk('Morning! It’s good to see you!')
    elif bool(re.match(r'your.*?name', command)):
        talk('I am Nandyalexa, how may I help you?')
    elif 'single' in command:
        talk('I am already in relationship with nandy!')
    elif 'weather' in command:
        place = [i for i in re.split(r'weather|in ', command) if len(i) > 1 and i][-1]
        data = openweathermap('api.openweathermap.org/data/2.5/weather?', '79caf71712770c9af7b697ff4cd806e9', place)
        string = f'Current weather status in {place} is {data[0]}, Temperature in {place} is {data[1]}, Pressure in {place} is {data[2]}, and Wind Speed in {place} is {data[3]}'
        talk(string)
    elif 'where' in command:
        print(command)
        js = requests.get('https://freegeoip.app/json/').json()
        talk(
            f"Your Country is {js['country_name']}, Your Region is {js['region_name']}, Your city is {js['city']}, and Your Time zone is {js['time_zone']}")

    elif 'screen' in command:
        global degree
        screen = rotatescreen.get_primary_display()
        if any(i in command for i in ['default', '0', 'stop']):
            degree = 0
            screen.rotate_to(degree)
            talk('Screen set to normal!')
            return
        screen.rotate_to(degree % 360)
        talk('Screen rotated to ' + str(degree))
        degree += 90
    else:
        talk('Please say the command again ! ')


degree = 90
while True:
    try:
        n = run_alexa()
        if n == 1:
            break
    except:
        continue
