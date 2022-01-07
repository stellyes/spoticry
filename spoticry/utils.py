import os
import time
import json
import errno
import socket
import string
import random
import urllib
import shutil
import pathlib
import requests

SUPPORTED_REGIONS = ["AD", "AR", "AS", "AT", "BE", "BO", "BR", "BG",
                     "CA", "CL", "CO", "CR", "CY", "CZ", "DK", "DO",
                     "EC", "SV", "EE", "FI", "FR", "DE", "GR", "GT",
                     "HN", "HU", "IS", "IN", "ID", "IE", "IL", "IT",
                     "JP", "LV", "LI", "LT", "LU", "MY", "MT", "MX",
                     "MC", "NL", "NZ", "NI", "NO", "PA", "PY", "PE",
                     "PH", "PL", "PT", "RO", "RU", "SA", "SG", "SK",
                     "ZA", "KR", "ES", "SE", "CH", "TW", "TH", "TR",
                     "AE", "UK", "US", "UY", "VN"]

# Sign up URLs for each country supported by Spotify
SIGN_UP_URL_AD = 'https://www.spotify.com/ad/signup'    # Andorra
SIGN_UP_URL_AR = 'https://www.spotify.com/ar/signup'    # Argentina
SIGN_UP_URL_AS = 'https://www.spotify.com/as/signup'    # Australia
SIGN_UP_URL_AT = 'https://www.spotify.com/at/signup'    # Austria
SIGN_UP_URL_BE = 'https://www.spotify.com/be/signup'    # Belgium
SIGN_UP_URL_BO = 'https://www.spotify.com/bo/signup'    # Bolivia
SIGN_UP_URL_BR = 'https://www.spotify.com/br/signup'    # Brazil
SIGN_UP_URL_BG = 'https://www.spotify.com/bg/signup'    # Bulgaria
SIGN_UP_URL_CA = 'https://www.spotify.com/ca/signup'    # Canada
SIGN_UP_URL_CL = 'https://www.spotify.com/cl/signup'    # Chile
SIGN_UP_URL_CO = 'https://www.spotify.com/co/signup'    # Colombia
SIGN_UP_URL_CR = 'https://www.spotify.com/cr/signup'    # Costa Rica
SIGN_UP_URL_CY = 'https://www.spotify.com/cy/signup'    # Cyprus
SIGN_UP_URL_CZ = 'https://www.spotify.com/cz/signup'    # Czech Republic
SIGN_UP_URL_DK = 'https://www.spotify.com/dk/signup'    # Denmark
SIGN_UP_URL_DO = 'https://www.spotify.com/do/signup'    # Dominican Republic
SIGN_UP_URL_EC = 'https://www.spotify.com/ec/signup'    # Ecuador
SIGN_UP_URL_SV = 'https://www.spotify.com/sv/signup'    # El Salvador
SIGN_UP_URL_EE = 'https://www.spotify.com/ee/signup'    # Ecuador
SIGN_UP_URL_FI = 'https://www.spotify.com/fi/signup'    # Finland
SIGN_UP_URL_FR = 'https://www.spotify.com/fr/signup'    # France
SIGN_UP_URL_DE = 'https://www.spotify.com/de/signup'    # Germany
SIGN_UP_URL_GR = 'https://www.spotify.com/gr/signup'    # Greece
SIGN_UP_URL_GT = 'https://www.spotify.com/gt/signup'    # Guatemala
SIGN_UP_URL_HN = 'https://www.spotify.com/hn/signup'    # Honduras
SIGN_UP_URL_HU = 'https://www.spotify.com/hu/signup'    # Hungary
SIGN_UP_URL_IS = 'https://www.spotify.com/is/signup'    # Iceland
SIGN_UP_URL_IN = 'https://www.spotify.com/in/signup'    # India
SIGN_UP_URL_ID = 'https://www.spotify.com/id/signup'    # Indonesia
SIGN_UP_URL_IE = 'https://www.spotify.com/ie/signup'    # Ireland
SIGN_UP_URL_IL = 'https://www.spotify.com/il/signup'    # Israel
SIGN_UP_URL_IT = 'https://www.spotify.com/it/signup'    # Italy
SIGN_UP_URL_JP = 'https://www.spotify.com/jp/signup'    # Japan
SIGN_UP_URL_LV = 'https://www.spotify.com/lv/signup'    # Latvia
SIGN_UP_URL_LI = 'https://www.spotify.com/li/signup'    # Liechtenstein
SIGN_UP_URL_LT = 'https://www.spotify.com/lt/signup'    # Lithuania
SIGN_UP_URL_LU = 'https://www.spotify.com/lu/signup'    # Luxembourg
SIGN_UP_URL_MY = 'https://www.spotify.com/my/signup'    # Malaysia
SIGN_UP_URL_MT = 'https://www.spotify.com/mt/signup'    # Malta
SIGN_UP_URL_MX = 'https://www.spotify.com/mx/signup'    # Mexico
SIGN_UP_URL_MC = 'https://www.spotify.com/mc/signup'    # Monaco
SIGN_UP_URL_NL = 'https://www.spotify.com/nl/signup'    # Netherlands
SIGN_UP_URL_NZ = 'https://www.spotify.com/nz/signup'    # New Zealand
SIGN_UP_URL_NI = 'https://www.spotify.com/ni/signup'    # Nicaragua
SIGN_UP_URL_NO = 'https://www.spotify.com/no/signup'    # Norway
SIGN_UP_URL_PA = 'https://www.spotify.com/pa/signup'    # Panama
SIGN_UP_URL_PY = 'https://www.spotify.com/py/signup'    # Paraguay
SIGN_UP_URL_PE = 'https://www.spotify.com/pe/signup'    # Peru
SIGN_UP_URL_PH = 'https://www.spotify.com/ph/signup'    # Philippines
SIGN_UP_URL_PL = 'https://www.spotify.com/pl/signup'    # Poland
SIGN_UP_URL_PT = 'https://www.spotify.com/pt/signup'    # Portugal
SIGN_UP_URL_RO = 'https://www.spotify.com/ro/signup'    # Romania
SIGN_UP_URL_RU = 'https://www.spotify.com/ru/signup'    # Russia
SIGN_UP_URL_SA = 'https://www.spotify.com/sa/signup'    # Saudi Arabia
SIGN_UP_URL_SG = 'https://www.spotify.com/sg/signup'    # Singapore
SIGN_UP_URL_SK = 'https://www.spotify.com/sk/signup'    # Slovakia
SIGN_UP_URL_ZA = 'https://www.spotify.com/za/signup'    # South Africa
SIGN_UP_URL_KR = 'https://www.spotify.com/kr/signup'    # South Korea
SIGN_UP_URL_ES = 'https://www.spotify.com/es/signup'    # Spain
SIGN_UP_URL_SE = 'https://www.spotify.com/se/signup'    # Sweden
SIGN_UP_URL_CH = 'https://www.spotify.com/ch/signup'    # Switzerland
SIGN_UP_URL_TW = 'https://www.spotify.com/tw/signup'    # Taiwan
SIGN_UP_URL_TH = 'https://www.spotify.com/th/signup'    # Thailand
SIGN_UP_URL_TR = 'https://www.spotify.com/tr/signup'    # Turkey
SIGN_UP_URL_AE = 'https://www.spotify.com/ae/signup'    # United Arab Emirates
SIGN_UP_URL_UK = 'https://www.spotify.com/uk/signup'    # United Kingdom
SIGN_UP_URL_US = 'https://www.spotify.com/us/signup'    # United States
SIGN_UP_URL_UY = 'https://www.spotify.com/uy/signup'    # Uruguay
SIGN_UP_URL_VN = 'https://www.spotify.com/vn/signup'    # Vietnam

