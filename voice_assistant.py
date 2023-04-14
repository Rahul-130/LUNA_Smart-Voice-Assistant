import tkinter as tk
from PIL import Image, ImageTk
import warnings
warnings.filterwarnings("ignore")
import pyttsx3 
import speech_recognition as sr 
import datetime
import wikipedia
import webbrowser
import os
import subprocess
import time
import keyboard
import pyautogui
import psutil
import pywhatkit
import random
from forex_python.converter import CurrencyRates
import speedtest
import uuid
import urllib.parse
from moviepy.editor import *    #pip install moviepy  -- for the video as a background

import functions as f    # imported functions.py file

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# <------------------------------------------- Speak function ---------------------------------->
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# <------------------------------------------ Wishme -------------------------------------------->
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")
    elif hour>=12 and hour<18:
        speak("Good Afternoon!")  
    else:
        speak("Good Evening!")  
    speak("hii, I am Luna, how may I help you")
    # query()

ok=0  
# <------------------------------------------ takeCommand --------------------------------------->
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        output("Listening...")
        speak("Listening...")

        audio = r.record(source,duration=5)
        # audio = r.listen(source)
    try:
        output("Recognizing...")    
        query = r.recognize_google(audio,language='en-in')
        # print(f"User said: {query}\n")
        output(f"User said: {query}\n")
        return query
        #ok=1
    except Exception as e:
        speak("Say that again please...")  
        return ""

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< OPERATIONS FUNCTIONS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# <-------------------------------  to stop scrolling  ----------------------------------->
def stop_scrolling():
    global scrolling
    scrolling = False
# output_label -- from main its function to print the content on GUI windoes  ------------------------------------>>>>>>>>>>>>>>>>>
def output(text):
    print(text)
    output_label.config(text=text)

# <---------------------------------------------- query --------------------------------------------------->
def query():
    # while True:
    command = ''
    command = takeCommand().lower()
    if query:
        # run_task(query)
        # the input should content the word wikipedia and about the content which u need to know ex: wikipedia about bill gates
        if 'wikipedia' in command:
            speak('Searching Wikipedia...')
            command = command.replace("wikipedia about", "")
            command = command.replace("wikipedia", "")
            result = wikipedia.summary(command, sentences=2)
            speak("According to Wikipedia")
            print(result)
            speak(result)

        

         # <--------------------------------     subprocess     ----------------------------------->
        elif 'open calculator' in command:
            subprocess.Popen('calc.exe')
            result = "Calculator has been opened"
            output_label.config(text="Calculator has been opened")
            speak(result)
        elif 'close calculator' in command:  #not working ----------------
            try:
                for proc in psutil.process_iter():
                    if proc.name() == "calc.exe":
                        proc.kill()
                        result = "Calculator closed successfully"
                        output(result)
                        speak(result)
                        return
                result = "Calculator is not currently running"
                output(result)
                speak(result)
            except psutil.NoSuchProcess:
                result = "Calculator is not currently running"
                output(result)
                speak(result)
        elif 'help' in command:
            filepathhelp = 'help_menu.txt'
            # subprocess.call(['notepad.exe', filepathhelp])
            os.startfile(filepathhelp)
            result = "help file is opend"
            speak(result)
            output(result)

 # <-------------------------------------------         functions   -------------------------------------------------------------->
        elif "get weather deatils" in command or "get weather" in command or "get temperature" in command or "what is the temperature" in command or "what is the weather" in command:
            city, country = f.get_location()
            weather = f.get_weather(city, country)
            print(city + " " + country)
            output(weather)
        

        elif command == "set reminder": 
            # f.reminder()
            speak("What should I remember?")
            Information=takeCommand()
            speak('you said me to remember that '+Information)
            rem = open('data.txt','w') 
            rem.write(Information) 
            rem.close() 
            output("Your remider has been saved")

        elif command == "show reminder":
            result = f.reminder_knowing()
            speak("You said me to remind"+result)
            output(result)
        elif 'change background' in command:
            f.change_desktop_background()
            result = "Background changed successfully"
            speak(result)
            output(result)

    # using import wmi win32con for brightness controls --------------------->
        elif "brightness up" in command or "increase brightness" in command:
            result = f.increase_brightness()
            speak(result)
            output(result)
        elif "brightness down" in command or "decrease brightness" in command:
            result = f.decrease_brightness()
            speak(result)
            output(result)

    # using pyautogui for volume--------------------->
        elif "increase volume" in command:
            result = f.increase_volume()
            speak(result)
            output(result)
        elif "decrease volume" in command:
            result = f.decrease_volume()
            speak(result)
            output(result)
    # ----------------------------------------------->

    # using pyjokes for joke ------------------------>
        elif "tell me a joke" in command or "tell a joke" in command or "make me laugh" in command:
            result = f.jokes()
            speak(result)
            output(result)

    # using webbrowser for google search or search and for opening website
        elif 'search' in command or 'google search' in command:    #error as output_label is not defined
            # result = f.GoogleSearch()
            speak("What should I search?")
            SearchData=takeCommand()
            SearchDataInput = urllib.parse.quote(SearchData)
            webbrowser.open_new_tab("https://www.google.com/search?q=" + SearchDataInput)
            result = "opened your search result"
            speak(result)
            output(result)
        
        # # the input should content the word as open website website_name which u need to search ex: open website gmail
        # limatstion with only .com extension websites
        elif 'open website' in command:
            f.openWebsite(command)
            result = "ur requested site is opended"
            speak(result)
            output(result)
    # using urllib.request   bs4   webbrowser   for getting news
        elif 'news' in command or 'news headlines' in command:
            f.news()
    # using library         from forex_python.converter import CurrencyRates  for coverting currency
        elif 'convert currency' in command:
            result = f.currencyConvert()
            speak(result)
            output(result)
    # error in convert currency

    # calculate num () num  ("multiply": "*", "multiplied by": "*", "times": "*", "plus": "+", "minus": "-", "divided by": "/", "to the power of": "**", "^": "**", "mod": "%", "remainder": "%")
        elif 'calculate' in command:
            expression = f.replace_words(command, f.word_dict).replace("calculate", "")
            result = f.calculate(expression)
            speak(f"The result of {expression} is {result}")
            output(f"The result of {expression} is {result}")
        

