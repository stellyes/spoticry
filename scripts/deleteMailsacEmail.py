import json
import requests

def lambda_handler(event, context):
    
    r = requests.delete(
        "https://mailsac.com/api/addresses/" + event['email'],
        headers={
            "Mailsac-Key": event['apikey']
        }
    ) 

    if r.status_code == 200:
        print(">> Successfully deleted email " + event['email'])
    elif r.status_code == 400:
        print(">> ERROR: Email does not exist")
    elif r.status_code == 401:
        print(">> ERROR: Email owne by another account") 
    else:
        print(">> Unknown error occured")             

    return { "response": r.status_code, "body": json.loads(r.content) }

if __name__ == "__main__":
    lambda_handler({ "apikey": "k_kVsKS05Xl5TcgdfjUSLlnU0N4ivDr9wf404", "email": "lexaprofunfacts394@mailsac.com" }, "Local Environment")