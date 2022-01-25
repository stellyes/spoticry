"""
    Legacy functions from utils.py
"""

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