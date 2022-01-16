import time
import utils

import requests

def generate_user(user):

    gender = user['gender']

    if gender == 0:
        parsed_gender = "male"
    elif gender == 1:
        parsed_gender = "female"
    elif gender == 2:
        parsed_gender = "non-binary"
        
    headers={"Accept-Encoding": "gzip",
             "Accept-Language": "en-US",
             "App-Platform": "Android",
             "Connection": "Keep-Alive",
             "Content-Type": "application/x-www-form-urlencoded",
             "Host": "spclient.wg.spotify.com",
             "User-Agent": "Spotify/8.6.72 Android/29 (SM-N976N)",
             "Spotify-App-Version": "8.6.72",
             "X-Client-Id": utils.generate_random_string(32)}
    
    payload = {"creation_point": "client_mobile",
            "gender": parsed_gender,
            "birth_year": user['dob']['year'],
            "displayname": user['user'],
            "iagree": "true",
            "birth_month": user['dob']['month'],
            "password_repeat": user['pass'],
            "password": user['pass'],
            "key": "142b583129b2df829de3656f9eb484e6",
            "platform": "Android-ARM",
            "email": user['email'],
            "birth_day": user['dob']['day']}
    
    r = requests.post('https://spclient.wg.spotify.com/signup/public/v1/account/', headers=headers, data=payload)

    if r.status_code==200:
        if r.json()['status']==1:
            return (True, time.time())
        else:
            #Details available in r.json()["errors"]
            print(r.json()["errors"])
            return (False, "Could not create the account, some errors occurred")
    else:
        return (False, "Could not load the page. Response code: "+ str(r.status_code))             


