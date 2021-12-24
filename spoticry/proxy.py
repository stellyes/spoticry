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

import spoticore

PROXYLIST = "src/webdriver/proxy.json"
PROXYFARM = "https://proxylist.geonode.com/api/proxy-list?limit=200&page=1&sort_by=lastChecked&sort_type=desc&speed=fast"
BANNED_LOCATIONS = ["--", "HK", "CN"]


def test_connection(proxy):
    try:
        proxy_handler = urllib.request.ProxyHandler({'http': proxy})
        opener = urllib.request.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        req = urllib.request.Request('https://deoautemnihil.bandcamp.com/')
        urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        print('>> ERROR: ', e.code)
        return e.code
    except Exception as detail:
        print('>> ERROR: ', detail)
        return True
    return False            


def check(proxy):

    # Status Codes:
    #   0 = Uninitialized
    #   1 = Failed
    #   2 = Success
    #   3 = Debug

    statuscode = 0
    socket.setdefaulttimeout(120)

    if test_connection(proxy):
        statuscode = 1
        print('>>\tERROR:\n>>\tPROXY: ' + proxy + '\n>>\tExpired proxy. Updating list.')
    else:
        print('>>\t Proxy connection successful') 
        statuscode = 2

    return statuscode   

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
    


    # Parse and print proxy dictionary object to file
    with open(PROXYLIST, "r") as proxies:
        data_json = json.load(proxies)              # Load JSON data
        data = data_json["data"]                    # Indicate parent to iterate
        for data in data:                                          
            if not data['country'] in BANNED_LOCATIONS:             # Check to see if proxy is from banned country  
                path = 'src/webdriver/sign_up/' + data['country'] + "/proxies/"
                __nof = spoticore.count(path)
                num = str(__nof)                                                        # Convert file counter to str for file name
                zf = num.zfill(4)                                                       # proxy number prepended with fixed number of zeros
                export = path + zf + '.json' # Path to proxy JSON file                    
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
            else:
                path = 'src/webdriver/sign_up/' + data['country'] + "/banned_proxies"
                __nof = spoticore.count(path)
                num = str(__nof)                                                                    # Convert file counter to str for file name
                zf = num.zfill(4)                                                                   # proxy number prepended with fixed number of zeros
                export = path + zf + '.json'      # Path to proxy JSON file    
                
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

            __nof += 1                  


def main():
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
        print(">>\t Proxy list outdated. Grabbing latest proxy list")
        spoticore.clear_proxies()
        update()

     

if __name__ == "__main__":
    main()