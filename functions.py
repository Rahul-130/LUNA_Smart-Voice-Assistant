import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from PIL import Image, ImageTk
import warnings
warnings.filterwarnings("ignore")
import speech_recognition as sr 
import webbrowser
import os
import smtplib
import ctypes
import pyautogui
import time
import random
import requests
import platform
import psutil
import pyjokes      #pip install pyjokes
import wmi          #pip install wmi
import urllib.parse
import urllib.request
import bs4
from forex_python.converter import CurrencyRates        # pip install forex-python
import json
import datetime

import hidden        # imported hidden.py file
import voice_assistant  as s  # imported main.py file

# <---------------------------------------------------- get_location ----------------------------------------------------->
def get_location():
    # API endpoint to get the location data
    API_endpoint = "http://ip-api.com/json"
    # Make a GET request to the API endpoint
    response = requests.get(API_endpoint)
    # Get the JSON data from the response
    location_data = response.json()
    # Return the city and country name
    return location_data["city"], location_data["country"]

# <--------------------------------------------------- get_weather ------------------------------------------------------>
def get_weather(city, country):
    # API key for OpenWeatherMap
    API_key = hidden.OpenWeatherMap_API_key
    # API endpoint to get the current weather data
    API_endpoint = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "," + country + "&appid=" + API_key
    # Make a GET request to the API endpoint
    response = requests.get(API_endpoint)
    # Get the JSON data from the response
    weather_data = response.json()
    temperature = round(weather_data["main"]["temp"] - 273.15, 2)
    weather = weather_data["weather"][0]["description"]
    # Print the temperature in Celsius
    s.speak("The temperature in " + city + " is " + str(temperature) + "°C" + "and its"+ weather)
    return weather_data["weather"][0]["description"]

# <------------------------------------------------- reminder -------------------------------------------->
# def reminder():
#     s.speak("What should I remember?")
#     Information=s.takeCommand()
#     s.speak('you said me to remember that '+Information)
#     rem = open('data.txt','w') 
#     rem.write(Information) 
#     rem.close() 
# <----------------------------------------------------- reminder_knowing ----------------------------------------->
def reminder_knowing():
    reminder = open('data.txt','r')
    return reminder.read()

# <------------------------------------------------------ change_desktop_background ------------------------------------>
def change_desktop_background():
    os_name = platform.system()
    version = platform.release()
    if os_name == "Windows":
        if version == "10" or version == "8" or version == "9":
            SPI_SETDESKWALLPAPER = 20
            files = [f for f in os.listdir("C:\Windows\Web\Wallpaper\Windows") if f.endswith(".jpg") or f.endswith(".jpeg") or f.endswith(".png")]
            image_path = os.path.join("C:\Windows\Web\Wallpaper\Windows", random.choice(files))
            ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 0)
        else:
            print(f"Changing the desktop background is not supported on Windows {version}")
            s.speak(f"Changing the desktop background is not supported on Windows {version}")
    else:
        print(f"The operating system is not Windows: {os_name}")
        s.speak(f"The operating system is not Windows: {os_name}")
        

# <----------------------------- Increase and decrease brightness ----  using import wmi win32con ----------------------------->
# define the brightness levels
BRIGHTNESS_MIN = 0
BRIGHTNESS_MAX = 100
BRIGHTNESS_STEP = 10

# connect to the WMI service
c = wmi.WMI(namespace='wmi')

# define a function to get the current brightness
def get_brightness():
    brightness = c.WmiMonitorBrightness()[0].CurrentBrightness
    return brightness

# define a function to set the brightness
def set_brightness(brightness):
    brightness = max(min(brightness, BRIGHTNESS_MAX), BRIGHTNESS_MIN)
    c.WmiMonitorBrightnessMethods()[0].WmiSetBrightness(brightness, 0)

# define a function to increase brightness
def increase_brightness():
    current_brightness = get_brightness()
    new_brightness = current_brightness + BRIGHTNESS_STEP
    set_brightness(new_brightness)
    result = "Brightness increased!"
    return result

