import os
import sys
import time
import json
import errno
import random
import string
import hashlib
import pathlib
import proxy as prox
import verify as verify

months = ['January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December']
domains = ['@mailkept.com', '@promail1.net', '@rcmails.com', '@relxv.com', '@folllo.com',
           '@fortuna7.com', '@invecra.com', '@linodg.com', '@awiners.com', '@subcaro.com']


class dob:
    def __init__(self, month, day, year):
        self.month = month
        self.day = day
        self.year = year


def select_entry(filename):
    # Selects random string from random line in text document

    with open(filename, "r") as doc:
        text = doc.read()
        words = list(map(str, text.split()))
    doc.close()
    return random.choice(words)


def generate_password(length):
    # Random password generator of length provided

    charset = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(charset) for i in range(length))
    return password


def generate_username():
    # Random username generator

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
            op1 = select_entry("src/txt/fname.txt")
            username = username + op1
        elif username_order == 2:
            markers[2] = 1
            op2 = select_entry("src/txt/lname.txt")
            username = username + op2
        elif username_order == 3:
            markers[3] = 1
            op3 = select_entry("src/txt/words.txt")

            # If length of string is unreasonably long, reselect
            while len(op3) > 8:
                op3 = select_entry("src/txt/words.txt")
            username = username + op3

    return username


def generate_email(domain_index):
    # Generates email address and corresponding MD5 hash of email

    # Generate random string for email
    base_string = generate_username()
    domain = domains[domain_index]

    email = base_string + domain

    # Email MD5 Hash key calculated for Temp Mail API Usage
    email_hash = hashlib.md5(email.encode('utf-8')).hexdigest()
    return email, email_hash


def generate_birthday(dob_month, dob_day, dob_year):
    # Generate complete indexed date-of-birth object

    month = months[dob_month]
    birthday = dob(month, dob_day, dob_year)
    return birthday


def update_records(email_hash, data):
    # Updates JSON records with aggregated, generated user infomration

    __dir = os.path.join('src/json')    # JSON output directory
    __nof = 0                           # Number of files in output directory

    # Creates directory if __dir does note exist
    if not os.path.exists(__dir):
        try:
            os.makedirs(__dir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    # Count number of JSON files in directory
    for path in pathlib.Path("src/json").iterdir():
        if path.is_file():
            __nof += 1

    # Convert file counter to str for file name
    num = str(__nof)
    # Account number prepended with fixed number of zeros
    zf = num.zfill(16)
    export = 'src/json/' + zf + '.json'    # Path to account JSON file

    try:
        with open(export, 'x') as x:
            json.dump(data, x, indent=4)
    except:
        print("\n>>> ERROR\n>>> ID: " + email_hash +
              '\n>>> Could not create JSON file\n')


def main():
    amount = 100

    for i in range(amount):
        print("\n>> Generating new user...")

        # Random elements initialized
        password_length = random.randint(8, 16)
        domain_index = random.randint(0, 9)
        dob_month = random.randint(0, 11)
        dob_day = random.randint(1, 28)
        dob_year = random.randint(1982, 2006)

        # Generate spotifyUser data
        # Generate temp email address and email MD5 hash token
        email, email_hash = generate_email(domain_index)
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
        print(">> Fetching proxy information...")
        proxy_info = prox.get()
        print(">> Proxy " + proxy_info['ip'] + " selected")

        # If proxy fails connection, get new proxy value to assign
        print(">>\t Testing connection: " + proxy_info['ip'] + "...")
        while (prox.check(proxy_info['ip']) < 2):
            print(">>\t Testing connection: " + proxy_info['ip'] + "...")
            proxy_info = prox.get()
        

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
            "md5_hash": email_hash,
            "proxy": proxy_info,
            "verified": {
                "status": '',
                "date": ''
            }
        }

        print(">> Credentials for " + newUser["user"] + " generated.")
        time.sleep(random.randint(1, 3))

        # Send credentials to sign-up page using webdriver
        print(">> Verifying user...")
        status, date = verify.sign_up(newUser)


        # Print generated user to JSON file
        update_records(email_hash, newUser)

        print(">> User " + newUser["user"] + " successfully generated\n")


if __name__ == "__main__":
    main()
