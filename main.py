from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
import time


PROMISED_DOWN = 1000
PROMISED_UP = 800
CHROME_DRIVER_PATH = "C:\Development\chromedriver_win32"
TWITTER_EMAIL = "mariam499512665"
TWITTER_PASSWORD = "Asdfghjkl5208"


class InternetSpeedTwitterBot:
    def __init__(self, driver_path):
        service = Service(driver_path)
        self.driver = webdriver.Chrome(service=service)
        self.down = 0
        self.up = 0

    def get_internet_speed(self):
        self.driver.get("https://www.speedtest.net/result/14955529852")


        time.sleep(3)
        go_button = self.driver.find_element(by=By.CSS_SELECTOR, value=".start-button a")
        go_button.click()

        time.sleep(60)
        up = self.driver.find_element(by=By.CLASS_NAME, value="upload-speed").text
        down = self.driver.find_element(by=By.CLASS_NAME, value="download-speed").text
        print(up, down)

    def tweet_at_provider(self):
        self.driver.get("https://twitter.com/i/flow/login?redirect_after_login=%2Flogin")

        time.sleep(10)
        email = self.driver.find_element(by=By.CSS_SELECTOR, value='input[name="text"]')
        email.send_keys(TWITTER_EMAIL)
        next_button = self.driver.find_element(by=By.XPATH, value='//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]')
        next_button.click()
        wait = WebDriverWait(self.driver, 10)
        password = wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, 'input[type="password"]')))
        password.send_keys(TWITTER_PASSWORD)
        time.sleep(2)
        password.send_keys(Keys.ENTER)
        time.sleep(5)
        print("logged in successfully")

    def compose_tweet(self):
        try:
            # Click the tweet compose button
            tweet_compose = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/compose/tweet"][aria-label="Tweet"]')))
            tweet_compose.click()

            tweet = f"Hey Internet Provider, why is my internet speed {self.down}down/{self.up}up when I pay for {PROMISED_DOWN}down/{PROMISED_UP}up?"
            tweet_box = self.driver.find_element(by=By.XPATH, value='//div[@data-testid="tweetTextarea_0"]')
            tweet_box.click()
            tweet_box.send_keys(tweet)

            # Add a small delay to ensure the tweet text is entered before clicking the tweet button
            time.sleep(10)
            # Click the tweet button to send the tweet
            tweet_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@data-testid="tweetButton"]')))
            tweet_button.click()

            # Add a small delay to allow the tweet to be sent (you can adjust the delay based on your needs)
            time.sleep(10)

        except Exception as e:
            print("Error: ", e)

        finally:
           self.driver.quit()


bot = InternetSpeedTwitterBot(CHROME_DRIVER_PATH)
bot.get_internet_speed()
bot.tweet_at_provider()
