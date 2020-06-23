#Authors: Fahad Shaikh; Mariam Baloch; Haris Karim Ladhani
#Instructor: Shah Jamal Alam
#Title: Project Officium
#CS102 - Data Structures and Algorithms

import tkinter as tk
import tkinter.ttk as ttk
from ttkthemes import ThemedStyle
from gtts import gTTS
import os
import re
import webbrowser
import random
import smtplib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.request
import urllib.parse
import wikipedia
import pyowm
import sys
from time import strftime
import logging
from pygame import mixer
import time
import datetime

#push function for the stacks
def push(intent, ele):
    global my_stack
    global my_stack2
    if intent == "my_stack":
        if len(my_stack)==2:
            del my_stack[:]
            my_stack.append(ele)
        else:
            my_stack.append(ele)
    elif intent == "my_stack2":
        if len(my_stack2)==2:
            del my_stack2[:]
            my_stack2.append(ele)
        else:
            my_stack2.append(ele)

def pop(): #separate pop function for the mystack - i.e. the "back" stack - mapped to the back button
    global my_stack
    global my_stack2
    if is_empty(my_stack):
        blank.insert(0,"No previous commands.")
    else:
        a = my_stack.pop()
        push("my_stack2", a)
        blank.insert(0, a)
def pop2(): #separate pop function for the mystack2 - i.e. the "forward" stack - mapped to the forward button
    global my_stack2
    global my_stack
    if is_empty(my_stack2):
        blank.insert(0, "No future commands")
    else:
        b = my_stack2.pop()
        push("my_stack", b)
        blank.insert(0, b)

def is_empty(lst):
    if len(lst)==0:
        return True
    else:
        return False

def my_command():
    global command1
    global c2
    global c3
    global c4
    global c5
    global c6
    global my_stack
    global my_stack2
    command = command1.get()
    str1 = c2.get()
    str2 = c3.get()
    str3 = c4.get()
    str4 = c5.get()
    str5 = c6.get()
    push("my_stack", command)
    assistant(command, str1, str2, str3, str4, str5)

def speak(msg): #system media player output for longer msgs to give user the option of not listening to the entire thing
    logging.info("Officium communicated the following to the user: {}".format(msg))
    for lines in msg.splitlines():
        tts = gTTS(text=lines , lang="en-uk", slow=False)
        tts.save("output.mp3")
        os.system("start output.mp3")

def talk(audio): #direct aduio output for smaller msgs
    date_string = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
    filename = "voice"+date_string+".mp3"
    logging.info("Officium communicated the following to the user: {}".format(audio))
    for line in audio.splitlines():
        text_to_speech = gTTS(text=line, lang='en-uk', slow=False)
        text_to_speech.save(filename)
        mixer.init()
        mixer.music.load(filename)
        mixer.music.play()
        time.sleep(3) #necessary otherwise audio wont play - gives the mixer some time to properly initialize.