# <---------------------------------------    webbrowser     -------------------------------------->
        elif 'open youtube' in command:
            result = "Searching youtube ..."
            speak(result)
            webbrowser.open("youtube.com")
            output(result)
        elif command == 'open google':
            result = "Searching google ..."
            speak(result)
            webbrowser.open("google.com")
            output(result)
        elif 'open firefox' in command:
            result = "Searching firefox ..."
            speak(result)
            webbrowser.open("firefox.com")
            output(result)
        elif 'open zoom' in command:
            result = "opening zoom"
            speak(result)
            webbrowser.open("zoom.com")
            output(result)
        elif 'open facebook' in command:
            result = "opening facebook"
            speak(result)
            webbrowser.open("facebook.com")
            output(result)
        elif ('open instagram' in command) or ('open insta' in command):
            result = "opening Instagram"
            speak(result)
            webbrowser.open("instagram.com")
            output(result)
        elif command == "open whatsapp web" or command == "open whatsapp":
            result = "opening whatsapp web"
            speak(result)
            webbrowser.open("web.whatsapp.com")
            output(result)
        elif command=="open spotify":
            result = "opening spotify"
            speak(result)
            webbrowser.open("open.spotify.com")
            output(result)
        elif "open coursera" in command:
            result = "Opening Coursera..."
            speak(result)
            webbrowser.open("https://www.coursera.org/")
            output(result)
        elif "open linkedin" in command:
            result = "Opening LinkedIn..."
            speak(result)
            webbrowser.open("https://www.linkedin.com/")
            output(result)
        elif "open gmail" in command:
            result = "Opening Gmail..."
            speak(result)
            webbrowser.open("https://mail.google.com/")
            output(result)
        elif "open yahoo" in command:
            result = "Opening Yahoo..."
            speak(result)
            webbrowser.open("https://www.yahoo.com/")
            output(result)
        elif "open zomato" in command:
            result = "Opening Zomato..."
            speak(result)
            webbrowser.open("https://www.zomato.com/")
            output(result)
        elif "open swiggy" in command:
            result = "Opening Swiggy..."
            speak(result)
            webbrowser.open("https://www.swiggy.com/")
            output(result)
        elif "open bookmyshow" in command:
            result = "Opening BookMyShow..."
            speak(result)
            webbrowser.open("https://in.bookmyshow.com/")
            output(result)
        elif "open google meet" in command:
            result = "Opening Google Meet..."
            speak(result)
            webbrowser.open("https://meet.google.com/")
            output(result)
        elif "open teams" in command:
            result = "Opening Microsoft Teams..."
            speak(result)
            webbrowser.open("https://www.microsoft.com/en-in/microsoft-teams/group-chat-software")
            output(result)
        elif "open quora" in command:
            result = "Opening Quora..."
            speak(result)
            webbrowser.open("https://www.quora.com/")
            output(result)
        elif "open brainly" in command:
            result = "Opening Brainly..."
            speak(result)
            webbrowser.open("https://brainly.com/")
            output(result)
        elif "open stack overflow" in command:
            result = "Opening Stack Overflow..."
            speak(result)
            webbrowser.open("https://stackoverflow.com/")
            output(result)
        elif "open github" in command or "open git hub" in command:
            result = "Opening GitHub..."
            speak(result)
            webbrowser.open("https://github.com/")
            output(result)
        elif "open colab" in command or "open google colab" in command or "open collab" in command or "open google collab" in command: #-------------- not working as its taking colab as collab so added the spelling of collab in the command
            result = "Opening Google Colab..."
            speak(result)
            webbrowser.open("https://colab.research.google.com/")
            output(result)
        elif "open vnr website" in command or "open vnr" in command:
            result = "Opening VNRVJIET collage website..."
            speak(result)
            webbrowser.open("http://www.vnrvjiet.ac.in/")
            output(result)
        elif "open eduprime" in command or "open edu prime" in command or "open ediprime" in command or "open edi prime" in command:     #---------- not working as its taking eduprime as edi prime so added the spelling of edi prime in the command
            result = "Opening eduprime VNRVJIET collage website..."
            speak(result)
            webbrowser.open("https://automation.vnrvjiet.ac.in/eduprime3")
            output(result)
