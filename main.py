import requests
import browser_cookie3

def get_local_cookies():
    browser = 'firefox'

    get_cookies_from_selected_browser = getattr(browser_cookie3, browser)

    cookie_dictionary = requests.utils.dict_from_cookiejar(get_cookies_from_selected_browser(domain_name='hoyolab.com'))

    print(cookie_dictionary)
    return cookie_dictionary

def get_workflow_cookies():
    return

def claim_rewards(cookie_dictionary):
    url = "https://hk4e-api-os.mihoyo.com/event/sol/sign?act_id=e202102251931481&lang=en-us"

    ltuid = cookie_dictionary["ltuid"]
    ltoken = cookie_dictionary["ltoken"]
    cookies = {'ltuid': ltuid, 'ltoken': ltoken}

    r = requests.post(url, cookies=cookies)
    print(r.json())

cookie_dictionary = get_local_cookies()
claim_rewards(cookie_dictionary)