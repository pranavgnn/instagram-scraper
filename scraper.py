from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
import os
from dotenv import load_dotenv


class InstagramScraper:
    def __init__(self):
        self.options = Options()
        # self.options.add_experimental_option("detach", True)
        self.options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=self.options)
        self.wait = WebDriverWait(self.driver, 5)
        self.cookies_file = "instagram_cookies.pkl"  # File to store cookies

    def login(self, username: str, password: str):
        self.driver.get("https://www.instagram.com/accounts/login/")

        username_input = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
        password_input = self.driver.find_element(By.NAME, "password")

        username_input.send_keys(username)
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)

        self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'x1n2onr6')]")))

        self.save_cookies()
        print("Cookies have been saved.")

    def save_cookies(self):
        with open(self.cookies_file, "wb") as file:
            pickle.dump(self.driver.get_cookies(), file)

    def load_cookies(self):
        if os.path.exists(self.cookies_file):
            with open(self.cookies_file, "rb") as file:
                cookies = pickle.load(file)
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
            print("Cookies have been loaded.")
        else:
            print("No cookies file found. Please log in manually.")


    def update_cookies(self):
        self.save_cookies()
        print("Cookies have been updated.")


    def scrape(self, username: str):
        self.driver.get("https://www.instagram.com/")
        self.load_cookies()
        self.driver.refresh()

        self.driver.get(f"https://www.instagram.com/{username}/")

        profile_pic = None
        try:
            profile_pic = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//img[contains(@src, '.fbcdn.net')]")
            )).get_attribute("src")
        except Exception:
            pass

        posts, followers, following = None, None, None
        try:
            stats = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//ul/li/div//span")))

            posts = stats[0].get_attribute("title") if stats[0].get_attribute("title") else stats[0].text
            followers = stats[2].get_attribute("title") if stats[2].get_attribute("title") else stats[2].text
            following = stats[4].get_attribute("title") if stats[4].get_attribute("title") else stats[4].text

            posts = int(posts.replace(",", ""))
            followers = int(followers.replace(",", ""))
            following = int(following.replace(",", ""))
                
        except Exception:
            pass

        name = None
        try:
            name = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//header/section/div[1]/div[1]/span")
            )).text
        except Exception:
            pass

        bio = None
        try:
            bio = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//header/section/div[1]/span/div/span")
            )).text
        except Exception:
            pass

        external_link = None
        try:
            external_link = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//header/section/div[1]/div[3]/div[1]/a")
            )).get_attribute("href")
        except Exception:
            pass

        self.driver.quit()

        return {
            "username": username,
            "profile_pic": profile_pic,
            "posts": posts,
            "followers": followers,
            "following": following,
            "name": name,
            "bio": bio,
            "external_link": external_link
        }


if __name__ == "__main__":
    load_dotenv()

    scraper = InstagramScraper()

    instagram_username = os.environ.get("INSTAGRAM_USERNAME")
    instagram_password = os.environ.get("INSTAGRAM_PASSWORD")
    profile_to_scrape = "cristiano"

    # scraper.login(instagram_username, instagram_password)
    # time.sleep(10)
    # scraper.update_cookies()

    data = scraper.scrape(profile_to_scrape)
    print(data)