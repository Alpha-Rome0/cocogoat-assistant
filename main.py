import browser_cookie3
import os
import requests

# select browser based on config file options
# locate hoyo cookies and return them
def get_local_cookies():
    browser = 'firefox'

    # call different module functions based on browser, ex: browser_cookie3.firefox()
    # using browser as a variable string
    get_cookies_from_selected_browser = getattr(browser_cookie3, browser)

    # only select cookies for hoyolab.com domain, store in cookie jar
    jar = get_cookies_from_selected_browser(domain_name='hoyolab.com')
    cookie_dictionary = requests.utils.dict_from_cookiejar(jar)

    return cookie_dictionary

# get hoyo cookies using github workflow with repo secrets
def get_workflow_cookies():
    cookie_dictionary = {}

    cookie_dictionary['ltuid'] = os.environ.get('LTUID')
    cookie_dictionary['ltoken'] = os.environ.get('LTOKEN')
    return cookie_dictionary

# send a post request with auth cookies to claim materials, primos, and food from hoyo website
def claim_rewards(cookie_dictionary):
    url = "https://hk4e-api-os.mihoyo.com/event/sol/sign?act_id=e202102251931481&lang=en-us"

    ltuid = cookie_dictionary["ltuid"]
    ltoken = cookie_dictionary["ltoken"]
    cookies = {'ltuid': ltuid, 'ltoken': ltoken}

    r = requests.post(url, cookies=cookies)
    # print status of request
    print(r.json())

cookie_dictionary = get_local_cookies()
claim_rewards(cookie_dictionary)