import os
import sys
import time
import json
import errno
import string
import shutil
import random
import socket
import urllib
import pathlib
import hashlib
import requests
import datetime
import threading

from bs4 import BeautifulSoup
from requests import HTTPError
from twocaptcha import TwoCaptcha  

import datafy


class pprint:
    def __init__(self, message, bool_resposne, error, success):
        message = self.message
        bool_resposne = self.bool_resposne
        error = self.error
        success = self.success

    def write(self, message):
        print(">> " + message + "...", end="", flush=True)

    def response(self, bool_response, error, success):
        if (bool_response == True):
            print(success)
        else:
            print(error)    


class dob:
    def __init__(self, month, day, year):
        self.month = month
        self.day = day
        self.year = year

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


def random_parameter(r1, r2):
    '''
    Returns random integer in specified range (inclusive)
    Implementation used to clean imports on other files
    '''
    return random.randint(r1, r2)


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
    Generates email address and corresponding MD5 hash of email
    '''

    # Generate random string for email
    base_string = generate_username()
    domain = datafy.DOMAINS[domain_index]

    email = base_string + domain

    # Email MD5 Hash key calculated for Temp Mail API Usage
    email_hash = hashlib.md5(email.encode('utf-8')).hexdigest()
    return email, email_hash


def generate_birthday(dob_month, dob_day, dob_year):
    '''
    Generate complete indexed date-of-birth object
    '''

    month = datafy.MONTHS[dob_month]
    birthday = dob(month, dob_day, dob_year)
    return birthday


def update_records(email_hash, data):
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
        print("\n>>> ERROR\n>>> ID: " + email_hash +
              '\n>>> Could not create JSON file\n')


def update_proxy_list():
    '''
    Grabs proxy list from latest update on genode.com
    List updates every ten minutes, if proxy.txt is
    older than 10 minutes
    '''

    # Delete old version of proxies.json
    if os.path.exists(datafy.PROXYLIST):
        os.remove(datafy.PROXYLIST)

    # Create new version of proxies.json, offload parsed proxies into proxy.txt
    with open(datafy.PROXYLIST, "a+") as proxies:
        r = requests.get(datafy.PROXYFARM)                 # Pull data from webpage
        html = r.text                               # Convert data to string
        data = json.loads(html)                     # Load string as JSON
        proxies.write(json.dumps(data, indent=4))   # Write to file       
    
    # Parse and print proxy dictionary object to file
    with open(datafy.PROXYLIST, "r") as proxies:
        data_json = json.load(proxies)              # Load JSON data
        data = data_json["data"]                    # Indicate parent to iterate
        for data in data:                                          
            if  data['country'] in datafy.SUPPORTD_REGIONS:             # Check to see if proxy is from banned country  
                path = 'src/webdriver/sign_up/' + data['country'] + "/proxies/"     
                makedir(path)                                                   
                nof = count(path)                                                       # Count files in output directory
                num = str(nof)                                                          # Convert file counter to str for file name
                zf = num.zfill(4)                                                       # proxy number prepended with fixed number of zeros
                export = path + zf + '.json'                                            # Path to proxy JSON file    
                                
                ip = str(data['ip'] + ":" + data['port'])                       # Render IP
                country = str(data['country'])                                  # Render country code
                protocol = str(data['protocols'])[1:-1].lstrip("'").rstrip("'") # Render protocol
                
                # Create proxy object
                proxy = {
                    "ip": ip,
                    "country": country,
                    "protocol": protocol
                }                   
                
                with open(export, 'a+') as x:
                        json.dump(proxy, x, indent=4)               

            nof += 1                  


def get_proxy_list():
    '''
    Checks if datafy.PROXYLIST is up to date, pulls new proxies if file outdated
    '''

    # If proxy file does not exist, creates proxy.txt
    if not os.path.exists(datafy.PROXYLIST):
        try:
            update_proxy_list()
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    # Modified time and current time of proxy.txt            
    last_modified = os.path.getmtime(datafy.PROXYLIST)
    current_time = time.time()

    # Execute update of file if proxies outdated
    if (current_time - last_modified) > 600:
        print(">>\t Proxy list outdated. Grabbing latest proxy list")
        clear_proxies()
        update_proxy_list()


def test_connection(proxy):
    '''
    Pings address using selected proxy to test connection

    Status Codes:
       0 = Uninitialized
       1 = Failed
       2 = Success
       3 = Debug
    '''

    statuscode = 0                  
    socket.setdefaulttimeout(120)   # Threshold for testing proxy timeout
    ping = False                    # Results set to false at initialization, changed to true if pinged

    try:
        proxy_handler = urllib.request.ProxyHandler({'http': proxy})
        opener = urllib.request.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        req = urllib.request.Request('https://deoautemnihil.bandcamp.com/')
        ping = True
    except urllib.error.HTTPError as e:
        print('>> ERROR: ', e.code)
        return e.code
    except Exception as detail:
        print(detail) 
    
    if not ping:
        statuscode = 1
        print('>>\tERROR: ' + proxy + ' has expired')
    else:
        print('>>\t Proxy connection successful') 
        statuscode = 2

    return statuscode


def makedir(path):
    '''
    Creates directory if proxy folder does note exist
    '''   

    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise


def clear_proxies():
    '''
    Removes all proxy data from subdirectories
    '''

    # Get subdirectory names associated with each country
    makedir('src/webdriver/sign_up')
    directories = os.listdir('src/webdriver/sign_up')
    
    # Iterate through directories and delete respective proxy data
    for directory in directories:
        proxies = 'src/webdriver/sign_up/' + directory + '/proxies'

        if os.path.isdir(proxies):
            for item in os.scandir(proxies):
                try:
                    shutil.rmtree(item)
                except OSError:
                    os.remove(item)
            shutil.rmtree(proxies)       

    try:
        shutil.rmtree('src/webdriver/proxy.json') 
    except OSError:
        os.remove('src/webdriver/proxy.json')
    

def get_proxy():
    '''
    Pick random proxy file in directorty
    '''

    if not (os.path.exists('src/webdriver/proxy.json')):
        get_proxy_list()
    else:
        clear_proxies()
        update_proxy_list()    

    root = 'src/webdriver/sign_up/'

    # Creates parent directory for individual country folders
    if not (os.path.isdir(root)):
        makedir(root)

    directories = os.listdir(root)                      # 
    country = random.choice(directories)
    path = os.path.join(root + country + '/proxies')

    if not (os.path.isdir(path)):
        makedir(root)

    # Random choice in provided path
    proxyfile = path + '/' + random.choice(os.listdir(path))

    # Convert JSON file to JSON object
    with open(proxyfile, "r") as doc:
        obj = json.loads(doc.read())

    return obj     


def fetch_image(amount):
    '''
    Generates requested amount of images
    '''

    APIKEY = '075fc857-3a70-4fd8-a129-ba1cf2e62335'

    with open("src/txt/words.txt", "r") as words:
        for i in range(amount):
            for line in words:
                try:
                    case = line.strip()
                
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

                    print("Image successfully generated using \'" + case + "\'.")

                    # Generate unique, timestamped file name for image
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