# define a function to decrease brightness
def decrease_brightness():
    current_brightness = get_brightness()
    new_brightness = current_brightness - BRIGHTNESS_STEP
    set_brightness(new_brightness)
    result = "Brightness decreased!"
    return result

# <------------------------------------------   using import pyautogui  ---------------------------------------------------->
def decrease_volume():
    for i in range(0,4):
        pyautogui.press("volumedown")
    result = "Volume decreased"
    return result
def increase_volume():
    for i in range(0,4):
        pyautogui.press("volumeup")
    result = "Volume increased"
    return result
# <--------------------------------------      using import pyjokes  ------------------------------------------------------->
def jokes():
    result = pyjokes.get_joke()
    return result

# <--------------------------------------      using webbrowser     -------------------------------------------------------->
# limatstion with only .com extension websites
def openWebsite(command):
    website = command.replace("open website", "").strip()
    webbrowser.open_new_tab(website+'.com')

# def GoogleSearch():
#     s.speak("What should I search?")
#     SearchData=s.takeCommand()
#     SearchDataInput = urllib.parse.quote(SearchData)
#     webbrowser.open_new_tab("https://www.google.com/search?q=" + SearchDataInput)
#     result = "opend your search result"
#     return result

# libraries required urllib.request   bs4   webbrowser
def news():     
    url = "https://news.google.com/news/rss"
    client = urllib.request.urlopen(url)
    xml_page = client.read()
    client.close()
    page = bs4.BeautifulSoup(xml_page, 'xml')
    news_list = page.findAll("item")
    s.speak("Today's top headlines are--")
    try:
        for news in news_list:
            print(news.title.text)
            s.speak(f"{news.title.text}")
            print()
    except Exception as e:
        pass

# using          from forex_python.converter import CurrencyRates
def currencyConvert():
    try:
        curr_list = {
            'dollar': 'USD', 'taka': 'BDT', 'dinar': 'BHD',
            'rupee': 'INR', 'afghani': 'AFN', 'real': 'BRL',
            'yen': 'JPY', 'peso': 'ARS', 'pound': 'EGP', 'rial': 'OMR',
            'lek': 'ALL', 'kwanza': 'AOA', 'manat': 'AZN', 'franc': 'CHF'
        }

        cur = CurrencyRates()
        # s.output(curr_list)
        # print(cur.get_rate('USD', 'INR'))
        s.speak('From which currency u want to convert?')
        from_cur = s.takeCommand()
        src_cur = curr_list[from_cur.lower()]
        s.speak('To which currency u want to convert?')
        to_cur = s.takeCommand()
        dest_cur = curr_list[to_cur.lower()]
        s.speak('Tell me the value of currency u want to convert.')
        val_cur = float(s.takeCommand())
        # print(val_cur)
        result = cur.convert(src_cur, dest_cur, val_cur)
                        
    except Exception as e:
        result = "Couldn't get what you have said, Can you say it again??"
        # print("Couldn't get what you have said, Can you say it again??")
    return result

# <--------------- calculate the expression ------------------------->
def replace_words(text, word_dict):
    for key in word_dict:
        text = text.replace(key, word_dict[key])
    return text

def calculate(expression):
    try:
        return eval(expression)
    except:
        return "Sorry, I could not perform the calculation"
word_dict = {"multiply": "*", "multiplied by": "*", "times": "*", "plus": "+", "minus": "-", "divided by": "/", "to the power of": "**", "^": "**", "mod": "%", "remainder": "%"}

# <--------------------  get the general answers  ----------------------->
# set up Google Custom Search API credentials
api_key = hidden.google_search_API_key
search_engine_id = hidden.MySearchEngine_ID
# Define function to get answer from Google search
def get_answer(question):
    # Format question for Google search
    formatted_question = question.replace(" ", "+")
    # Make API request to Google search API
    response = requests.get(f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_engine_id}&q={formatted_question}")
    # Parse response JSON and get answer
    try:
        answer = response.json()["items"][0]["snippet"]
    except:
        answer = "Sorry, I could not get it."
    return answer

