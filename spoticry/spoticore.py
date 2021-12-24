import os
import json
import errno
import shutil
import random
import pathlib
import requests
import datetime

from requests import HTTPError


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
    path = 'src/webdriver/sign_up'
    directories = os.listdir(path)
    
    # Iterate through directories and delete respective proxy data
    for directory in directories:
        proxies = path + '/' + directory + '/proxies'
        banned_proxies = path + '/' + directory + '/banned_proxies'

        if os.path.isdir(proxies):
            for item in os.scandir(proxies):
                file = os.path.join(proxies, item)
                try:
                    shutil.rmtree(file)
                except OSError:
                    os.remove(file)
            shutil.rmtree(proxies)

        if os.path.isdir(banned_proxies):
            for item in os.scandir(banned_proxies):
                file = os.path.join(banned_proxies, item)
                try:
                    shutil.rmtree(file)
                except OSError:
                    os.remove(file) 
            shutil.rmtree(banned_proxies)        

    try:
        shutil.rmtree('src/webdriver/proxy.json') 
    except OSError:
        os.remove('src/webdriver/proxy.json')
    

def get_proxy():
    '''
    Pick random proxy file in directorty
    '''

    root = 'src/webdriver/sign_up'
    directories = os.listdir(root)
    country = random.choice(directories)
    path = os.path.join(root + country + '/proxies')

    # Random choice in provided path
    proxyfile = random.choice(path)

    # Convert JSON file to JSON object
    with open(proxyfile, "r") as doc:
        obj = json.loads(doc.read())

    return obj
    

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
