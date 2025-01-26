
# Instagram Scraper Tool
This automation project allows you to scrape:

 1. Username
 2. Name
 3. Bio
 4. External URL
 5. Posts Count
 6. Following Count
 7. Followers Count
 8. Profile Picture URL

From any Instagram account, regardless of the visibility status of the account (public/private).

## Example Usage
```py
from scraper import InstagramScraper
from time import sleep

scraper = InstagramScraper()

# Do this only for the first time
scraper.login("username", "password")
sleep(5)
scraper.update_cookies()
###

data = scraper.scrape("username_to_scrape")
print(data)
```

## How to Use

**Step 1:** Use the `.login()` and `.update_cookies()` functions to initially create the account cookie. This must create a `instagram_cookies.pkl` file in your local directory. I chose the cookie route to avoid flagging and to bypass Instagram's anti-scraping measures.
**NOTE:** You MIGHT have to add a `sleep(3)` between the two function calls to avoid detection.

**Step 2:** You have retrieved the cookie, you can comment the`.login()` and `.update_cookies)` calls.

**Step 3:** You are now free to scrape! Use the `.scrape()` function and pass your username as a parameter to retrieve details about that account!

## Documentation
1. `.login(username: str, password: str)`: Used to log into your instagram account programatically. Returns None.
2. `.save_cookies()`: Used to locally save the session cookie. Returns None.
3. `load_cookies()`: Used to load the locally saved cookie. Returns None.
4. `.update_cookies()`: Wrapper function for `.save_cookies()`. Returns None.
5. `.scrape(username: str)`: Used to retrieve above mentioned details about a profile. Returns python dictionary object.

## Future Improvements
1. Scrape more data: Maybe even scrape posts of public accounts
2. Better error handling and missing element detection
3. Improve speed
4. Try to avoid hard-coded values while retrieving elements
5. Dynamically decide whether to regenerate the cookie, instead of manual decision