def email():
    def set_body(text):
        body.set(text)
        # Define the function to send an email
    def send_email():
        # Get the recipient email and subject
        recipient = email_entry.get()
        subject = subject_entry.get()

        # Define the sender's email and password
        # sender_email = hidden.sender_email
        # password = hidden.email_password

        # read the config file
        with open('email_password_config.json', 'r') as f:
            config = json.load(f)
        # extract email and password from config
        sender_email = config['sender_email']
        password = config['password']

        # Create a connection to the Gmail SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)

        # Compose the email message
        message = f"Subject: {subject}\n\n{body.get()}"

        try:
            # Send the email
            server.sendmail(sender_email, recipient, message)
            status_label.config(text="Email sent successfully!", fg="green")
            s.speak("Email sent successfully!")
        except Exception as e:
            print(e)
            status_label.config(text="Failed to send email.", fg="red")
            s.speak("Failed to send email.")
        finally:
            server.quit()

        # Clear input fields
        email_entry.delete(0, tk.END)
        subject_entry.delete(0, tk.END)
        body.set("")
        body_label.config(textvariable="")
        

    # Define the function to get voice input for email message
    def get_email_message():
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            s.speak("Listening...")
            audio = recognizer.listen(source)

        try:
            audio_input_message = recognizer.recognize_google(audio)
            print(f"You said: {audio_input_message}")
            body.set(audio_input_message)
            # update the body_label widget with the new text
            body_label.config(text=body.get())
            # body_label.config(textvariable=body)
            status_label.config(text="Got the email message..", fg="green")
            s.speak("Got the email message..")
            return audio_input_message
        except Exception as e:
            print(e)
            status_label.config(text="Error getting email message.", fg="red")
            s.speak("Error getting email message.")
            return ""

    # Define the function to get text input for email message
    def get_email_message_text():
        # Create a new window for text input
        text_window = tk.Toplevel(window)
        text_window.title("Email Message Text")

        # set logo for window
        window.iconbitmap("animations\email_icon.ico")


        # Set the window size as a percentage of the parent window size
        window_width = window.winfo_width() * 0.5
        window_height = window.winfo_height() * 0.5
        x = int((window.winfo_screenwidth()/2) - (window_width/2))
        y = int((window.winfo_screenheight()/2) - (window_height/2))
        text_window.geometry(f"{int(window_width)}x{int(window_height)}+{x}+{y}")
        text_window.resizable(False, False)  # disable maximize button
        # Create the GUI elements for text input
        body_field_label = tk.Label(text_window, text="Email Message:")
        body_field_label.grid(row=0, column=0, sticky="w", padx=10)
        body_field = tk.Text(text_window, width=27, height=5)
        body_field.grid(row=1, column=0, padx=10, pady=8)
        body_field.config(highlightbackground="black", highlightthickness=1)

        def update_body():
            body.set(body_field.get("1.0", tk.END))
            body_label.config(text=body.get())
            text_window.destroy()

        update_button = tk.Button(text_window, text="Update", command=update_body)
        update_button.grid(row=2, column=0, padx=10, pady=8)




    # functions for creting hover effect  'bind' method is used from tkinter
    # Define the function to change the button color on hover
    def on_enter(e):
        e.widget['background'] = '#FF5733'

    # Define the function to change the button color back on hover exit
    def on_leave(e):
        e.widget['background'] = '#F9C5B5'
    
    def update_wraplength():
        # Get the current width of the parent widget
        width = body_label.master.winfo_width()

        # Update the wraplength based on the current width
        body_label.config(wraplength=width-20)

    # Create a GUI window
    window = tk.Tk()
    # window.geometry("400x400")
    window.title("Send Email")
    window.configure(bg="light blue")

    # Set the window size and position
    window_width = 600
    window_height = 400
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width/2) - (window_width/2))
    y = int((screen_height/2) - (window_height/2))
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Create the GUI elements
    tk.Label(window, text="Recipient Email:", bg="light blue").pack()
    email_entry = tk.Entry(window, width=30)
    email_entry.pack(padx=10, pady=2)

    tk.Label(window, text="Email Subject:", bg="light blue").pack()
    subject_entry = tk.Entry(window, width=30)
    subject_entry.pack(padx=10, pady=2)

    body = tk.StringVar()

    # wraplength=400 its to ajust the size of text conent on screen
    tk.Label(window, text="Email Message:", bg="light blue").pack()
    body_label = tk.Label(window, text="", wraplength=380)
    body_label.pack(padx=10, pady=8)

    update_wraplength()

    # Bind the function to the window resize event
    window.bind("<Configure>", lambda e: update_wraplength())
    

    voice_button = tk.Button(window, text="Get Email Message (Voice)", command=lambda: set_body(get_email_message()))
    voice_button.pack(padx=10, pady=5)
    # for the voice_button hover
    voice_button.bind('<Enter>', on_enter)
    voice_button.bind('<Leave>', on_leave)

    text_button = tk.Button(window, text="Get Email Message (Text)", command=lambda: set_body(get_email_message_text()))
    text_button.pack(padx=10, pady=5)
    # for the text_button hover
    text_button.bind('<Enter>', on_enter)
    text_button.bind('<Leave>', on_leave)

    send_button = tk.Button(window, text="Send Email", command=send_email)
    send_button.pack(padx=10, pady=5)
    # for the send_button hover
    send_button.bind('<Enter>', on_enter)
    send_button.bind('<Leave>', on_leave)

    status_label = tk.Label(window, text="", bg="light blue")
    status_label.pack()

    # Start the GUI main loop
    window.mainloop()