def assistant(command, str1, str2, str3, str4, str5):
    error_msgs = ["I don't know what you mean", #list of error msgs that randomly cycled through if user enters wrong
                  "Please repeat yourself",     #commands
                  "Incorrect command",
                  "I cannot do what you ask"
                  ]
    if "open website" in command: #navigating to a specific web page
        logging.info(command)
        reg_ex = re.search('open website (.+)', command)  #regular expression used to isolate domain
        if reg_ex:
            domain = reg_ex.group(1)
            print("The domain is {}".format(domain))
            website_url = 'https://' + str(domain) #building a url
            webbrowser.open(website_url) #passing the url onto the webbrowser module that will load the page
            #speak("The website you requested has been opened")
            talk("The website you requested has been opened") #notify user of completion of task
        else:
            pass
    elif "email" in command: #sending an email to someone
        logging.info("Email sent to {} from {} with the following message {}".format(str2, str4, str3))
        #speak("What is the subject?")
        subject = str1  #subject entry field input
        #speak("Who is the recipient?")
        recipient = str2  #recipient address entry field input
        #speak("What do you want to say?")
        message = str3   #message entry field input
        content = 'Subject: {}\n\n{}'.format(subject, message) #format the different fields w.r.t to the email client
        mail = smtplib.SMTP('smtp.gmail.com', 587) #connect to the gmail mail server
        mail.ehlo()
        mail.starttls() #starting TLS encryption
        #speak("Enter your id")
        user_id = str4
        #speak("Enter Password")
        user_pwrd = str5
        mail.login(user_id, user_pwrd) #logging into users gmail account
        mail.sendmail(user_id, recipient, content)
        mail.close() #ending the session
        talk("Email has been sent.") #notify user of completion of task

    elif "google search" in command: #performing a google search
        logging.info(command)
        reg_ex = re.search('google search (.*)', command)  #isolate search query
        query = command.split("search", 1)[1]
        website_url = "https://www.google.com/" #url for google website
        if reg_ex:
            domain = reg_ex.group(1)
            url = domain + "r/" + str(domain) #building the actual url with search query
        driver = webdriver.Firefox(executable_path=r'C:\Users\fahad\Documents\Pycharm Projects\geckodriver')
        driver.get(website_url)  #using selenium and GeckoDriver to automate the process
        search = driver.find_element_by_name("q") #perform the actual search
        search.send_keys(str(query))
        search.send_keys(Keys.RETURN)
        talk("Required search has been performed.") #notify user of completion of task
    elif "youtube" in command: #perform a YouTube search
        logging.info(command)
        reg_ex = re.search("youtube (.+)", command) #isolate search query
        if reg_ex:
            domain = command.split("youtube", 1)[1]
            query = urllib.parse.urlencode({"search query": domain})
            html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + str(query)) #access html content
            search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html.read().decode()) #change encoding scheme
            webbrowser.open("https://www.youtube.com/watch?v={}".format(search_results[0])) #pass onto webbrowser module to load page
            talk("The requested video is being played.") #notify user of completion
            pass
    elif "wikipedia" in command:
        logging.info(command)
        reg_ex = re.search("wikipedia (.*)", command) #isolate query
        try:
            if reg_ex:
                topic = reg_ex.group(1)
                search = wikipedia.page(topic) #access content page after GET request is successful
                a = str(search.content[:500].encode('utf-8')) #change encoding of page to string encoding
                blank.insert(0, a[1:])
                speak(a[1:]) #pass onto SPEAK function to be read out like a audio book
                #talk(a[1:])
        except Exception as e:
            print(e)

    elif "weather" in command:
        logging.info(command)
        reg_ex = re.search("weather (.*)", command) #isolate location
        if reg_ex:
            city = reg_ex.group(1)
            owm = pyowm.OWM(API_key='ab0d5e80e8dafb2cb81fa9e82431c1fa') #access Open Weather Maps data
            obs = owm.weather_at_place(city) #data for our required city
            w = obs.get_weather() #weather data
            k = w.get_status() #current situation
            x = w.get_temperature() #temperatures
            temp = round(x["temp"] - 273.15, 2) #convert temps from farenheit to celsius
            max_temp = round(x["temp_max"] - 273.15, 2)
            min_temp = round(x["temp_min"] - 273.15, 2)
            f=("{} currently has a temperature of {}. The expected maximum temperature is {} and the minimum"
                  "temperature is {}. The city is currently experiencing {}".format(city, temp, max_temp, min_temp, k))
            speak(f) #read the message to the user
            blank.insert(0, f)
    elif "time" in command: #time update
        logging.info(command)
        current_time = datetime.datetime.now() #read system clock
        talk("The current time is {} hours and {} minutes".format(current_time.hour, current_time.minute)) #inform user
    elif "quit" in command: #terminate the program
        logging.info(command)
        talk("Until next time!") #ending message
        logging.info("Program terminated.")
        sys.exit() #teminate
    elif "Hello" in command: #saluatation
        logging.info(command)
        day_time = int(strftime('%H')) #depending on time of day, give appropiate salutation
        if day_time < 12:
            talk("Good Morning. Project Officium at your service.")
        elif day_time >= 12 and day_time < 18:
            talk("Good afternoon. Project Officium at your service.")
        else:
            talk("Good evening. Project Officium at your service.")
        logging.info("Project offers salutation to user.")
    else: #error msgs in case of error in user command
        error_msg = random.choice(error_msgs)
        talk(error_msg)
        logging.info("user enters incorrect command - {}".format(command))
    command1.delete(first=0, last=100)  #clearing the specified entry field once execution is complete
    c2.delete(first=0, last=100)
    c3.delete(first=0, last=100)
    c4.delete(first=0, last=100)
    c5.delete(first=0, last=100)
    c6.delete(first=0, last=100)