# gmail,yahoo,zomato,swiggy,bookmyshow, google meet, teams, quora, brainly, stack overflow, github, colab, vnr, eduprime
# <---------------------------------------  date & time ---------------------------------------->
        elif command == 'time' or command == "what's the time":
            strTime=datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"the time is {strTime}")
            output(f"the time is {strTime}")
        elif command == 'date' or command== "what's the date":
            strDate=datetime.date.today()
            speak(f"Todays date is {strDate}")
            output(f"Todays date is {strDate}")

# <--------------------------------  set an alarm for & set a timer for  ------------------------->
        # set an alarm for time+(am or pm) eg: set an alarm for 3:05 pm  (limitation: until the alarm rings u cant perform any other task)
        elif "set an alarm for" in command or "set alarm for" in command:
            index = command.index("set an alarm for") + len("set an alarm for")
            t = command[index:]
            t = t.strip()
            t = t.replace(".", "")
            t = t.replace(" ", "")
            time_obj = datetime.datetime.strptime(t, '%I:%M%p')
            speak("OK, I've set an alarm for " + time_obj.strftime("%I:%M %p"))
            while True:
                now = datetime.datetime.now().strftime('%I:%M %p')
                if now == time_obj.strftime('%I:%M %p'):
                    for i in range(10):
                        speak("Wake up!")
                    break

        # set a timer for (time) minutes eg:set a timer for 10 minutes  (limitation: until the timer complete u cant perform any other task)
        # elif "set a timer for" in command or "set timer for" in command:
        #     index = command.index("set a timer for") + len("set a timer for")
        #     time = command[index:]
        #     time = time.strip()
        #     time = time.replace(".", "")
        #     time = time.replace(" ", "")
        #     time = time.replace("minutes", "")
        #     time = int(time)
        #     speak("Sure, I've set a timer for " + str(time) + " minutes.")
        #     time = time * 60
        #     while time > 0:
        #         time -= 1
        #         time_left = str(time // 60) + " minutes " + str(time % 60) + " seconds"
        #         print(time_left)
        #         time.sleep(1)
        #         if time == 0:
        #             speak("Time's up!")
        #             break



