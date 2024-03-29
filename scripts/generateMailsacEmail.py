import json
import requests

def lambda_handler(event, context):
    
    r = requests.post(
        "https://mailsac.com/api/addresses/" + event['email'],
        headers={
            "Mailsac-Key": event['apikey'],
            "forward": "accounts@rengland.org"
        }
    )

    if r.status_code == 200:
        print(">> Successfully generated email " + event['email'])
    elif r.status_code == 400:
        print(">> ERROR: Email already reserved to this account or out of API credits")
    elif r.status_code == 401:
        print(">> ERROR: Email already reserved to another account") 
    else:
        print(">> Unknown error occured during email creation")          

    return { "response": r.status_code, "body": json.loads(r.content) }

if __name__ == "__main__":
    lambda_handler({ "apikey": "k_kVsKS05Xl5TcgdfjUSLlnU0N4ivDr9wf404", "email": "lexaprofunfacts394@mailsac.com" }, "Local Environment")