# create a email_password_config.json file and write     { "sender_email": "", "password": "" }   (Application-specific password is required) -------------------->
def update_email_config():
    try:
        with open('email_password_config.json', 'r') as f:
            config = json.load(f)
            sender_email = config['sender_email']
            password = config['password']
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        # If the file doesn't exist or is corrupt, create a new one
        sender_email = input("Enter sender email: ")
        password = input("Enter password: ")
        config = {"sender_email": sender_email, "password": password}
        with open('email_password_config.json', 'w') as f:
            json.dump(config, f)
            print("Config file created.")
    except Exception as e:
        print(f"Error: {e}")
        s.speak(f"Error: {e}")
        return

    # Check if the credentials are valid by trying to log in
    try:
        # Code to log in and send email using the sender_email and password
        # ...
        print("Credentials are valid.")
    except Exception as e:
        print(f"Error: Invalid email or password: {e}")
        return

    # If the credentials are valid, allow the user to update them
    while True:
        update = input("Would you like to update your email or password? (y/n): ")
        if update.lower() == 'n':
            break
        elif update.lower() == 'y':
            sender_email = input("Enter new sender email: ")
            password = input("Enter new password (Application-specific password is required): ")
            config = {"sender_email": sender_email, "password": password}
            try:
                with open('email_password_config.json', 'w') as f:
                    json.dump(config, f)
                    print("Config file updated.")
            except Exception as e:
                print(f"Error: {e}")
                return
        else:
            print("Invalid input.")

    # -------------------------------------------------