# <---------------------------------------     os      ----------------------------------------->
    # <---------------------- MS Offlice open and close  -------------------------------------->
        elif 'open powerpoint' in command:
            os.system("start powerpnt")
            result = "Microsoft PowerPoint opened successfully"
            speak(result)
            output(result)
        elif 'open word' in command:
            os.system("start winword")
            result = "Microsoft Word opened successfully" 
            speak(result)
            output(result)
        elif 'open excel' in command:
            os.system("start excel")
            result = "Microsoft Excel opened successfully"
            speak(result)
            output(result)
        elif 'open outlook' in command:
            os.system("start outlook")
            result = "Microsoft Outlook opened successfully"
            speak(result)
            output(result)
        elif 'close word' in command:
            for proc in psutil.process_iter():
                if proc.name() == "WINWORD.EXE":
                    proc.kill()
                    result = "Microsoft Word closed successfully"
                    speak(result)
                    output(result)
                    break
            else:
                result = "Microsoft Word is not currently running"
                speak(result)
                output(result)
        elif 'close excel' in command:
            for proc in psutil.process_iter():
                if proc.name() == "EXCEL.EXE":
                    proc.kill()
                    result = "Microsoft Excel closed successfully"
                    speak(result)
                    output(result)
                    break
            else:
                result = "Microsoft Excel is not currently running"
                speak(result)
                output(result)
        elif 'close powerpoint' in command:
            for proc in psutil.process_iter():
                if proc.name() == "POWERPNT.EXE":
                    proc.kill()
                    result = "Microsoft powerpoint closed successfully"
                    speak(result)
                    output(result)
                    break
            else:
                result = "Microsoft powerpoint is not currently running"
                speak(result)
                output(result)
        elif 'close outlook' in command:
            for proc in psutil.process_iter():
                if proc.name() == "OUTLOOK.EXE":
                    proc.kill()
                    result = "Microsoft outlook closed successfully"
                    speak(result)
                    output(result)
                    break
            else:
                result = "Microsoft outlook is not currently running"
                speak(result)
                output(result)
    # <--------------------------------------------------------------------------------------->

        elif 'open notepad' in command:
            os.startfile("notepad.exe")
            result = "Notepad opened successfully"
            speak(result)
            output(result)

        elif "close notepad" in command:        #trouble in closing notepad have to make command 2times then its closing
            for i in range(0,2):
                notepad_found = False
                for proc in psutil.process_iter():
                    try:
                        proc_name = proc.name().lower()
                        if "notepad" in proc_name:
                            notepad_found = True
                            proc.kill()
                            result = "Notepad closed successfully"
                            # speak(result)
                            # output(result)
                            break
                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        pass
                if notepad_found == False:
                    result = "Notepad is not currently running"
            speak(result)
            output(result)

        elif 'open camera' in command:
            os.system("start microsoft.windows.camera:")
            result = "camera opened"
            speak(result)
            output(result)
        elif "close camera" in command:
            os.system("taskkill /f /im WindowsCamera.exe") # Close the camera app forcefully
            result = "camera closed"
            speak(result)
            output(result)
        


        # elif command and "open file" in command:
        #     filename = command.split("open file ")[1]
        #     found_file = False
        #     for root, dirs, files in os.walk("C:\\"):
        #         if filename in files:
        #             filepath = os.path.join(root, filename)
        #             os.startfile(filepath)
        #             print(f"{filename} opened successfully.")
        #             speak(f"{filename} opened successfully.")
        #             found_file = True
        #             break
        #     if not found_file:
        #         for root, dirs, files in os.walk("D:\\"):
        #             if filename in files:
        #                 filepath = os.path.join(root, filename)
        #                 os.startfile(filepath)
        #                 print(f"{filename} opened successfully.")
        #                 speak(f"{filename} opened successfully.")
        #                 found_file = True
        #                 break
        #     if not found_file:
        #         print(f"Could not find {filename} on any drive.")
        #         speak(f"Could not find {filename} on any drive.")
            

        # open file file_name or folder_name
        elif "open file" in command:
            filename = command.split("open file ")[1]
            filepath = os.path.join(os.getcwd(), filename)
            os.startfile(filepath)
            speak(f"{filename} opened successfully.")
            output(f"{filename} opened successfully.")
            

        elif command == "open visual studio code" or command == "open VS code" or command == "open visual code":
            os.system('code')
            result = "open visual studio code"
            speak(result)
            output(result)
        elif command == "close visual studio code" or command == "close VS code" or command == "close visual code":
            os.system('taskkill /IM code.exe /F')
            result = "close visual studio code"
            speak(result)
            output(result)


