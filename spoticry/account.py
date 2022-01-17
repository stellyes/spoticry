import utils
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
        proxy_info = utils.get_proxy()

        print(">> Credentials for " + username + " generated")

        # Create spotifyUser dictionary
        newUser = {
            "email": "dawine9023@leezro.com",
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
            "created": {
                "status": '',
                "date": ''
            },
            "verified": {
                "status": '',
                "date": ''
            }
        }

        # Send credentials to sign-up page using webdriver
        print(">> Verifying user...")
        status, date = spoticore.generate_user(newUser)

        # Print generated user to JSON file
        utils.update_records(newUser)

        print(">> User " + newUser["user"] + " successfully generated\n")

        

if __name__ == "__main__":
    main()
