import json
import boto3
import requests

APIKEY = 'k_kVsKS05Xl5TcgdfjUSLlnU0N4ivDr9wf404'

def main(email):
    r = requests.post(
        "https://mailsac.com/api/addresses/" + email + "?_mailsacKey=" + APIKEY,
        headers={
            'forward': "accounts@rengland.org"
        }
    )

    print(r)   