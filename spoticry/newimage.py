# Special thanks to Desi Quintans for the giant list of nouns.
# desiquintans.com/nounlist
# 
# This noun list makes the first 6801 lines of the nouns.txt file.
#
# The remaining few thousand lines of words came from the following site:
# http://www.mieliestronk.com/corncob_lowercase.txt


import sys
import shutil
import datetime
import requests
from requests import HTTPError

APIKEY = '075fc857-3a70-4fd8-a129-ba1cf2e62335'
MAXIMUM_IMG_COUNT = 64911
sysout = sys.stdout


def main():
    REQ_AMT = 25
    x = 0

    #if REQ_AMT > MAXIMUM_IMG_COUNT:
    #    print(">>> Maximum requested images exceeded. Defaulting to max value.")
    #    REQ_AMT = MAXIMUM_IMG_COUNT

    with open("src/txt/words.txt", "r") as words:
        for line in words:
            if x < REQ_AMT:
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
                            'api-key': '075fc857-3a70-4fd8-a129-ba1cf2e62335'}
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

                x += 1
            else:
                break
            
        words.close()      


if __name__ == "__main__":
    main()