#main
#start log file
logging.basicConfig(filename="project_officium_history.txt", level=logging.INFO, format="%(asctime)s ---- %(message)s")
main = tk.Tk() #the Tkinter window
#specifiy window elements
main.title("Project Officium")
main.geometry("845x345")
main['background']='#8FBC8F'
style = ThemedStyle(main)
style.set_theme("scidgreen")
a = tk.Label(main, text = "Enter Command:", relief = "ridge", fg= "grey1", bg = "grey85", font = ('Franklin Gothic Medium Cond',11)).grid(row=0)
b=tk.Label(main, text = "Start Guide:", relief = "ridge", fg= "grey1", bg = "grey85",font = ('Franklin Gothic Medium Cond',11)).grid(row=0, column=2)
c=tk.Label(main, text = "Assistant says:", relief = "ridge", fg= "grey1", bg = "grey85",font = ('Franklin Gothic Medium Cond',11)).grid(row=1)
d=tk.Label(main, text = "1. open website <website_name>.com", relief = "ridge", fg= "grey1", bg = "grey85",font = ('Franklin Gothic Medium Cond',11)).grid(row=1, column=2)
e=tk.Label(main, text = "2. email - and then fill out the additional boxes", relief = "ridge", fg= "grey1", bg = "grey85",font = ('Franklin Gothic Medium Cond',11)).grid(row=2, column=2)
f=tk.Label(main, text = "3. google search <query>", relief = "ridge", fg= "grey1", bg = "grey85",font = ('Franklin Gothic Medium Cond',11)).grid(row=3, column=2)
g=tk.Label(main, text = "4. youtube <query>", relief = "ridge", fg= "grey1", bg = "grey85",font = ('Franklin Gothic Medium Cond',11)).grid(row=4, column=2)
h=tk.Label(main, text = "5. wikipedia <query>", relief = "ridge", fg= "grey1", bg = "grey85",font = ('Franklin Gothic Medium Cond',11)).grid(row=5, column=2)
i=tk.Label(main, text = "6. weather <location_name>", relief = "ridge", fg= "grey1", bg = "grey85",font = ('Franklin Gothic Medium Cond',11)).grid(row=6, column=2)
j=tk.Label(main, text = "7. time", relief = "ridge", fg= "grey1", bg = "grey85",font = ('Franklin Gothic Medium Cond',11)).grid(row=7, column=2)
k=tk.Label(main, text = "8. quit", relief = "ridge", fg= "grey1", bg = "grey85",font = ('Franklin Gothic Medium Cond',11)).grid(row=8, column=2)
l=tk.Label(main, text = "9. Hello", relief = "ridge", fg= "grey1", bg = "grey85",font = ('Franklin Gothic Medium Cond',11)).grid(row=9, column=2)
m=tk.Label(main, text = "----Additional Fields to fill if Email is command----", relief = "ridge", fg= "grey1", bg = "grey85",font = ('Franklin Gothic Medium Cond',11)).grid(row=2)
n=tk.Label(main, text = "Enter Subject:", relief = "ridge", fg= "grey1", bg = "grey85",font = ('Franklin Gothic Medium Cond',11)).grid(row=3)
o=tk.Label(main, text = "Enter Recipient id:", relief = "ridge", fg= "grey1", bg = "grey85",font = ('Franklin Gothic Medium Cond',11)).grid(row=4)
p=tk.Label(main, text = "Enter Message:", relief = "ridge", fg= "grey1", bg = "grey85",font = ('Franklin Gothic Medium Cond',11)).grid(row=5)
q=tk.Label(main, text = "Enter your id:", relief = "ridge", fg= "grey1", bg = "grey85",font = ('Franklin Gothic Medium Cond',11)).grid(row=6)
r=tk.Label(main, text = "Enter your password:", relief = "ridge", fg= "grey1", bg = "grey85",font = ('Franklin Gothic Medium Cond',11)).grid(row=7)

my_stack = []
my_stack2 = []
#create physical elements of the window - buttons and fields- also place them
command1 = ttk.Entry(main)
blank = ttk.Entry(main)
c2 = ttk.Entry(main)
c3 = ttk.Entry(main)
c4 = ttk.Entry(main)
c5 = ttk.Entry(main)
c6 = ttk.Entry(main, show="*") #password entry field thus, hidden.

command1.grid(row=0, column=1, ipadx = 75)
blank.grid(row=1, column=1,ipadx=75)
c2.grid(row=3, column=1, ipadx = 75)
c3.grid(row=4, column=1, ipadx = 75)
c4.grid(row=5, column=1, ipadx = 75)
c5.grid(row=6, column=1, ipadx = 75)
c6.grid(row=7, column=1, ipadx = 75)

#create, map and place the buttons
b1 = ttk.Button(main, text='Quit', command=main.destroy).grid(row=9, column=0,  pady=4)
b2 = ttk.Button(main, text='Execute', command=my_command).grid(row=9, column=1, pady=4)
#b3 and b4 mapped using lambda because this anonymous mapping prevents automatic execution of history traversal
b3 = ttk.Button(main, text='Back', command=lambda: pop()).grid(row=10, column=0, pady=4)
b4 = ttk.Button(main, text='Forward', command=lambda: pop2()).grid(row=10, column=1, pady=4)

#loop the window
main.mainloop()
