import os
import time
import json
import errno
import random
import socket
import shutil
import pathlib
import requests
import urllib.request
import urllib.error

PROXYLIST = "src/webdriver/proxy.json"
PROXYFARM = "https://proxylist.geonode.com/api/proxy-list?limit=200&page=1&sort_by=speed&sort_type=asc&protocols=https%2Csocks4%2Csocks5&anonymityLevel=elite&anonymityLevel=anonymous"
BANNED_LOCATIONS = ["--", "HK", "CN"]


def test_connection(proxy):
    try:
        proxy_handler = urllib.request.ProxyHandler({'http': proxy})
        opener = urllib.request.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        req = urllib.request.Request('https://deoautemnihil.bandcamp.com/')
        sock = urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        print('>> ERROR: ', e.code)
        return e.code
    except Exception as detail:
        print('>> ERROR: ', detail)
        return True
    return False            


def check(proxy):
    socket.setdefaulttimeout(120)

    if test_connection(proxy):
        print('>>\tERROR:\n>>\tPROXY: ' + proxy + '\n>>\tExpired proxy. Updating list.')
        update()
    else:
        print('>> Proxy connection successful')    

def update():
    # Grabs proxy list from latest update on genode.com
    # List updates every ten minutes, if proxy.txt is
    # older than 10 minutes

    # Delete old version of proxies.json
    if os.path.exists(PROXYLIST):
        os.remove(PROXYLIST)

    # Create new version of proxies.json, offload parsed proxies into proxy.txt
    with open(PROXYLIST, "a+") as proxies:
        r = requests.get(PROXYFARM)                 # Pull data from webpage
        html = r.text                               # Convert data to string
        data = json.loads(html)                     # Load string as JSON
        proxies.write(json.dumps(data, indent=4))   # Write to file 

    # Creates directory if proxy folder does note exist
    if not os.path.exists('src/webdriver/proxies'):
        try:
            os.makedirs('src/webdriver/proxies')
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    # Creates directory if banned proxy folder does note exist
    # Folder exists for debugging purposes
    if not os.path.exists('src/webdriver/banned_proxies'):
        try:
            os.makedirs('src/webdriver/banned_proxies')
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise        

    __nof = 0   # Number of files in output directory

    # Count number of JSON files in directory
    for path in pathlib.Path("src/webdriver/proxies").iterdir():
        if path.is_file():
            __nof += 1  

    # Parse and print proxy dictionary object to file
    with open(PROXYLIST, "r") as proxies:
        data_json = json.load(proxies)              # Load JSON data
        data = data_json["data"]                    # Indicate parent to iterate
        for data in data:                                          
            if not data['country'] in BANNED_LOCATIONS:             # Check to see if proxy is from banned country  
                num = str(__nof)                                    # Convert file counter to str for file name
                zf = num.zfill(8)                                   # proxy number prepended with fixed number of zeros
                export = 'src/webdriver/proxies/' + zf + '.json'    # Path to account JSON file    
                
                ip = str(data['ip'] + ":" + data['port'])                       # Render IP
                country = str(data['country'])                                  # Render country code
                protocol = str(data['protocols'])[1:-1].lstrip("'").rstrip("'") # Render protocol
                
                # Create proxy object
                proxy = {
                    "ip": ip,
                    "country": country,
                    "protocol": protocol
                }                    
                
                with open(export, 'x') as x:
                        json.dump(proxy, x, indent=4)
            else:
                num = str(__nof)                                            # Convert file counter to str for file name
                zf = num.zfill(4)                                           # proxy number prepended with fixed number of zeros
                export = 'src/webdriver/banned_proxies/' + zf + '.json'     # Path to account JSON file    
                
                ip = str(data['ip'] + ":" + data['port'])                       # Render IP
                country = str(data['country'])                                  # Render country code
                protocol = str(data['protocols'])[1:-1].lstrip("'").rstrip("'") # Render protocol
                
                # Create proxy object
                proxy = {
                    "ip": ip,
                    "country": country,
                    "protocol": protocol
                }                    
                
                with open(export, 'x') as x:
                        json.dump(proxy, x, indent=4)

            __nof += 1                  


def get():
    # Checks if proxylist is up to date, pulls new proxies if file outdated

    # If proxy file does not exist, creates proxy.txt
    if not os.path.exists(PROXYLIST):
        try:
            update()
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    # Modified time and current time of proxy.txt            
    last_modified = os.path.getmtime(PROXYLIST)
    current_time = time.time()

    # Execute update of file if proxies outdated
    if (current_time - last_modified) > 600:
        print(">> Proxy list outdated. Grabbing latest proxy list")
        
        # Remove all files and directories associated with old list
        try:
            shutil.rmtree('src/webdriver/banned_proxies')
            shutil.rmtree('src/webdriver/proxies')
            os.remove('src/webdriver/proxy.json')
        except OSError as e:
            print(">> ERROR: " + e.strerror)

        update()

    # Pick random file in directorty
    proxyfile = 'src/webdriver/proxies/' + random.choice(os.listdir('src/webdriver/proxies'))

    with open(proxyfile, "r") as doc:
        obj = json.loads(doc.read())

    return obj 