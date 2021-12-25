import spoticore
import verify as verify


def main():
    amount = 100

    for i in range(amount):
        print("\n>> Generating new user...")

        # Random elements initialized
        password_length = spoticore.random_parameter(8, 16)
        domain_index = spoticore.random_parameter(0, 9)
        dob_month = spoticore.random_parameter(0, 11)
        dob_day = spoticore.random_parameter(1, 28)
        dob_year = spoticore.random_parameter(1982, 2006)

        # Generate spotifyUser data
        # Generate temp email address and email MD5 hash token
        email, email_hash = spoticore.generate_email(domain_index)
        # Generate random username
        username = spoticore.generate_username()
        # Generate random password
        password = spoticore.generate_password(password_length)
        # Generate random birthday
        birthday = spoticore.generate_birthday(dob_month, dob_day, dob_year)
        # Generate random gender selection
        gender = spoticore.random_parameter(0, 2)
        # Generate random response to marketing infomation
        marketing_info = spoticore.random_parameter(0, 1)

        # Generate random proxy from list of scraped proxies
        print(">> Fetching proxy information...")
        proxy_info = spoticore.get_proxy()
        print(">> Proxy " + proxy_info['ip'] + " selected")

        # If proxy fails connection, get new proxy value to assign
        print(">>\t Testing connection: " + proxy_info['ip'] + "...")
        if (spoticore.test_connection(proxy_info['ip']) < 2):
            print(">>\t Testing connection: " + proxy_info['ip'] + "...")
            proxy_info = spoticore.get_proxy()
            print(">> Proxy " + proxy_info['ip'] + " selected")

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
            "md5_hash": email_hash,
            "proxy": proxy_info,
            "verified": {
                "status": '',
                "date": ''
            }
        }

        print(">> Credentials for " + newUser["user"] + " generated")

        # Send credentials to sign-up page using webdriver
        # print(">> Verifying user...")
        # status, date = verify.sign_up(newUser)

        # Print generated user to JSON file
        spoticore.update_records(email_hash, newUser)

        print(">> User " + newUser["user"] + " successfully generated\n")


if __name__ == "__main__":
    main()
