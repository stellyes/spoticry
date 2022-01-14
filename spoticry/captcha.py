import os
import sys


sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from twocaptcha import TwoCaptcha

def solve(captcha_id, sign_up_url):
    api_key = os.getenv('APIKEY_2CAPTCHA', 'cfdd1e0dafb83224e79a5ade1e9191a9')

    solver = TwoCaptcha(api_key)

    try:
        result = solver.recaptcha(
            sitekey=captcha_id,
            url=sign_up_url)

    except Exception as e:
        sys.exit(e)

    else:
        return('solved: ' + str(result))

if __name__ == "__main__":
    solve()