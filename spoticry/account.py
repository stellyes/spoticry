import utils
import verify
import random
import spoticore


def main():
    amount = 1

    for i in range(amount):
        print("\n>> Generating new user...")

        # Random elements initialized
        password_length = random.randint(8, 16)
        domain_index = random.randint(0, 9)
        dob_month = random.randint(0, 11)
        dob_day = random.randint(1, 28)
        dob_year = random.randint(1982, 2006)

        # utils spotifyUser data
        # utils temp email address and email MD5 hash token
        email = utils.generate_email(domain_index)
        # utils random username
        username = utils.generate_username()
        # utils random password
        password = utils.generate_password(password_length)
        # utils random birthday
        birthday = utils.generate_birthday(dob_month, dob_day, dob_year)
        # utils random gender selection
        gender = random.randint(0, 2)
        # utils random response to marketing infomation
        marketing_info = random.randint(0, 1)

        # utils random proxy from list of scraped proxies
        print(">> Fetching proxy information...")
        proxy_info = utils.get_proxy()
        print(">>\t Proxy " + proxy_info['ip'] + " selected")

        # If proxy fails connection, get new proxy value to assign
        #print(">>\t Testing connection: " + proxy_info['ip'] + "...")
        #if (utils.test_connection(proxy_info['ip']) < 2):    
            #print(">>\t Testing connection: " + proxy_info['ip'] + "...")
            #proxy_info = utils.get_proxy()
            #print(">> Proxy " + proxy_info['ip'] + " selected")

        print(">> Credentials for " + username + " generated")

        # Create spotifyUser dictionary
        newUser = {
            "email": email,
            "user": username,
            "pass": password,
            "dob": {
                "day": birthday.day,
                "month": birthday.month,
                "year": birthday.year
            },
            "gender": gender,
            "opt_in": marketing_info,
            "proxy": proxy_info,
            "verified": {
                "status": '',
                "date": ''
            }
        }

        # Send credentials to sign-up page using webdriver
        print(">> Verifying user...")
        status, date = verify.sign_up(newUser)

        # Print generated user to JSON file
        spoticore.update_records(newUser)

        print(">> User " + newUser["user"] + " successfully generated\n")

        

if __name__ == "__main__":
    main()