# <---------------------------------------     keyboard    ------------------------------------------>
        elif "page up" in command:
            keyboard.press_and_release("pageup")
            output("pageup")
        elif "page down" in command:
            keyboard.press_and_release("pagedown")
            output("pagedown")

        elif "minimize" in command or "minimise" in command:
            keyboard.press_and_release("win+m")
            output("minimize")
        elif "maximize" in command or "maximize" in command:
            keyboard.press_and_release("win+shift+m")
            output("maximize")
        
        elif command == "lock system" or command == "lock user" or command == "lock my system" or command=="lock my laptop":
            keyboard.press_and_release('win+l')
            speak("user locked")
            output("user locked")
        
        elif command == "open my computer" or command == "open explorer":
            keyboard.press_and_release('win+e')
            speak("File Explorer opened")
            output("File Explorer opened")

        elif command == "speech to text" or command== "write" or command=="write the content":
            keyboard.press_and_release('win+h')
            result = "speech to text or wite operation performed"
            speak(result)
            output(result)

        elif command == "open settings" or command == "open setting":
            keyboard.press_and_release('win+i')
            speak("opened settings")
            output("opened settings")
# 
        elif command == "open snipping tool":
            keyboard.press_and_release('win+shift+s')
            output("snipping Tool opened")
            speak("snipping Tool opened")
                # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<     basic operations       >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        elif command == "save":
            keyboard.press_and_release('ctrl+s')
            output("save operation performed")
        elif command == "copy":
            keyboard.press_and_release('ctrl+c')
            output("copy operation performed")
        elif command == "paste":
            keyboard.press_and_release('ctrl+v')
            output("paste operation performed")
        elif command == "cut":          #----------------------
            keyboard.press_and_release('ctrl+x')
            output("cut operation performed")
        elif command == "undo":
            keyboard.press_and_release('ctrl+z')
            output("undo operation performed")
        elif command == "redo":
            keyboard.press_and_release('ctrl+y')
            output("redo operation performed")
        elif command == "print":
            keyboard.press_and_release('ctrl+p')
            output("print")
        elif command == "home" or command == "beginning":
            keyboard.press_and_release("home")
            output("home")
        elif command == "end" or command == "end of page" or command == "end of the page":
            keyboard.press_and_release("end")
            output("end")
        elif command == "select all":
            keyboard.press_and_release('ctrl+a')
            output("select all")
        elif command == "close tab":
            keyboard.press_and_release('ctrl+w')
            speak("current tab closed")
            output("current tab closed")
        elif command == "open a new tab" or command=="open new tab":
            speak("opening new tab")
            output("opening new tab")
            keyboard.press_and_release('ctrl+t')
        elif command == "file menu":
            speak("opening file menu")
            output("opening file menu")
            keyboard.press_and_release('alt+f')


        # <--------------------------------------       pyautogui    ----------------------------------------->
        # elif command == 'resume' or 'pause':
        #     pyautogui.press("playpause")
        #     speak("pause or resume")
        # elif command == 'previous':
        #     pyautogui.press("prevtrack")

        # elif command == 'next':
        #     pyautogui.press("nexttrack")
        
        # Scroll up and scroll down----------------------------------> 
        elif 'scroll up' in command:
            result = "scroll up please press esc to stop scrolling"
            speak(result)
            output(result)
            scrolling = True
            # Press the 'esc' key to start scrolling up
            # pyautogui.press('esc')
            while scrolling:
                if keyboard.is_pressed('esc'):
                    scrolling = False
                else:
                    pyautogui.scroll(80)
                    time.sleep(0.1)

        elif 'scroll down' in command:
            result = "scroll down please press esc to stop to stop scrolling"
            speak(result)
            output(result)
            scrolling = True
            # Press the 'esc' key to start scrolling up
            # pyautogui.press('esc')
            while scrolling:
                if keyboard.is_pressed('esc'):
                    scrolling = False
                else:
                    pyautogui.scroll(-80)
                    time.sleep(0.1)
        # -------------------------------------------------------------->
        # play songs/video in youtube  --  using pywhatkit
        elif 'play' in command:
            song = command.replace('play', '')
            speak('playing' +song)
            pywhatkit.playonyt(song)

        # to open any application --- easy method
        elif "open" in command:
            command = command.replace("open", "")
            pyautogui.press("super")
            pyautogui.typewrite(command)
            pyautogui.sleep(1)
            pyautogui.press("enter")

        # to know internet speed   --  pip install speedtest
        elif "internet speed" in command:
            wifi = speedtest.Speedtest()
            upload_internet_speed = wifi.upload()/1048576    #Megabyte = 1024*1024 Bytes
            download_internet_speed = wifi.download()/1048576
            upload_speed = round(upload_internet_speed, 2)
            download_speed = round(download_internet_speed, 2)
            print("Upload speed: ", upload_speed, "Download speed :", download_speed)
            speak("Upload speed: " + str(upload_speed) + " megabytes per second. Download speed: " + str(download_speed) + " megabytes per second.")

        # to take screenshot  -- pyautogui for taking screenshot and import uuid for saving the filename with timestamp
        elif "screenshot" in command:
            im = pyautogui.screenshot()
            now = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
            # filepath = "screenshots"
            filename = f"screenshots\ss_{now}_{str(uuid.uuid4())[:8]}.jpg"
            im.save(filename)
            speak("Screenshot taken and saved")



        elif command == 'email' or command == 'mail' or command == 'send email' or 'send mail' in command:
            try:
                speak("opening the send Email window Enter the details for the message input choose according to ur option")
                f.email()
                output("Email operation completed")
            except Exception as e:
                print(e)
                speak("Sorry sir, Im not able to send this mail.")
        
        # <--------------------------------------- normal convo ----------------------->
        elif 'hey' in command or 'hello' in command:
            hey = random.choice(["Hi! How can I help you out?",
                                 "Hello! It's great to chat with you. What can I do for you?",
                                 "Hey, how's it going? Is there anything you need assistance with?",
                                 "Hey! Thanks for reaching out. How can I support you today?"])
            output(hey)
            speak(hey)
        
        elif 'what are you doing' in command:
            what_r_u_dng = random.choice(["I'm always learning and improving my capabilities. What can I help you with today?",
                                          "I'm processing and analyzing data to help you get the information you need. What do you want to know?",
                                          "I'm here to assist you in any way I can. How can I help you today?",
                                          "I'm just waiting for your next command. What can I do for you right now?",
                                          "I'm constantly searching for ways to make your life easier. What can I help you with?"])
            output(what_r_u_dng)
            speak(what_r_u_dng)

        elif command == 'how are you':
            how_are_u = random.choice(["I'm just a machine, so I don't have feelings in the way humans do. But I'm always here to help you out and make your life easier.",
                                       "I'm here and ready to assist you in any way I can. What can I do for you today?",
                                       "As an AI language model, I don't have emotions like humans do. But I'm always working to improve my responses and provide better assistance to users like you.",
                                       "I'm always available and ready to help you out. Is there something specific you need help with today?",
                                       "I'm just a voice assistant, but I'm always here to assist you with whatever you need. How can I help you out right now?"])
            output(how_are_u)
            speak(how_are_u)

        elif command ==  'who are you':
            who_are_u = "I am Luna, Your Personal Assistant"
            output(who_are_u)
            speak(who_are_u)

        elif command == "who created you" or command == "who developed you":
            who_created = "Rahul from Team 15"
            output(who_created)
            speak(who_created)


            

        else:
                answer = f.get_answer(command)
                if answer:
                    output(answer)
                    speak(answer)
                else:
                    speak("Command not recognized")
        #     # if command == "None" or command == "none":
        #     #     speak("no operation performed")
                
        #     # else:
        #         speak("searching in google")
        #         url = "https://www.google.com/search?q=" + command
        #         webbrowser.open_new_tab(url)

