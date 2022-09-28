import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import requests
import creds
import random

PATH = Service(executable_path=creds.DRIVER_PATH)


def get_random_word_and_definition():
    global definition
    global tweet
    with open("words_list.txt") as file:
        word = file.read().splitlines()
        random_word = random.choice(word)
    try:
        response = requests.get(url=f"https://api.dictionaryapi.dev/api/v2/entries/en/{random_word}")
        response.raise_for_status()
        json = response.json()
        meanings = json[0]['meanings']
        definition = meanings[0]['definitions'][0]['definition']

    except requests.exceptions.HTTPError or NameError:
        random_word = random.choice(word)

    tweet = f"{random_word.capitalize()}: {definition.capitalize()}"
    print(tweet)
    return tweet


class TwitterBot:
    def __init__(self, driver):
        self.driver = webdriver.Chrome(executable_path=creds.DRIVER_PATH)

    def tweet_word(self):
        # signing in/email
        self.driver.get("https://twitter.com/i/flow/login")
        self.driver.implicitly_wait(15)
        self.email_input = bot.driver.find_element(By.XPATH, '//input[@autocomplete="username"]')
        self.email_input.click()
        self.email_input.send_keys(creds.TWITTER_EMAIL)
        self.email_input.send_keys(Keys.ENTER)

        # enter phone number
        self.driver.implicitly_wait(5)

        # password
        self.driver.implicitly_wait(5)
        self.pass_input = bot.driver.find_element(By.XPATH, '//input[@autocomplete="current-password"]')
        self.pass_input.send_keys(creds.TWITTER_PASSWORD)
        self.pass_input.send_keys(Keys.ENTER)

        # sending tweet
        self.driver.implicitly_wait(5)
        self.tweet_input = bot.driver.find_element(By.XPATH, '//div[contains(@aria-label, "Tweet text"])')
        self.tweet_input.send_keys(tweet)
        self.tweet_input.send_keys(Keys.ENTER)


get_random_word_and_definition()
bot = TwitterBot(PATH)
bot.tweet_word()
