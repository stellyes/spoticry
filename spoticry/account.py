import time
import utils
import pickle
import random
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

def request(user):
    headers= {
        "Accept-Encoding": "gzip",
        "Accept-Language": "en-US",
        "App-Platform": "Android",
        "Connection": "Keep-Alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "spclient.wg.spotify.com",
        "User-Agent": "Spotify/8.6.72 Android/29 (SM-N976N)",
        "Spotify-App-Version": "8.6.72",
        "X-Client-Id": utils.generate_random_string(32)
    }
    
    payload = {
    "creation_point": "client_mobile",
    "gender": "male" if random.randint(0, 1) else "female",
    "birth_year": random.randint(1990, 2000),
    "displayname": user['user'],
    "iagree": "true",
    "birth_month": random.randint(1, 11),
    "password_repeat": user['pass'],
    "password": user['pass'],
    "key": "142b583129b2df829de3656f9eb484e6",
    "platform": "Android-ARM",
    "email": user['email'],
    "birth_day": random.randint(1, 20)
    }

    r = requests.post('https://spclient.wg.spotify.com/signup/public/v1/account/', headers=headers, data=payload, proxies={"http": user['proxy']['ip']})
    time.sleep(random.randint(3, 5))

    if r.status_code==200:
        if r.json()['status']==1:
            return True, time.time()
        else:
            False, time.time()
    else:
        print(">> Spotify account failed initialization - 400")
        False, time.time()

def initialize(user):
    chrome_options = webdriver.ChromeOptions()          

    chrome_options.add_argument('--proxy-server=%s' % user['proxy']['ip'])                  # Assigns proxy
    #chrome_options.add_argument('--headless')                                             # Specifies GUI display, set to headless (NOGUI)
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_experimental_option("excludeSwitches", ["disable-popup-blocking"])   # Disable pop-ups? maybe?
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])           # Disable all logging        

    print(">>\tLogging into Spotify...")
    # Builds corresponding URL to proxy host location
    url = "https://accounts.spotify.com/" + user['proxy']['country'].lower() + "/login"


    web = webdriver.Chrome(executable_path=r"src/resources/webdriver/chromedriver.exe", options=chrome_options)
    # Open Spotify login URL
    web.get(url)   
    time.sleep(random.randint(random.randint(3, 4), random.randint(6, 10)))  
    
    print(">>\tFilling Credentials...")
    # Input login credentials
    a = web.find_element(By.XPATH, "//*[@id='login-username']")
    a.send_keys(user['email'])
    time.sleep(random.randint(random.randint(3, 4), random.randint(6, 10))) 
    
    a = web.find_element(By.XPATH, "//*[@id='login-password']")
    a.send_keys(user['pass'])
    time.sleep(random.randint(random.randint(3, 4), random.randint(6, 10))) 
    
    print(">>\tAttempting to login...")
    a = web.find_element(By.XPATH, "//*[@id='login-button']")
    a.click()
    time.sleep(random.randint(random.randint(3, 4), random.randint(6, 10))) 

    # Handles login errors
    if elementExists(web, "//div[@data-testid='login-container']/div[@role='alert']"):
        errormessage = web.find_element(By.XPATH, "//div[@data-testid='login-container']/div[@role='alert']/span/p").text   
        print(">>\t" + utils.bcolors.FAIL + "ERROR: Login failed \"" + errormessage.removesuffix('.') + "\". Shutting down." + utils.bcolors.ENDC)
        return False, time.time()
    else:
        print(">>\tLoading webplayer...")
        # Click Webplayer option
        a = web.find_element(By.XPATH, "//*[@id='root']/div/div[2]/div/div/button[2]")
        a.click()
        time.sleep(random.randint(random.randint(3, 4), random.randint(6, 10))) 

        time.sleep(180)
        try:
            print(">>\tAttempting to gather cookies")
            utils.makedir("src/resources/cookies/")
            cookie_dir = "src/resources/cookies/" + user['user'] + ".pk1"
            pickle.dump(web.get_cookies(), open(cookie_dir, "wb"))
            print(">>\tCookies successfully stored")
        except:
            print(">>\tFailed to gather cookies")

    web.quit()    
    return True, time.time()    

def elementExists(web, xpath):
    try:
        web.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        time.sleep(random.randint(random.randint(3, 4), random.randint(6, 10))) 
        return False
    time.sleep(random.randint(random.randint(3, 4), random.randint(6, 10)))     
    return True   

def main():
    record = utils.startProcess()
    valid = False

    while not valid:
        try:
            amount = input(">>\n>> Spoticry Account Tool v0.0.2\n>> How many accounts do you wish to create? : ")
            amount = int(amount)
            valid = True
        except ValueError as VE:
            print(">> " + utils.bcolors.WARNING + "WARNING: Error converting input. Please provide a valid input" + utils.bcolors.ENDC)    

    for i in range(amount):
        print(">>\n>> Generating new user...")

        # Random elements initialized
        password_length = random.randint(8, 16)
        domain_index = random.randint(0, 9)
        dob_month = random.randint(1, 11)
        dob_day = random.randint(1, 28)
        dob_year = random.randint(1982, 2006)

        # Generate spotifyUser data
        # Generate temp email address and email MD5 hash token
        email = utils.generate_email(domain_index)

        # Generate random username
        username = utils.generate_username()
        # Generate random password
        password = utils.generate_password(password_length)
        # Generate random birthday
        birthday = utils.generate_birthday(dob_month, dob_day, dob_year)
        # Generate random gender selection
        gender = random.randint(0, 2)
        # Generate random response to marketing infomation
        marketing_info = random.randint(0, 1)
        # Generate random proxy from list of scraped proxies
        proxy_info = utils.get_proxy()

        print(">> Credentials for " + username + " generated")

        # Create email user in AWS
        print(">> Initializing email in AWS WorkMail...")
        resp = utils.create_email(username, password, email)

        # Create spotifyUser dictionary
        newUser = {
            "email": email,
            "user": username,
            "pass": password,
            "dob": {
                "day": birthday.day,
                "month": birthday.month,
                "year": birthday.year
            },
           "gender": gender,
            "opt_in": marketing_info,
            "proxy": proxy_info,
            "created": {
                "status": '',
                "date": ''
            },
            "verified": {
                "status": '',
                "date": ''
            }
        }

            
        # Send credentials to sign-up page using webdriver
        print(">> Verifying user...")
        status, date = request(newUser)
        newUser["created"]["status"] = status
        newUser["created"]["date"] = date

        # Login to create cookie file and verify user existence
        print(">> Initializing user...")
        status, date = initialize(newUser)
        newUser["verified"]["status"] = status
        newUser["verified"]["date"] = date

        # Print generated user to JSON file
        time.sleep(180)
        if status == True:
            utils.create_user(newUser)
            print(">> " + utils.bcolors.BOLD + "User " + newUser["user"] + " successfully generated" + utils.bcolors.ENDC)
        else:
            print(">> " + utils.bcolors.FAIL + utils.bcolors.BOLD + "User " + newUser["user"] + " generation failed" + utils.bcolors.ENDC)

    
    print(">>\n>> " + utils.bcolors.OKGREEN + utils.bcolors.BOLD + str(amount) + " users successfully generated. Closing..." + utils.bcolors.ENDC + "\n")
    utils.peakMemory(record)


if __name__ == "__main__":
    main()
