import os
import time
import json
import string
import random
import requests

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

class dob:
    def __init__(self, month, day, year):
        self.month = month
        self.day = day
        self.year = year

def select_entry(filename):
    '''
    Selects random string from random line in text document
    '''

    with open(filename, "r") as doc:
        text = doc.read()
        words = list(map(str, text.split()))
    doc.close()
    return random.choice(words)

def generate_password(length):
    '''
    Random password generator of length provided
    '''
    charset = string.ascii_letters + string.digits + '!#@&^*()<>?'
    password = ''.join(random.choice(charset) for i in range(length))
    return password

def generate_username():
    '''
    Random username generator
    '''

    markers = [0, 0, 0, 0]          # Markers used to prevent duplicate entries
    op0 = random.randint(0, 99)     # appended numbers to username
    op1 = ''                        # first name options
    op2 = ''                        # last name options
    op3 = ''                        # random word from words list
    username = ''                   # empty username string

    for i in range(2):
        # Get random marker
        username_order = random.randint(0, 3)

        # If marker indicates the choice has already been made
        if (markers[username_order] == 1):
            if username_order == 3:                 # If polled int is 3, wrap around to 0
                username_order = 0
            else:
                username_order = username_order + 1  # If polled int is < 3, increment

        if username_order == 0:
            markers[0] = 1
            username = username + str(op0)
        elif username_order == 1:
            markers[1] = 1
            op1 = select_entry("resources/data/fname.txt")
            username = username + op1
        elif username_order == 2:
            markers[2] = 1
            op2 = select_entry("resources/data/lname.txt")
            username = username + op2
        elif username_order == 3:
            markers[3] = 1
            op3 = select_entry("resources/data/words.txt")

            # If length of string is unreasonably long, reselect
            while len(op3) > 8:
                op3 = select_entry("resources/data/words.txt")
            username = username + op3

    return username    

def generate_email():
    '''
    Generates email address
    '''
    # Generate random string for email
    base_string = generate_username()

    email = base_string + '@mailsac.com'

    return email

def generate_birthday(dob_month, dob_day, dob_year):
    '''
    Generate complete indexed date-of-birth object
    '''
    #month = MONTHS[dob_month]
    return dob(dob_month, dob_day, dob_year)  

def get_proxy():
    '''
    Pick random proxy server in directorty
    '''  

    root = 'resources/proxies/'  
    file = random.choice(os.listdir(root))                   
    country = root + file
    proxy = select_entry(country)
    parsed_country = country.removesuffix(".txt").removeprefix("resources/proxies/")

    return { "ip": proxy, "country": parsed_country } # file.removesuffix('.txt')      

def lambda_handler(event, context):
    print(">>\n>> Generating new user...")

    # Random elements initialized
    password_length = random.randint(8, 16)
    domain_index = random.randint(0, 9)
    dob_month = random.randint(1, 11)
    dob_day = random.randint(1, 28)
    dob_year = random.randint(1982, 2006)

    # Generate spotifyUser data
    # Generate temp email address and email MD5 hash token
    email = generate_email(domain_index)

    # Generate random username
    username = generate_username()
    # Generate random password
    password = generate_password(password_length)
    # Generate random birthday
    birthday = generate_birthday(dob_month, dob_day, dob_year)
    # Generate random gender selection
    gender = random.randint(0, 2)
    # Generate random response to marketing infomation
    marketing_info = random.randint(0, 1)
    # Generate random proxy from list of scraped proxies
    proxy_info = get_proxy()

    print(">> Credentials for " + username + " generated")

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

    if status == True:
        return ({ "response": True, "body": json.dumps(newUser) })
    elif status == False:
        return ({ "response": False, "body": json.dumps('Error in sign-up request for user ' + newUser['username']) })
    else:
        return ({ "response": False, "body": json.dumps("Critical failure in sign-up process") })