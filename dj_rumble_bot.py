import random
import time

from resources.greetings import greetings
from resources.sentences import sentences
from resources.dialogues import dialogues

from multiprocessing import Pool

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument("--mute-audio")
options.add_argument('--headless')

MESSAGE_INPUT_ID = "new-message-input"

strings = sentences + dialogues

random.shuffle(strings)

sentences = greetings + strings


def spawn_player(message):

    # Initiate the browser
    browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    # browser.get("https://dj-rumble.herokuapp.com/rooms/series-openings")
    browser.get("https://dj-rumble.herokuapp.com/rooms/short-videos")
    # browser.get("http://localhost:4000/rooms/1979-songs")

    # Wait for page to load
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, MESSAGE_INPUT_ID))
    )

    element = browser.find_element_by_id(MESSAGE_INPUT_ID)

    [send_message(element) for n in range(1, 20)]

    # Close connection
    browser.stop_client()
    browser.close()


def send_message(element):
    message = random.choice(sentences)
    element.send_keys(message)
    element.submit()
    time.sleep(5)


with Pool(20) as p:
    p.map(spawn_player, range(4))