# Written out for profile generation and webdriver input
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

# Webdriver information
WEBDRIVER = 'src/webdriver/chromedriver.exe'
PROXYLIST = "src/webdriver/proxy.json"
PROXYFARM = "https://proxylist.geonode.com/api/proxy-list?limit=200&page=1&sort_by=lastChecked&sort_type=desc&speed=fast"


class dob:
    def __init__(self, month, day, year):
        self.month = month
        self.day = day
        self.year = year


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

    month = MONTHS[dob_month]
    birthday = dob(month, dob_day, dob_year)
    return birthday


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


def update_proxy_list():
    '''
    Grabs proxy list from latest update on genode.com
    List updates every ten minutes, if proxy.txt is
    older than 10 minutes
    '''

    # Delete old version of proxies.json
    if os.path.exists(PROXYLIST):
        os.remove(PROXYLIST)

    # Create new version of proxies.json, offload parsed proxies into proxy.txt
    with open(PROXYLIST, "a+") as proxies:
        r = requests.get(PROXYFARM)                 # Pull data from webpage
        html = r.text                               # Convert data to string
        data = json.loads(html)                     # Load string as JSON
        proxies.write(json.dumps(data, indent=4))   # Write to file       
    
    # Parse and print proxy dictionary object to file
    with open(PROXYLIST, "r") as proxies:
        data_json = json.load(proxies)              # Load JSON data
        data = data_json["data"]                    # Indicate parent to iterate
        for data in data:                                          
            if  data['country'] in SUPPORTED_REGIONS:             # Check to see if proxy is from banned country  
                path = 'src/webdriver/sign_up/' + data['country'] + "/"     
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
    Checks if PROXYLIST is up to date, pulls new proxies if file outdated
    '''

    # If proxy file does not exist, creates proxy.json
    if not os.path.isdir(PROXYLIST):
        try:
            update_proxy_list()
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    # Modified time and current time of proxy.txt            
    last_modified = os.path.getctime(PROXYLIST)
    current_time = time.time()
    timedelta = current_time - last_modified

    # Execute update of file if proxies outdated
    if timedelta > 600:
        print(">>\t Proxy list outdated. Grabbing latest proxy list")
        clear_proxies()
        update_proxy_list()


def test_connection(protocol, proxy):
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
        proxy_handler = urllib.request.ProxyHandler({protocol: proxy})
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
    path = os.path.join(root + country)

    if not (os.path.isdir(path)):
        makedir(root)

    # Random choice in provided path
    proxyfile = path + '/' + random.choice(os.listdir(path))

    # Convert JSON file to JSON object
    with open(proxyfile, "r") as doc:
        obj = json.loads(doc.read())

    return obj 