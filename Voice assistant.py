import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia


# voice language options
id1 ="HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0"
id2 = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"

# hear the microphone and return audio as text
def transform_audio_into_text():

    #store recognizer in variable
    r = sr.Recognizer()

    # set microphone
    with sr.Microphone() as source:

        r.adjust_for_ambient_noise(source,duration=1)
        # waiting time
        r.pause_threshold = 0.5

        #report that recording has begun
        print("You can now speak")

        #save what you hear as audio
        audio = r.listen(source)


        try:
            # search on google
            request = r.recognize_google(audio,language="en-US")

            # test in text
            print("You said "+ request)

            #return request
            return request

        # In case it doesnot understand audio

        except sr.UnknownValueError :

            #show proof that didnot understand the audio
            print("I didnt understand the audio")

            #return error
            return "I am still waiting"

        # IN case request cannot be resolved

        except sr.RequestError :
            # show proof that didnot understand the audio
            print("oops !There is no service")

            # return error
            return "I am still waiting"

        # unexpected error

        except :
            # show proof that didnot understand the audio
            print("Something went wrong")

            # return error
            return "I am still waiting"

# function that assistant can be heard
def speak(message):

    #start engine ofpyttsx3
    engine = pyttsx3.init()
    engine.setProperty('voice',id2)

    #deliver message
    engine.say(message)
    engine.runAndWait()

# inform day of the week
def ask_day():

    #create a variable with todays information
    day = datetime.date.today()
    print(day)

    #create variable for day of week
    week_day = day.weekday()
    print(week_day)

    #names of day
    calendar = {0 :"Monaday",
                1 :"Tuesday",
                2 : "Wednesday",
                3 : "Thursday",
                4 : "Friday",
                5 : "Saturday",
                6 : "Sunday"
                }

    speak(f"Today is {calendar[week_day]}")

#inform the time
def ask_time():

    #variable with new information
    time = datetime.datetime.now()
    time = f"At this moment it is {time.hour} hour and {time.minute} minute"

    print(time)

    speak(time)

def initial_greeting():

    speak("Hello I am Hazel. How can I help you")

# main function of assistant
def my_assistant():

    #activate the initial greeting
    initial_greeting()

    #cut-off variable
    go_on = True

    #main loop
    while go_on :

        #activate the micropone and save request
        my_request = transform_audio_into_text().lower()

        if 'open youtube' in my_request:
            speak("Sure , I am opening Youtube")
            webbrowser.open('https://www.youtube.com')
            continue
        elif 'open browser' in my_request:
            speak("Of course, I am on it")
            webbrowser.open('https://www.google.com')
            continue

        elif 'what day is today' in my_request:
            ask_day()
            continue
        elif 'what time it is' in my_request:
            ask_time()
            continue
        elif 'do a wikipedia search for' in my_request:
            speak("I am looking for it")
            my_request = my_request.replace('do a wikipedia search for ', " ")
            answer = wikipedia.summary(my_request , sentences=1)
            speak("according to wikipedia:")
            speak(answer)
            continue
        elif 'search the internet for' in my_request:
            speak('of course! right now')
            my_request = my_request.replace('search the internet for', " ")
            pywhatkit.search(my_request)
            speak("this is what i found")
            continue
        elif 'play' in my_request:
            speak(" i will play it right now")
            pywhatkit.playonyt(my_request)
            continue
        elif 'joke ' in my_request:
            speak(pyjokes.get_joke())
            continue
        elif 'stock price' in my_request:
            share = my_request.split()[-2].strip()
            portfolio = {"apple" : 'APL',
                         'amazon' : 'AMAZ',
                         'google' : 'GOOGL'}
            try :
                searched_stock = portfolio[share]
                searched_stock = yf.Ticker(searched_stock)
                price = searched_stock.info['regularMarketPrice']
                speak(f'I found it! the price of {share} is {price}')
                continue
            except :
                speak("sorry , i could not find it")
                continue
        elif 'goodbye' in my_request :
            speak('I am going to rest.let me know if you need anything')
            break
my_assistant()