# <=========================================== Function for the GUI window  ==============================================================>
# Update the time label every second
def update_time():
    current_time = datetime.datetime.now().strftime("%A %d-%m-%Y  %H:%M:%S")
    time_label.config(text=current_time)
    window.after(1000, update_time)

# function to stop/close the running program
def stop_assistant():
    window.destroy()
# <===========================================      main        ===================================================================>
if __name__ == "__main__":
    # wishMe()
    # Create the main window
    window = tk.Tk()
    window.geometry("800x600")
    window.title("LUNA -Voice Assistant")

    # set logo for window
    window.iconbitmap("animations\\va-icon.ico")


    # Set the background video for the GUI
    clip = VideoFileClip("animations\\bg.mp4")
    clip_resized = clip.resize((800, 600))
    clip_duration = clip.duration
    clip_fps = clip.fps
    # Define a function to update the tkinter window with the current frame of the video clip
    def update_frame(time):
        frame = clip_resized.get_frame(time)
        frame_image = Image.fromarray(frame)
        frame_photo = ImageTk.PhotoImage(frame_image)
        canvas.itemconfig(canvas_image, image=frame_photo)
        canvas.image = frame_photo
        window.after(int(1000/clip_fps), update_frame, (time + 1/clip_fps) % clip_duration)

    # Create a canvas widget to hold the video clip
    canvas = tk.Canvas(window, width=800, height=600)
    canvas.place(x=0, y=0)
    canvas_image = canvas.create_image(0, 0, anchor=tk.NW)
    # Start updating the video frames
    update_frame(0)
    

    # Set the background image for the GUI
    # bg_image = Image.open("animations\\luna_background.png")
    # bg_image = bg_image.resize((800, 600))
    # bg_image = ImageTk.PhotoImage(bg_image)
    # canvas = tk.Canvas(window, width=800, height=600)
    # canvas.create_image(0, 0, anchor=tk.NW, image=bg_image)
    # canvas.place(x=0, y=0)

    # Create a label widget to display the output
    output_label = tk.Label(window, text="", font=("Arial", 16), bg="#10212b", fg="#aaadb5", wraplength=350)
    output_label.place(relx=0.77, rely=0.07, anchor="n")

    # Create the microphone button
    # mic_img = Image.open("animations\luna.png")
    # mic_img = mic_img.resize((70, 50))
    # mic_img = ImageTk.PhotoImage(mic_img)
    mic_button = tk.Button(window, text="Start", font=("Arial", 12), command=query, bg="#143341", fg="white")
    mic_button.place(relx=0.82, rely=0.95, anchor="se")

    # Add a hotkey to activate the microphone button
    keyboard.add_hotkey("ctrl+1", lambda: mic_button.invoke())

    # Create a label widget to display the current time
    time_label = tk.Label(window, font=("Arial", 12), bg="#0f202a", fg="white")
    time_label.place(relx=0.98, rely=0.02, anchor="ne")

    # Start updating the time label
    update_time()

    # Create a stop button
    stop_button = tk.Button(window, text="Stop", font=("Arial", 12), command=stop_assistant, bg="#153344", fg="white")
    stop_button.place(relx=0.94, rely=0.95, anchor="se")

    # Create a label widget to display the name of the assistant
    luna = tk.Label(window, text="Luna", font=("Comic Sans MS", 36, "bold italic"), bg="#14303f", fg="white")
    luna.place(relx=0.93, rely=0.85, anchor="se")

    # Create a label widget to display the message to activate the assistant
    activate_label = tk.Label(window, text="To activate, press: 'ctrl+1' or 'Start'", font=("Arial", 12), bg="#286277", fg="white")
    activate_label.place(relx=0.5, rely=0.96, anchor="center")
    
    # disable maximize button
    window.resizable(False, False)  


    # Start the GUI loop
    window.mainloop()
    
