import os
import sys
import time
import errno
import random
import datetime
from selenium import webdriver

PROXYFARM = 'https://sslproxies.org/'
PROXYLIST = 'src/txt/proxy.txt'


def update():
    # Grabs proxy list from latest update on sslproxies.org
    # List updates every ten minutes, if proxy.txt is
    # older than 10 minutes

    op = webdriver.ChromeOptions()      # Options argument initalization
    op.add_argument('--headless')       # Specifies GUI display, set to headless (NOGUI)
    web = webdriver.Chrome(executable_path='src/webdriver/chromedriver.exe', options=op)  # Headless Chrome instance

    ip = '//*[@id="list"]/div/div[2]/div/table/tbody/tr[1]/td[1]'

    raw_list = web.find_element_by_xpath(raw_list_xpath)
    print(raw_list)
    sys.exit()



def main():
    # Checks if proxylist is up to date, pulls new proxies if file outdated

    # If proxy file does not exist, creates proxy.txt
    if not os.path.exists(PROXYLIST):
        try:
            os.makedirs(PROXYLIST)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    # Modified time and current time of proxy.txt            
    last_modified = os.path.getmtime(PROXYLIST)
    current_time = time.time()

    # Execute update of file if proxies outdated
    if (current_time - last_modified) > 600:
        print("\n>>> Proxy list outdated. Grabbing latest proxy list")
        update()

if __name__ == "__main__":
    main()
