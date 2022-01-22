import os
import sys
import time
import json
import errno
import boto3
import socket
import string
import random
import urllib
import shutil
import pathlib
import requests
import datetime

from requests import HTTPError 


# Supported regions for Spotify
SUPPORTED_REGIONS = ["AD", "AR", "AS", "AT", "BE", "BO", "BR", "BG",
                     "CA", "CL", "CO", "CR", "CY", "CZ", "DK", "DO",
                     "EC", "SV", "EE", "FI", "FR", "DE", "GR", "GT",
                     "HN", "HU", "IS", "IN", "ID", "IE", "IL", "IT",
                     "JP", "LV", "LI", "LT", "LU", "MY", "MT", "MX",
                     "MC", "NL", "NZ", "NI", "NO", "PA", "PY", "PE",
                     "PH", "PL", "PT", "RO", "RU", "SA", "SG", "SK",
                     "ZA", "KR", "ES", "SE", "CH", "TW", "TH", "TR",
                     "AE", "UK", "US", "UY", "VN"]

WEBMAIL_ORG_ID = 'm-32a11f6f87e54cb0b1756a5a6b963f5f'
WEBDRIVER = 'src/webdriver/chromedriver.exe'
REGION = 'us-west-2'


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class dob:
    def __init__(self, month, day, year):
        self.month = month
        self.day = day
        self.year = year


def makedir(path):
    '''
    Creates directory does not exist
    '''   

    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise


# Returns aboslute path of file from relative path
def absolutePath(relativePath):
    return os.path.abspath(relativePath)


def count(path):
    '''
    Counts files in subdirectory
    '''

    nof = 0   # Number of files in output directory

    # Count number of JSON files in directory
    if os.path.isdir(path):
        for path in pathlib.Path(path).iterdir():
            if path.is_file():
                nof += 1 
    else:
        makedir(path)            

    return nof 


def get_sitemap():
    # XPATH Storage Object
    f = open('src/siteconfig.json')
    sitemap = json.load(f)
    f.close()
    return sitemap


def select_entry(filename):
    '''
    Selects random string from random line in text document
    '''

    with open(filename, "r") as doc:
        text = doc.read()
        words = list(map(str, text.split()))
    doc.close()
    return random.choice(words)


def generate_random_string(length): 
    '''
    Generates random string letters and numbers inclusive
    '''

    pool=string.ascii_lowercase+string.digits
    return "".join(random.choice(pool) for i in range(length))


def generate_random_text(length):
    '''
    Generates random string exclusively characters
    '''

    return "".join(random.choice(string.ascii_lowercase) for i in range(length))


def generate_password(length):
    '''
    Random password generator of length provided
    '''

    charset = string.ascii_letters + string.digits + string.punctuation
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
    '''
    Generates email address
    '''

    # Generate random string for email
    base_string = generate_username()

    email = base_string + '@rengland.org'

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

    root = 'src/proxies/'  
    file = random.choice(os.listdir(root))                   
    country = root + file
    proxy = select_entry(country)

    return { "ip": proxy, "country": file.removesuffix('.txt') } 


def update_records(data):
    '''
    Updates JSON records with aggregated, generated user infomration
    '''

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
    zf = num.zfill(6)
    export = 'src/json/' + zf + '.json'    # Path to account JSON file

    try:
        with open(export, 'x') as x:
            json.dump(data, x, indent=4)
    except:
        print("\n>>> ERROR\n>>> Could not create JSON file\n")  


def fetch_image(amount):
    '''
    Generates requested amount of images
    '''

    APIKEY = '075fc857-3a70-4fd8-a129-ba1cf2e62335'

    with open("src/txt/words.txt", "r") as words:
        for i in range(amount):
            try:
                case = select_entry("src/txt/words.txt")
                
                # Many thanks to DeepAI for this beautiful AI model, and also
                # making it free to use (for the most part)
                #
                # See more here: https://deepai.org/machine-learning-model/text2img

                r = requests.post(
                    "https://api.deepai.org/api/text2img",
                    files={
                        'text': case,
                    },
                    headers={
                        'api-key': APIKEY
                    }
                )

                # Check if API request passed
                try:
                    r.raise_for_status()
                except HTTPError as http_err:
                    print(f'HTTP request failed: {http_err}')

                print(">> Image successfully generated using \'" + case + "\'.")

                # Generate unique, timestamped file name for image
                makedir('src/img')
                gen_filename = 'src/img/image' + datetime.datetime.now().strftime("%d%m%Y%H%M%S") + '.jpg'

                # Parse JSON stream and write to image file
                url = r.json().get('output_url')
                image = requests.get(url, stream=True)
                image.raw.decode_content = True
                with open(gen_filename, 'wb') as i:
                    shutil.copyfileobj(image.raw, i)

                print('Image successfully saved:\n\t >> ' + gen_filename)
            except HTTPError as http_err:
                print(f'HTTP error occured: {http_err}')
            except Exception as err:
                print(f'Other error occured during image fetch: {err}')

            
    words.close()
    return gen_filename              


def create_email(username, password):

    # Initialize AWS WorkMail Client
    client = boto3.client('workmail', region_name=REGION)

    try:
        # Create new email user
        print(client.create_user(
            OrganizationId = WEBMAIL_ORG_ID, 
            Name = username,
            DisplayName = username,
            Password = password
        ))

        return True
    except:

        print(">> " + bcolors.FAIL + "FATAL ERROR: Failed to initialize email for user " + username + ". Shutting down..." + bcolors.ENDC)   
        return False