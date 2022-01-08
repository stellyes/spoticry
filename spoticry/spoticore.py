import os
import sys
import json
import time
import utils
import errno
import shutil
import random
import urllib
import socket
import pathlib
import requests
import datetime
import threading

from requests import HTTPError 


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


def update_proxy_list():
    '''
    Grabs proxy list from latest update on genode.com
    List updates every ten minutes, if proxy.txt is
    older than 10 minutes
    '''

    # Delete old version of proxies.json
    if os.path.exists(utils.PROXYLIST):
        os.remove(utils.PROXYLIST)

    # Create new version of proxies.json, offload parsed proxies into proxy.txt
    with open(utils.PROXYLIST, "a+") as proxies:
        r = requests.get(utils.PROXYFARM)                 # Pull data from webpage
        html = r.text                               # Convert data to string
        data = json.loads(html)                     # Load string as JSON
        proxies.write(json.dumps(data, indent=4))   # Write to file       
    
    # Parse and print proxy dictionary object to file
    with open(utils.PROXYLIST, "r") as proxies:
        data_json = json.load(proxies)              # Load JSON data
        data = data_json["data"]                    # Indicate parent to iterate
        for data in data:                                          
            if  data['country'] in utils.SUPPORTD_REGIONS:             # Check to see if proxy is from banned country  
                path = 'src/webdriver/sign_up/' + data['country'] + "/proxies/"     
                makedir(path)                                                   
                nof = utils.count(path)                                                       # Count files in output directory
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
    Checks if utils.PROXYLIST is up to date, pulls new proxies if file outdated
    '''

    # If proxy file does not exist, creates proxy.txt
    if not os.path.exists(utils.PROXYLIST):
        try:
            update_proxy_list()
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    # Modified time and current time of proxy.txt            
    last_modified = os.path.getmtime(utils.PROXYLIST)
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
        proxies = 'src/webdriver/sign_up/' + directory

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

    utils.get_proxy_list()

    root = 'src/webdriver/sign_up/'

    # Creates parent directory for individual country folders
    if not (os.path.isdir(root)):
        utils.makedir(root)

    directories = os.listdir(root)                      # 
    country = random.choice(directories)
    path = os.path.join(root + country)

    if not (os.path.isdir(path)):
        utils.makedir(root)

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