# Help
def help():
    print('To know the content from wikipedia -- wikipedia content_name')
    print('To open calculator  -- open calculator')
    print('To know the weather  --  get weather')
    print('To set reminder -- set reminder')
    print('To know the reminder  -- know reminder')
    print('To increase brightness  == increase brightness')
    print('To decrease brightness  -- decrease brightness')
    print('To increase volume  -- increase volume')
    print('To decrease volume  -- decrease volume')
    print("If u wanna know joke  -- tell me a joke 'OR' tell a joke 'OR' make me laugh" )
    print("To search anything in internet  --  search 'OR' google search")
    print("To open any website -- open website website_name '(# the input should content the word as open website website_name which u need to search ex: open website gmail #limatstion with only .com extension websites)'")
    print("To know latest news headlines  --  news 'OR' news headlines")
    print("To open Youtube  --  open youtube")
    print("To open google  --  open google")
    print("To open firefox  --  open firefox")
    print("To open facebook  --  open facebook")
    print("To open Zoom meeting  --  open zoom")
    print("To open instagram  --  open instagram  'OR'  open insta")
    print("To open coursera  --  open coursera")
    print("To open linkedin  --  open linkedin")
    print("To open gmail -- open gmail")
    print("To open yahoo -- open yahoo")
    print("To open zomato -- open zomato")
    print("To open swiggy -- open swiggy")
    print("To open bookmyshow -- open bookmyshow")
    print("To open google meet -- open google meet")
    print("To open teams -- open teams")
    print("To open quora -- open quora")
    print("To open brainly -- open brainly")
    print("To open stack overflow -- open stack overflow")
    print("To open github -- open github")
    print("To open colab -- open colab")
    print("To open vnr -- open vnr")
    print("To open eduprime -- open eduprime")
    print("To open whatsapp web  --  open whatsapp  'OR'  open whatsapp web")
    print("To open spotify or play music --  open spotify  'OR'  play music  'OR'  play song")
    print("To get the time  --  time")
    print("To get the date  --  date")
    print("To open powerpoint  --  open powerpoint")
    print("To open word  --  open word")
    print("To open excel  --  open excel")
    print("To open outlook  --  open outlook")
    print("To close powerpoint  --  close powerpoint")
    print("To close word  --  close word")
    print("To close excel  --  close excel")
    print("To close outlook  --  close outlook")
    print("To open notepad  --  open notepad")
    print("To close notepad  --  close notepad")
    print("To open camera  --  open camera")
    print("To close camera  --  close camera")
    print("To open visual studio code  --  open visual studio code  'OR'  open vs code  'OR'  open visual code")
    print("To close visual studio code  --  close visual studio code  'OR'  close vs code  'OR'  close visual code")
    print("To page up  --  page up")
    print("To page down  -- page down")
    print("To scroll up (it stops scrolling when the user press 'Esc' key)  --  scroll up")
    print("To scroll down (it stops scrolling when the user press 'Esc' key)  --  scroll down")
    print("To minimize  --  minimize")
    print("To maximize  --  maximize")
    print("To look the system  --  lock system 'OR' lock user 'OR' lock my system 'OR' lock my laptop")
    print("To open my computer or file explorer  --  open my computer 'OR' open explorer")
    print("To write any content in the input filed or 'speech to text'   --   speech to text 'OR'  write  'OR'  write the content")
    print("To open settings  --  open settings")
    print("To perform save operation  --  save")
    print("To perform copy operation  --  copy")
    print("To perform paste operation  --  paste")
    print("To perform undo operation  --  undo")
    print("To perform redo operation  --  redo")
    print("To perform print operation  --  print")
    print("To perform select all operation  --  select all")
    print("To open new tab   --  open new tab 'OR' open a new tab")
    print("To close tab  --  close tab")
    print("To go to beginning of the page  --  home  'OR'  beginning")
    print("To go to end of the page  --  end  'OR'  end of the page  'OR'  end of page")
    print("to send Email -- email 'OR' mail 'OR' send email 'OR' send mail")
    print("To set an alarm  --  set an alarm for time+(am or pm) eg: set an alarm for 3:05 pm  (limitation: until the alarm rings u cant perform any other task)")
    print('To calculate the expressions -- calculate num () num  ("multiply": "*", "multiplied by": "*", "times": "*", "plus": "+", "minus": "-", "divided by": "/", "to the power of": "**", "^": "**", "mod": "%", "remainder": "%")')
    print("To conver the currency  --  convert currency")
    print("normal covno -- hey or hello")
    print("normal covno -- how are you")
    print("normal covno -- what are you doing")
    
    print("To play song/video in youtube  -- play {name of the song/video/movie}")
    print("To open any application   --  open {application name}")
    print("To get or know the internet speed  --  internet speed")
    print("To take the screenshot  --  screenshot")
    print("To update the email and password (for sending email use Application-specific password)  --  update email")




