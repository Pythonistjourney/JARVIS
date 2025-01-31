import speech_recognition as sr
import pyttsx3
import webbrowser
import openai
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

engine = pyttsx3.init()

def say(text):
    engine.say(text)
    engine.runAndWait()

def take_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.6
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-PK")  # Fixed language code
            print(f"User said: {query}")
            return query.lower()
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand. Please speak again.")
            return None
        except sr.RequestError:
            print("Could not connect to the recognition service. Check your internet.")
            return None

def control_web_page(url, command):
    # Initialize the WebDriver (make sure the path to your WebDriver is correct)
    driver = webdriver.Chrome(executable_path='D:\chromedriver-win64.zip\chromedriver-win64')  # Update the path to your chromedriver
    driver.get(url)
    
    if "click" in command:
        # Example: Click a button with a specific name
        try:
            element = driver.find_element_by_name("button_name")  # Replace with the actual button name
            element.click()
            say("Button clicked successfully.")
        except Exception as e:
            say("Could not find the button.")
    
    elif "search" in command:
        # Example: Search for something in a search bar
        try:
            search_box = driver.find_element_by_name("q")  # Replace with the actual search box name
            search_box.send_keys(" ".join(command.split()[1:]))
            search_box.send_keys(Keys.RETURN)
            say("Search completed.")
        except Exception as e:
            say("Could not find the search box.")
    
    # Add more commands as needed

    time.sleep(5)  # Wait for 5 seconds to see the result
    driver.quit()

if __name__ == "__main__":
    print("Python Voice Assistant Started")
    say("Hello, I am AI. I am listening to you.")

    sites = [
        ["youtube", "https://youtube.com"],
        ["wikipedia", "https://wikipedia.org"],
        ["google", "https://google.com"],
        ["instagram", "https://instagram.com"],
        ["facebook", "https://facebook.com"],
        ["twitter", "https://twitter.com"],
    ]  # Fixed the incorrect list structure

    while True:
        command = take_input()
        if not command:
            continue

        say(command)

        for site in sites:
            if f"open {site[0]}" in command:
                say(f"Opening {site[0]} sir")
                webbrowser.open(site[1])

        if "control web" in command:
            say("Which website would you like to control?")
            website = take_input()
            if website:
                url = f"https://{website}.com"
                say(f"Controlling {website}. Please give your command.")
                web_command = take_input()
                if web_command:
                    control_web_page(url, web_command)

        if "stop listening" in command:
            say("Okay, I am stopping now.")
            break