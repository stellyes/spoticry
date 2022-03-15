import os
import sys
import time
import json
import math
import errno
import boto3
import socket
import string
import random
import urllib
import shutil
import psutil
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
WEBDRIVER = 'src/resources/webdriver/chromedriver.exe'
REGION = 'us-west-2'

BL_CHAR = ["/", chr(92),  '"', '.', '<', '>', ':', '?', '*']
RP_CHAR = ["_fs_", '_bs_', '_qt_', '_p_', '_lb_', "_rb_", '_col_', '_q_', '_star_']

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

# Returns random timedelta for automating loops
def randomTimeDelta(minutes_low, minutes_high):
    return time.time() + (60 * random.randint(minutes_low, minutes_high))

def updateJSON(file, data):
    try:
        if os.path.exists(file):
            os.remove(file)

        with open(file, 'x') as filename:
            json.dumps(data, filename, indent=4)    
        return True
    except:
        print(">>\t" + bcolors.FAIL + "ERROR: Unable to update JSON file" + bcolors.ENDC)
        return False


def cleanInput(name):
    i = 0
    for character in BL_CHAR:
        name = name.replace(BL_CHAR[i], RP_CHAR[i])
        i += 1
    return name    

# Initializes recording feature in psutil library
def startProcess(): 
    return psutil.Process()

# Prints peak memory usage during script, converts to proper size abbreviation
def peakMemory(process):
    size_bytes = process.memory_info().peak_wset
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    result = "PEAK MEMORY USAGE: %s %s" % (s, size_name[i])
    print(">> " + bcolors.BOLD + bcolors.OKBLUE + result + bcolors.ENDC) 

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

def get_useragents():
    # User agent storage object
    f = open("src/useragent.json")
    useragents = json.load(f)
    f.close()
    return useragents    

# Returns odds out of 100, dice roll
def chance(odds):
    return True if random.randint(1, 100) <= odds else False    


def selectPriority(**debug):
    '''
    Uses weighted priority scale to determine which object of priority/5 gets chosen
    '''
    if debug == 1:
        return random.choice(seq=["1", "2", "3", "5", "5"], cum_weights=(5, 15, 35, 65, 100))

    return random.choice(seq=["1", "2", "3", "4", "5"], cum_weights=(5, 15, 35, 65, 100))     


def select_entry(filename):
    '''
    Selects random string from random line in text document
    '''

    with open(filename, "r") as doc:
        text = doc.read()
        words = list(map(str, text.split()))
    doc.close()
    return random.choice(words)

def select_file(filepath):
    '''
    Function: Selects random file from given folder path
    Returns: String - Absolute path to selected file
    '''    
    try:
        return absolutePath(filepath)
    except:
        raise Exception(">> " + bcolors.FAIL + "ERROR: File selection failed. Shutting down..." + bcolors.ENDC)   


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
            op1 = select_entry("src/resources/txt/fname.txt")
            username = username + op1
        elif username_order == 2:
            markers[2] = 1
            op2 = select_entry("src/resources/txt/lname.txt")
            username = username + op2
        elif username_order == 3:
            markers[3] = 1
            op3 = select_entry("src/resources/txt/words.txt")

            # If length of string is unreasonably long, reselect
            while len(op3) > 8:
                op3 = select_entry("src/resources/txt/words.txt")
            username = username + op3

    return username


def generate_email(domain_index):
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

    root = 'src/resources/proxies/'  
    file = random.choice(os.listdir(root))                   
    country = root + file
    proxy = select_entry(country)
    parsed_country = country.removesuffix(".txt").removeprefix("src/resources/proxies/")

    return { "ip": proxy, "country": parsed_country } # file.removesuffix('.txt')


def create_user(data):
    '''
    Updates JSON records with aggregated, generated user information
    '''

    __dir = os.path.join('src/resources/users/inactive/')      # JSON output directory

    # Creates directory if __dir does note exist
    if not os.path.exists(__dir):
        try:
            os.makedirs(__dir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
    
    export = __dir + data['user'] + '.json'    # Path to account JSON file

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

    with open("src/resources/txt/words.txt", "r") as words:
        for i in range(amount):
            try:
                case = select_entry("src/resources/txt/words.txt")
                
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
                makedir('src/resources/img')
                gen_filename = 'src/resources/img/image' + datetime.datetime.now().strftime("%d%m%Y%H%M%S") + '.jpg'

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