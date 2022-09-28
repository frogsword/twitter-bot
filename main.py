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
        definition = json[0]['meanings'][0]['definitions'][0]['definition']

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
        self.phone_input = bot.driver.find_element(By.XPATH, '//input[@autocomplete="on"]')
        self.phone_input.send_keys(creds.PHONE_NUMBER)
        self.phone_input.send_keys(Keys.ENTER)

        # password
        self.driver.implicitly_wait(5)
        self.pass_input = bot.driver.find_element(By.XPATH, '//input[@autocomplete="current-password"]')
        self.pass_input.send_keys(creds.TWITTER_PASSWORD)
        self.pass_input.send_keys(Keys.ENTER)

        # sending tweet
        self.driver.implicitly_wait(5)
        self.driver.find_element(By.CSS_SELECTOR, 'a[aria-label="Tweet"]').click()
        self.tweet_input = self.driver.find_element(By.CSS_SELECTOR, 'div[data-contents="true"]')
        self.tweet_input.send_keys(tweet)
        self.driver.find_element(By.CSS_SELECTOR, 'div[data-testid="tweetButton"]').click()
        self.driver.quit()


while True:
    # every 24 hours
    get_random_word_and_definition()
    bot = TwitterBot(PATH)
    bot.tweet_word()
    time.sleep(86400)
